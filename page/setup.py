from .database import local_db, remote_db
from .models.doc import Doc
from .models.gist import Gist
from .models.member import Member
from .models.problem import Problem
import json

Member.update_all_baekjoon_solved([member for member in remote_db.get_all("member").values() if len(member.baekjoon_id) != 0])


local_db.add("doc", {"name": "Python", "id": "1uNFwWX34SJVOV341j2CqtYUiRps9O1Yh2HexThJ4i1E"})
# get docs from docs.json
with open(f"{PATH.SRC}/docs.json", "r") as f:
  docs = json.load(f)
  for doc in docs:
    doc = Doc.get_doc(doc["doc_id"], doc["file_id"])
    local_db.add("doc", doc)

local_db.add("problem", Problem.get_baekjoon_problems() + Problem.get_leetcode_problems())

for doc in local_db.get_all("doc").values():
  for content in doc.contents:
    local_db.add("gist", Gist.get_all_gist(content["gist_ids"], content["h1"], content["h2"], content["h3"], content["li"]))

for gist in local_db.get_all("gist").values():
  try:
    file_name = gist.file_names[0]
  except Exception as e:
    logger.error(f"{e}")
    continue
  if file_name.startswith("BJ_") or file_name.startswith("KT_") or file_name.startswith("LC_"):
    try:
      problem = local_db.get("problem", file_name.split(".")[0])
      problem.gist_id = gist.gist_id
      gist.problem_id = problem.problem_id
      local_db.add("problem", problem)
      local_db.add("gist", gist)
    except Exception as e:
      logger.error(e)
"""
"""
