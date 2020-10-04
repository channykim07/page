from flask_login import UserMixin, current_user
from .common import get_logger, PATH, get_db_instance
import json

log = get_logger(__name__)


class User(UserMixin):
  def __init__(self, id="", en_name=""):
    self.id = id
    db = get_db_instance()
    user_doc = next(db.collection("user").where('id', '==', id).stream(), None)
    if not user_doc:
      db.collection("user").document(id).set({"id": id, "en_name": en_name, "solved": [], "class_id": ""})
      user_doc = next(db.collection("user").where('id', '==', id).stream(), None)
    user_doc = user_doc.to_dict()
    log.debug(user_doc)

    self.solved = user_doc['solved']
    problems = [doc.to_dict() for doc in db.collection("problem").order_by("h1").get()]
    solved_set, unsolved_gist = set(self.solved), []
    for problem in problems:
      if 'id' in problem and problem["id"] not in solved_set:
        if "py" in problem:
          unsolved_gist.append(problem["py"])
        if "sh" in problem:
          unsolved_gist.append(problem["sh"])

    self.unsolved_gist = unsolved_gist
    log.debug(self.unsolved_gist)

  def __repr__(self):
    return f"{self.__dict__}"

  @staticmethod
  def get(id):
    return User(id)


if __name__ == "__main__":
  pass
