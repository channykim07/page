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
from ..common import PATH, get_logger, get_git_credential, get_db_instance

logger = get_logger(__name__)


def clone_files(gist_ids, result_path=PATH.GIST):
  logger.info(f"clone_files({gist_ids}, {result_path})")
  if isinstance(gist_ids, str):
    gist_ids = [gist_ids]
  git_cred = get_git_credential()
  db = get_db_instance()
  popens = []
  for gist_id in gist_ids:
    gist_url, gist_path = f"https://gist.github.com/{gist_id}.git", f"{result_path}/{gist_id}"
    if os.path.isdir(gist_path):
      popens.append(Popen(['git', '-C', gist_path, 'pull', gist_url], stdout=PIPE, stderr=PIPE))
    else:
      popens.append(Popen(['git', 'clone', gist_url, f"{result_path}/{gist_id}"], stdout=PIPE, stderr=PIPE))
  for popen in popens:
    popen.wait()


def display_gist(gist_id, doc="py"):
  logger.info(f"display_gist({gist_id}, {doc})")
  result = requests.get(f'https://gist.github.com/{gist_id}.js', headers=get_git_credential()).content
  result = result.replace(b"\\\\", b"\\").replace(b"\\/", b"/").decode("unicode-escape")
  result = result.split("document.write('")[-1][:-3]
  bss = BeautifulSoup(result, "html.parser")

  for bs in bss.find_all(class_="gist"):
    file_box = bs.find(class_="file-box")
    root = bs.find(class_="file-box")
    toggle_div = bss.new_tag('div', attrs={"class": "gist-meta"})

    for i, d in enumerate(bs.find_all(class_="file")):
      if i != 0:
        file_box.append(d)  # combine to first table
      if doc != d.attrs['id'].split("-")[-1]:
        d.attrs["display"] = {"none"}

    for d in bs.find_all(class_="gist-meta"):
      siblings = list(d.next_elements)
      id, file_name = siblings[4].attrs["href"].split("#")[-1], siblings[5]
      toggle_a = bss.new_tag('a', attrs={"id": id, "class": f"gist-toggle", "onclick": f"toggle('{id}')", "style": "padding: 0 18px"})
      toggle_a.append(file_name)
      toggle_div.append(toggle_a)
      d.extract()  # remove bottom nav

    root.insert(0, toggle_div)
    for d in islice(bs.find_all(class_="gist-file"), 1, None):
      d.extract()  # remove except first

  return str(bss)


if __name__ == "__main__":
  clone_files(os.listdir(PATH.GIST))
