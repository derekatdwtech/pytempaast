import logging
import sys
from modules.config import Config

config = Config()

#setup handlers
fHand = logging.FileHandler(sys.argv[2] + ".pytempaast.log")
sHand = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        fHand,
        sHand
    ]
)
logger = logging.getLogger('tempaast')