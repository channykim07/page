import re
import pickle
import io
import os.path
import json
import pathlib

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

from pprint import pprint as print
from ..common import PATH, get_logger, get_service_account_credential, get_db_instance
from itertools import islice
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup
from functools import lru_cache

logger = get_logger(__name__)


def get_pages():
  db = get_db_instance()
  pages = [f.to_dict() for f in db.collection("doc").get()]
  logger.info(f"{pages}")
  return pages


def download_html(doc_id, file_name, dest_path=PATH.DOC):
  """
  get docs from google and save to html
  https://developers.google.com/drive/api/v3/quickstart/python
  """
  logger.info(f"Downloading to {dest_path} {doc_id} {file_name}")
  credentials = ServiceAccountCredentials.from_json_keyfile_dict(get_service_account_credential(), ['https://www.googleapis.com/auth/drive.readonly'])

  http_auth = credentials.authorize(Http())
  service = build('drive', 'v3', http=http_auth, cache_discovery=False)

  request = service.files().export(fileId=doc_id, mimeType=f'text/html')
  fh = io.BytesIO()
  downloader = MediaIoBaseDownload(fd=fh, request=request)
  done = False
  while not done:
    status, done = downloader.next_chunk()
  fh.seek(0)
  return fh.read()


def html2json(html):
  bs = BeautifulSoup(html, "html.parser")
  doc = {}
  db = get_db_instance()

  cur_h1, cur_h2, cur_h3, cur_li = None, None, None, None
  tags = bs.findAll(["h1", "h2", "h3", "p", "li"])
  tags = list(filter(lambda tag: tag.text != "", tags))
  i = -1
  while i + 1 < len(tags):
    i += 1
    tag = tags[i]

    if tag.name == "h1":
      cur_h1 = tag.text
      doc[cur_h1] = {}
    elif cur_h1 != None and tag.name == "h2":
      cur_h2 = tag.text
      doc[cur_h1][cur_h2] = {}
    elif cur_h2 != None and tag.name == "h3":
      cur_h3 = tag.text
      doc[cur_h1][cur_h2][cur_h3] = []
    elif cur_h3 != None and tag.name == "li":
      cur_li = tag.text
      gists, forms, ps = [], [], []
      while i + 1 < len(tags) and tags[i + 1].name == "p":
        i += 1
        tag = tags[i]
        # CASE 1: [GIST] 0f2e02474831bfd40c69d9702e313bda LC_1117.py (2)
        # CASE 2: [GIST] b728688abda4aed59c414dbc973a8037 convex_hull_plot.ipynb
        if tag.text.startswith("[GIST]"):
          try:
            line = tag.text[:tag.text.find("#")].strip()
            _, gist_id, file_name = line.split(" ", 2)
            pid = file_name.split('.')[0]
            os.makedirs(f"{PATH.GIST}/{gist_id}", exist_ok=True)
            gists.append(gist_id)
            if "KT_" in tag.text:
              level = file_name[file_name.index("(") + 1:-1]
              logger.debug(str({"title": file_name.split(".")[0][3:], "level": float(level), "h1": cur_h1, "h2": cur_h2, "h3": cur_h3, "li": cur_li, "gist_id": gist_id}))
              db.collection("problem").document(pid).set({"title": file_name.split(".")[0][3:], "level": float(level), "h1": cur_h1, "h2": cur_h2, "h3": cur_h3, "li": cur_li, "gist_id": gist_id})
            elif "BJ_" in tag.text or "LC_" in tag.text:
              logger.debug(str({"h1": cur_h1, "h2": cur_h2, "h3": cur_h3, "li": cur_li, "gist_id": gist_id}))
              db.collection("problem").document(pid).update({"h1": cur_h1, "h2": cur_h2, "h3": cur_h3, "li": cur_li, "gist_id": gist_id})
          except Exception as e:
            logger.warning(str(e))
            logger.warning(file_name)
        # CASE 3: [FORM] MH_Exponent
        elif tag.text.startswith("[FORM]"):
          form_id = tag.next.next.attrs["href"].split("/")[-2]
          logger.info(f"Add form {form_id}")
          forms.append(form_id)
        elif tag.find("a"):
          ps.append(str(tag.find("a")))
        else:
          ps.append(tag.text)
      try:
        doc[cur_h1][cur_h2][cur_h3].append({"li": cur_li, "gists": gists, "forms": forms, "ps": ps})
      except:
        pass
  return doc


@lru_cache
def get_header(src_path=PATH.DOC):
  headers = {}
  for fn in pathlib.Path(src_path).glob("*.json"):
    logger.info(fn)
    headers[fn.stem] = doc_headers = {}
    with open(fn, "r") as f:
      doc = json.load(f)
    for h1, h2 in doc.items():
      doc_headers[h1] = {h2: list(h3.keys()) for h2, h3 in h2.items()}
  return headers


@lru_cache
def get_post(doc, h1, h2, h3):
  post = {}
  try:
    with open(f"{PATH.DOC}/{doc}.json", "r") as f:
      data = json.load(f)
    post = data[h1][h2][h3]
  except Exception as e:
    logger.warning(f"{e}")
    logger.warning(f"while openning {doc} {h1} {h2} {h3}")
  logger.debug(f"{post}")
  return post


if __name__ == '__main__':
  for page in get_pages():
    html = download_html(page["doc_id"], page["id"])
    docs = html2json(html)
    with open(f"{PATH.DOC}/{page['id']}.json", "w") as f:
      json.dump(docs, f, ensure_ascii=False)
