import io
import json

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
