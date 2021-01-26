import os
import json
import pathlib
import functools
from firebase_admin import credentials, firestore, initialize_app
from .models.member import Member
from .models.team import Team
from .models.gist import Gist
from .models.problem import Problem
from .models.doc import Doc
from .models.mock import Mock
from .common import PATH, logger, service_account_credential, html2text
from algoliasearch.search_client import SearchClient


def dict2class(collection_id, dict):
  COLLECTION_ID2CLS = {"member": Member, "team": Team, "mock": Mock, "gist": Gist, "problem": Problem, "doc": Doc, "mock": Mock}
  return COLLECTION_ID2CLS[collection_id](**dict)


class FirebaseDB():
  def __init__(self):
    cred = credentials.Certificate(service_account_credential)
    try:
      initialize_app(cred)
    except Exception as e:
      logger.error(e)
      return
    self._db = firestore.client()

  def add(self, collection_id, document, overwrite=True):
    document_id = document.__dict__[collection_id + "_id"]
    document_ref = self._db.collection(collection_id).document(document_id)

    if not overwrite and document_ref.get().exists:
      return False
    document_ref.set(document.__dict__)
    return True

  def delete(self, collection_id, document_id, ignore_missing=True):
    logger.debug(f"delete({collection_id}, {document_id})")

    document_ref = self._db.collection(collection_id).document(document_id)
    if not ignore_missing and not document_ref.get().exists:
      return False
    document_ref.delete()
    return True

  @functools.lru_cache
  def get_all(self, collection_id):
    logger.debug(f"get_all({collection_id})")
    return {doc_ref.id: dict2class(collection_id, doc_ref.to_dict()) for doc_ref in self._db.collection(collection_id).get()}

  def get(self, collection_id, document_ids):
    document_id2obj = self.get_all(collection_id)
    documents = []
    if not isinstance(document_ids, list):
      document_ids = [document_ids]
    for document_id in document_ids:
      documents.append(document_id2obj[document_id])
    return documents[0] if len(documents) == 1 else documents


remote_db = FirebaseDB()


class JsonDB():
  def add(self, collection_id, documents, overwrite=True):
    if not isinstance(documents, list):
      documents = [documents]

    pathlib.Path(f"{PATH.DB}/{collection_id}").mkdir(parents=True, exist_ok=True)
    for document in documents:
      document_id = document.__dict__[collection_id + "_id"]
      document_path = PATH.DB / collection_id / f"{document_id}.json"
      if os.path.exists(document_path) and not overwrite:
        return False
      with open(document_path, "w") as f:
        json.dump(document.__dict__, f, ensure_ascii=False)
    return True

  def delete(self, collection_id, document_id, ignore_missing=True):
    logger.debug(f"delete({collection_id}, {document_id})")
    document_path = PATH.DB / collection_id / f"{document_id}.json"
    if document_path.exists:
      os.remove(document_path)
    elif not ignore_missing:
      return False
    return True

  @functools.lru_cache
  def get_all(self, collection_id):
    logger.debug(f"get_all({collection_id})")
    collection_path = PATH.DB / collection_id
    document_id2obj = {}
    for document_path in collection_path.iterdir():
      with open(document_path, "r") as f:
        document_id2obj[document_path.name[:-5]] = dict2class(collection_id, json.load(f))
    return document_id2obj

  def get(self, collection_id, document_ids):
    document_id2obj = self.get_all(collection_id)
    if not isinstance(document_ids, list):
      document_ids = [document_ids]
    documents = []
    for document_id in document_ids:
      documents.append(document_id2obj[document_id])
    return documents[0] if len(documents) == 1 else documents


def get_algolia_client():
  if "ALGOLIA" not in os.environ:
    return
  algolia_credential = os.environ["ALGOLIA"]
  return SearchClient.create('36HZ0DWIJ7', algolia_credential)


local_db = JsonDB()

if __name__ == "__main__":
  algolia_client = get_algolia_client()
  index = algolia_client.init_index('page')
  index.clear_objects()
  for doc in local_db.get_all("page").values():
    gist_texts = ""
    for gist_id in doc.contents["gist_ids"]:
      gist = local_db.get("gist", gist_id)
      gist_texts += html2text(gist.html)
    index.save_objects([{**doc.contents, 'objectID': "-".join([doc.contents['doc_id'], content['h1'], content['h2'], content['h3'], content['li']]), "gist_texts": gist_texts} for content in doc.contents])
