import os
import json
import pathlib
from firebase_admin import credentials, firestore, initialize_app
from .models.member import Member
from .models.team import Team
from .models.gist import Gist
from .models.problem import Problem
from .models.doc import Doc
from .models.mock import Mock
from .common import PATH, logger, service_account_credential


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
    self.db = firestore.client()

  def add(self, collection_id, document, overwrite=True):
    logger.debug(f"add({collection_id}, document, {overwrite})")
    document_id = document.__dict__[collection_id + "_id"]
    document_ref = self.db.collection(collection_id).document(document_id)

    if not overwrite and document_ref.get().exists:
      return False
    document_ref.set(document.__dict__)
    return True

  def delete(self, collection_id, document_id, ignore_missing=True):
    logger.debug(f"delete({collection_id}, {document_id})")

    document_ref = self.db.collection(collection_id).document(document_id)
    if not ignore_missing and not document_ref.get().exists:
      return False
    document_ref.delete()
    return True

  def get(self, collection_id, document_ids=None):
    if document_ids:
      if not isinstance(document_ids, list):
        document_ids = [document_ids]
      documents = []
      for document_id in document_ids:
        document_ref = self.db.collection(collection_id).document(document_id)
        if document_ref.get().exists:
          documents.append(dict2class(collection_id, document_ref.get().to_dict()))
        else:
          return
      return documents[0] if len(documents) == 1 else documents
    else:
      return [dict2class(collection_id, f.to_dict()) for f in self.db.collection(collection_id).get()]


remote_db = FirebaseDB()


class JsonDB():
  def add(self, collection_id, documents, overwrite=True):
    if not isinstance(documents, list):
      documents = [documents]
    logger.debug(f"add({collection_id}, {len(documents)})")

    pathlib.Path(f"{PATH.DB}/{collection_id}").mkdir(parents=True, exist_ok=True)
    for document in documents:
      document_id = document.__dict__[collection_id + "_id"]
      document_path = PATH.DB / collection_id / f"{document_id}.json"
      if os.path.exists(document_path) and not overwrite:
        return False
      with open(document_path, "w") as f:
        json.dump(document.__dict__, f)
    return True

  def delete(self, collection_id, document_id, ignore_missing=True):
    logger.debug(f"delete({collection_id}, {document_id})")
    document_path = PATH.DB / collection_id / f"{document_id}.json"
    if document_path.exists:
      os.remove(document_path)
    elif not ignore_missing:
      return False
    return True

  def get(self, collection_id, document_id=None):
    logger.debug(f"get({collection_id}, {document_id})")
    if document_id:
      document_path = PATH.DB / collection_id / f"{document_id}.json"
      if os.path.exists(document_path):
        with open(document_path, "r") as f:
          return dict2class(collection_id, json.load(f))
      else:
        return
    else:
      collection_path = PATH.DB / collection_id
      documents = []
      for document_path in collection_path.iterdir():
        with open(document_path, "r") as f:
          documents.append(dict2class(collection_id, json.load(f)))
      return documents


local_db = JsonDB()
