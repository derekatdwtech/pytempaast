import logging
import sys
from modules.config import Config

config = Config()

#setup handlers
fHand = logging.FileHandler("pytempaast.log")
sHand = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pytempaast.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('tempaast')