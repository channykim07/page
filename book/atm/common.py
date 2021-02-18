import logging
import logging.config
import json
from enum import Enum
from pathlib import Path

# ignore warning from other module
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Status(Enum):
  OVER = 0
  CARD_YET = 1
  PIN_YET = 2
  READY = 3

LOCAL_DB_PATH = Path(__file__).resolve().parent / 'db'