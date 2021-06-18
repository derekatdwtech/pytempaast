# PyTempaast

This project serves as a system where you can connect your DS18B20 sensors into a centralize and distributed system. Once installed we automatically configure your probe in our system and then you can manage it all on https://app.tempaast.com. Continue reading to get started.

## Intended Usage
This software is intended to be used only for DS18B20 probes. We scan /sys/bus/w1/devices for these....devices. We also intend for you to create one systemd service per device. I believe this is most advantageous. This registers each device with our system and thus you can turn off one device at a time for maintenance purposes. To install a serivce per device run the `install.sh` script for each device you want to setup. The installer walks you through the whole process.

## Getting Started
1. Go to https://app.tempaast.com and sign-up for an account.
2. Once your account is verified, and you are on your dashboard, to to the profile section and generate an api key
3. Download the latest release to your Raspberry Pi
4. Run the `install.sh` script in the folder to being. It's a guided install so it should be fairly simple to get started.

## Reporting Bugs
There will definitely be bugs. This project is basically pre-alpha. If you have a problem, you can contribute, or email me with a description of your problem. I'm pretty responsive.

## Contributing
This is my first open-sourced project. If you want to get involved with this project you can do so in a few ways:
1. Recommend this project to a hobbyist friend.
2. If you wish to collaborate, email derekcwilliams@protonmail.com
3. Donate. The website contains information on our run rate. I'm not trying to profit, but it would be nice to break even :)