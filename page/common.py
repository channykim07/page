import os
import json
import pathlib
import logging
import logging.config
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from firebase_admin import credentials, firestore, initialize_app
from threading import Lock
from dotenv import load_dotenv


lock = Lock()


class PATH:
  SRC = pathlib.Path(__file__).resolve().parent
  DOC = SRC / 'doc'
  API = SRC / 'api'
  CRED = SRC / 'cred'
  GIST = SRC / 'gist'
  TEST = SRC / 'test'
  ENV = SRC / '..' / '.env'
  Path(DOC).mkdir(exist_ok=True)
  Path(GIST).mkdir(exist_ok=True)


def get_logger(name, level=logging.INFO):  # WARNING 30, INFO 20, DEBUG 10
  logging.basicConfig(level=level, format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
  # logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True})  # ignore warning from other module
  logger = logging.getLogger(name)

  for hdlr in logger.handlers[:]:  # remove exsiting handlers -> prevents logging twice
    logger.removeHandler(hdlr)

  return logger


def get_service_account_credential():
  load_dotenv(dotenv_path=PATH.ENV)
  if "SERVICE_ACCOUNT" not in os.environ:
    return
  with open(f"{PATH.CRED}/service_account.json", "r") as f:
    service_cred = json.load(f)
  service_cred["private_key"] = os.environ["SERVICE_ACCOUNT"].replace("\\n", "\n")
  return service_cred


def get_git_credential():
  load_dotenv(dotenv_path=PATH.ENV)
  if "GIT" not in os.environ:
    return
  with open(f"{PATH.CRED}/git.json", "r") as f:
    git_cred = json.load(f)
  git_cred["Authorization"] = os.environ['GIT']
  return git_cred


def get_oauth_credential():
  load_dotenv(dotenv_path=PATH.ENV)
  if "OAUTH" not in os.environ:
    return
  with open(f"{PATH.CRED}/oauth.json", "r") as f:
    oauth_cred = json.load(f)
  oauth_cred["client_secret"] = os.environ["OAUTH"]
  return oauth_cred


def get_chrome_driver():
  global lock
  with lock:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--single-process")  # [Solves] DevToolsActivePort file doesn't exist
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
  return driver


def get_db_instance():
  cred = credentials.Certificate(get_service_account_credential())
  try:
    initialize_app(cred)
  except:
    pass
  return firestore.client()


if __name__ == "__main__":
  logger.info(PATH.DOC)
