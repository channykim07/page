import io
import json
import pathlib

from ..common import PATH, logger, service_account_credential
from bs4 import BeautifulSoup
from httplib2 import Http
from itertools import islice
from functools import lru_cache
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class Doc:
  def __init__(self, doc_id="", file_id="", headers=None, contents=None):
    self.doc_id = doc_id
    self.file_id = file_id
    self.headers = headers or {}
    self.contents = contents or []

  def __repr__(self):
    return f"{self.doc_id} / {len(self.contents)}"

  @classmethod
  def get_doc(cls, doc_id, file_id):
    logger.debug(f"get_doc({doc_id}, {file_id})")
    doc = Doc(doc_id, file_id)
    html = Doc.get_html(doc_id, file_id)
    doc.update_headers_contents(doc, html)
    return doc

  @staticmethod
  def get_html(doc_id, file_id):
    # https://developers.google.com/drive/api/v3/quickstart/python
    logger.debug(f"get_html({doc_id}, {file_id})")

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_credential, ['https://www.googleapis.com/auth/drive.readonly'])
    http_auth = credentials.authorize(Http())
    service = build('drive', 'v3', http=http_auth, cache_discovery=False)

    request = service.files().export(fileId=file_id, mimeType=f'text/html')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False
    while not done:
      status, done = downloader.next_chunk()
    fh.seek(0)
    return fh.read()

  def update_headers_contents(self, doc, html):
    logger.debug(f"update_headers_contents({doc})")
    bs = BeautifulSoup(html, "html.parser")

    h1, h2, h3, li = "", "", "", ""
    tags = list(filter(lambda tag: tag.text != "", bs.findAll(["h1", "h2", "h3", "p", "li"])))
    i = -1
    while i + 1 < len(tags):
      i += 1
      tag = tags[i]

      if tag.name == "h1":
        h1, h2, h3 = tag.text, "", ""
        doc.headers[h1] = {}
        doc.headers[h1][''] = {}
        doc.headers[h1][''][''] = []
      elif tag.name == "h2":
        h2, h3 = tag.text, ""
        doc.headers[h1][h2] = {}
        doc.headers[h1][h2][''] = []
      elif tag.name == "h3":
        h3 = tag.text
        doc.headers[h1][h2][h3] = []
      elif tag.name == "li":
        li = tag.text
        doc.headers[h1][h2][h3].append(li)
        gist_ids, form_ids, ps, problem_ids = [], [], [], []
        while i + 1 < len(tags) and tags[i + 1].name == "p":
          i += 1
          tag = tags[i]
          # CASE 1: [GIST] LC_1117.py (2)                   # comment
          # CASE 2: [GIST] convex_hull_plot.ipynb
          if tag.text.startswith("[GIST]"):
            try:
              line = tag.text[:tag.text.find("#")].strip()  # remove comment
              _, file_name = line.split(" ", 1)
              # https://gist.github.com/ef6b0f8aae30418b919c865e461ed0a9&sa=D&ust=1610638535418000&usg=AOvVaw2d54EQAi5OUwl9yfzUZxy0
              gist_id = tag.next.next.attrs["href"].split("/")[-1]
              gist_id = gist_id[:gist_id.find("&")]
              gist_ids.append(gist_id)
              if "BJ_" in tag.text or "LC_" in tag.text or "KT_" in tag.text:
                problem_id = file_name.split('.')[0]
                problem_ids.append(problem_id)
            except Exception as e:
              logger.warning(str(e))
          # CASE 3: [FORM] MH_Exponent + TODO Extra logic
          elif tag.text.startswith("[FORM]"):
            # https://docs.google.com/forms/d/form_id/edit -> form_id
            form_id = tag.next.next.attrs["href"].split("/")[-2]
            form_ids.append(form_id)
          # CASE 4: [YTUB] YOUTUB + TODO Extra logic
          elif tag.text.startswith("[YTUB]"):
            ps.append(str(tag.find("a")))
          else:
            img = tag.find("img")
            table = tag.find("table")
            if img:
              ps.append(str(img))
            elif table:
              ps.append(str(table))
            else:
              ps.append(tag.text)
        doc.contents.append({"doc_id": doc.doc_id, "h1": h1, "h2": h2, "h3": h3, "li": li, "gist_ids": gist_ids, "form_ids": form_ids, "ps": ps, "problem_ids": problem_ids})
