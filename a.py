import json
import urllib
from subprocess import PIPE, Popen
import time
import requests
import os
import math
from bs4 import BeautifulSoup
from urllib.parse import unquote
from itertools import islice
from firebase_admin import credentials, firestore, initialize_app
from math import ceil
from concurrent.futures import ProcessPoolExecutor


def clone_files(gist_ids, result_path=PATH.GIST):
  logger.info(f"clone_files({gist_ids}, {result_path})")
  if isinstance(gist_ids, str):
    gist_ids = [gist_ids]
  git_cred = get_git_credential()
  popens = []
  for gist_id in gist_ids:
    gist_url, gist_path = f"https://gist.github.com/{gist_id}.git", f"{result_path}/{gist_id}"
    if os.path.isdir(gist_path):
      popens.append(Popen(['git', '-C', gist_path, 'pull', gist_url], stdout=PIPE, stderr=PIPE))
    else:
      popens.append(Popen(['git', 'clone', gist_url, f"{result_path}/{gist_id}"], stdout=PIPE, stderr=PIPE))
  for popen in popens:
    popen.wait()
