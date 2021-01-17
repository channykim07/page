import requests
import os
from ..common import PATH, logger, git_credential
from bs4 import BeautifulSoup
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote
from xml.sax import saxutils as su
import html.parser


class Gist:
  def __init__(self, gist_id="", h1="", h2='', h3='', li='', file_names=None, html=''):
    self.gist_id = gist_id
    self.h1 = h1
    self.h2 = h2
    self.h3 = h3
    self.li = li
    self.file_names = file_names or []
    self.html = html

  def __repr__(self):
    return f"{self.__dict__}"

  @classmethod
  def get_gist(cls, gist_id, h1="", h2="", h3="", li=""):
    logger.debug(f"get_gist({gist_id})")
    gist = cls(gist_id, h1, h2, h3, li)
    result = requests.get(f'https://gist.github.com/{gist_id}.js', headers=git_credential)
    if result.text.startswith("<!DOCTYPE html>"):
      logger.warning(gist)
      return None
    # update with regex
    result = result.text
    result = result.replace("\\/", "/").replace("\\&", "&").replace("\\$", "$").replace("\\<", "<").replace("\\`", "`").replace("\\n", "\n").replace('\\"', '"')
    result = html.unescape(result)
    result = result.split("document.write('")[-1][:-3]

    bs = BeautifulSoup(result, "html.parser")

    for tag in bs.find_all(class_="gist"):
      file_box = tag.find(class_="file-box")
      root = tag.find(class_="file-box")
      toggle_div = bs.new_tag('div', attrs={"class": "gist-meta"})

      for i, d in enumerate(tag.find_all(class_="file")):
        d["class"] = f"file gist-toggle gist-id-{gist_id}"
        if i != 0:
          file_box.append(d)  # combine to first table

      for d in tag.find_all(class_="gist-meta"):
        siblings = list(d.next_elements)
        file_id, file_name = siblings[4].attrs["href"].split("#")[-1], siblings[5]
        gist.file_names.append(file_name)
        toggle_a = bs.new_tag('a', attrs={"id": file_id, "class": f"gist-toggle gist-id-{gist_id}", "onclick": f"toggle('gist-id-{gist_id}', '{file_id}')", "style": "padding: 0 18px"})
        toggle_a.append(file_name)
        toggle_div.append(toggle_a)
        d.extract()  # remove bottom nav

      root.insert(0, toggle_div)
      for d in islice(tag.find_all(class_="gist-file"), 1, None):
        d.extract()  # remove except first
    gist.html = str(bs)
    return gist

  @staticmethod
  def get_all_gist(gist_ids, h1="", h2="", h3="", li=""):
    logger.debug(f"get_all_gist()")
    with ThreadPoolExecutor() as ex:
      futures = [ex.submit(Gist.get_gist, gist_id, h1, h2, h3, li) for gist_id in gist_ids]
      gists = [future.result() for future in as_completed(futures)]
      return [gist for gist in gists if gist != None]


if __name__ == "__main__":
  from ..database import local_db
  for doc in local_db.get("doc"):
    for content in doc.contents:
      local_db.add("gist", Gist.get_all_gist(content["gist_ids"], content["h1"], content["h2"], content["h3"], content["li"]))
  for gist in local_db.get("gist"):
    try:
      file_name = gist.file_names[0]
    except:
      logger.error(gist)
      continue
    if file_name.startswith("BJ_") or file_name.startswith("KT_") or file_name.startswith("LC_"):
      try:
        problem = local_db.get("problem", file_name.split(".")[0])
        problem.gist_id = gist.gist_id
        local_db.add("problem", problem)
      except Exception as e:
        logger.error(f"{e}")
        logger.error(gist)
