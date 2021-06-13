#!/bin/bash
red="\e[0;91m"
blue="\e[0;94m"
expand_bg="\e[K"
blue_bg="\e[0;104m${expand_bg}"
red_bg="\e[0;101m${expand_bg}"
green_bg="\e[0;102m${expand_bg}"
green="\e[0;92m"
white="\e[0;97m"
bold="\e[1m"
uline="\e[4m"
reset="\e[0m"

INSTALLATION_DIR=/opt/tempaasttest

PROBES=()

checkRegistration() {
	read -p "$(echo -e "Before we get started, have your registered for an account at https://app.tempaast.com? (Y/N): $reset")" has_registered
	if [[ "$has_registered" == "Y" || "$has_registered" == "y" ]]; then
		echo -e "${green}Wonderful! Thank you so much for supporting this project.${reset}"
	elif [[ "$has_registered" == "N" || "$has_registered" == "n" ]]; then
		echo -e "${red}Oh No! In order to continue, you'll need to headover https://app.tempaast.com to register for an account!${reset}"
		exit 1
	else
		echo "I'm sorry I don't recognize that input. Have you registered for an account? (Y/N)"
		checkRegistration
	fi
}

findTempProbes() {
	SEARCHDIR="/sys/bus/w1/devices"
	PROBES=$(find $SEARCHDIR -name "28-*")
	if [[ ${#PROBES[@]} > 0 ]]; then
		echo -e "${green}Found the following probes${reset}"
	else
		echo -e "${red}We didn't find any DS18B20 probes active. Please connect your probes and run the setup again.${reset}"
		exit 1
	fi
}

chooseProbeToSetup() {
	for i in "${!PROBES[@]}"; do
		echo "$(($i + 1))). ${PROBES[$i]}"
	done
	read -p  "$(echo -e "Please choose the probe you would like to setup: "$reset)" probe_selection
	if [[ $probe_selection > 0 ]]; then
		probe_id=${PROBES[$probe_selection - 1]}
	else
		echo -e "${red}You must choose a probe to install$reset"
		chooseProbeToSetup
	fi

}
chooseProbeName() {
	read -p "$(echo -e $green"Please provide a unqiue name for this probe: "$reset)" nickname
	if [[ $nickname == "" ]]; then
		chooseProbeName
	fi
}

# Start the real work

if [[ $EUID != 0 ]]; then
	echo -e "${red} You should run this script as root. We need to install some stuffs${reset}"
	exit 1
fi

# Check OS Type
if [[ ! $OSTYPE == "linux"* ]]; then
	echo -e "${red}This package only supports linux operating systems. Exiting...${reset}"
	exit 1
fi

# Check for modprobe binary
if ! which modprobe > /dev/null 2>&1; then
	# TODO Install modprobe for each os
	echo "${red}modprobe binary was not found. This is required. Please install modprobe before continuing.${reset}"
	exit 1
fi

# Check for python binary
if ! which python > /dev/null 2>&1; then
	echo "${red}python binary was not found. This is required. Please install modprobe before continuing.${reset}"
	exit 1
fi

echo -e "${green}**********************************************************************************${reset}"
echo -e "${green}********* Welcome to PyTempaast! LEt's walk you through the installation *********${rese}t"
echo -e "${green}**********************************************************************************${reset}"

#Ensure user has registered
checkRegistration

read -p "$(echo -e "Please paste in your API Key. You can retrieve this from https://app.tempaast.com/profile: ${reset}")" api_key
if [[ $api_key == "" ]]; then
	echo -e "${red}API Key is required. Please register for an account to continue. An invalid API Key will fail to authenticate against our API${reset}"
	exit 1
fi

# Choose Installation directory
read -p "$(echo -e $green"Where should we install PyTempaast? (Default: /opt/tempaast): "$reset)" INSTALLATION_DIR
if [[ $INSTALLATION_DIR == "" ]]; then
	INSTALLATION_DIR=/opt/tempaast
fi
# create installation dir
mkdir -p $INSTALLATION_DIR

# Discover TEmperature Probes
findTempProbes

chooseProbeToSetup

chooseProbeName

echo -e "Checking for Tempaast user..."
if id "tempaast" ; then
	echo -e "Tempaast user exists"
else
	useradd tempaast
fi

echo -e "Setting up installation directory..."
mkdir -p $INSTALLATION_DIR

echo -e "Copying Application files..."
cp -Rf python/. $INSTALLATION_DIR
chown -Rf  tempaast: $INSTALLATION_DIR

echo -e "Installing python requirements..."
pip install -r $INSTALLATION_DIR/requirements.txt

echo -e "Setting up service..."
cp -f etc/template.service "tempaast-${nickname}.service"
sed -i "s/#{probeName}/${nickname}/g" "tempaast-${nickname}.service"
sed -i "s|#{probeDir}|${probe_id}|g" "tempaast-${nickname}.service"
sed -i "s/#{userId}/${api_key}/g" "tempaast-${nickname}.service"
sed -i "s|#{installation_dir}|${INSTALLATION_DIR}|g" "tempaast-${nickname}.service"

mv "tempaast-${nickname}.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable "tempaast-${nickname}.service"
systemctl start "tempaast-${nickname}.service"
