from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import islice
from ..common import PATH, get_chrome_driver, get_logger, get_db_instance
import json
import re
import os
import time

logger = get_logger(__name__)


def recommend_problems(kr_names=""):
  logger.info(f"recommend_problems({kr_names})")
  db = get_db_instance()
  problems = [doc.to_dict() for doc in db.collection("problem").order_by("h1").get()]

  html = ""
  for kr_name in kr_names.split(" "):
    logger.debug(kr_name)
    student = next(db.collection("user").where("kr_name", "==", kr_name).stream(), {})
    if student:
      student = student.to_dict()
    else:
      continue
    html += f"<div style='width: 20%; float: left;'><h2>{student['kr_name']}</h2> <br>"
    todos = [problem for problem in problems if problem['id'] not in student["solved"] and problem.get("id", "").startswith("BJ")]
    todos.sort(key=lambda todo: (todo['h1'][4], todo['h2'], todo['h3'], todo["li"], todo['level']))

    h1, h2, h3, li = "", "", "", ""
    for todo in todos:
      if h1 != todo["h1"]:
        h1 = todo["h1"]
        html += h1 + "<br>"
      if h2 != todo["h2"]:
        h2 = todo["h2"]
        html += h2 + "<br>"
      if h3 != todo["h3"]:
        h3 = todo["h3"]
        html += h3 + "<br>"
      if li != todo["li"] and todo.get("id", "").startswith("BJ"):
        li = todo["li"]
        html += li + "<br>"
      if 'link' in todo:
        html += todo['link'] + "<br>"
    html += "</div>"
  return html


def enroll_class(class_id, user_id):
  logger.info(f"enroll_class({class_id}, {user_id})")
  db = get_db_instance()
  class_doc = db.collection("class").where("id", "==", class_id).get()
  if len(class_doc) == 0:
    return False
  class_doc = class_doc[0].to_dict()
  logger.debug(class_doc)
  db.collection("class").document(class_id).update({"user_ids": class_doc["user_ids"] + [user_id]})
  db.collection("user").document(user_id).update({"class_id": class_id})


def get_solved(baekjoon_id):
  logger.info(f"get_solved({baekjoon_id})")
  driver = get_chrome_driver()

  try:
    driver.get(f"https://www.acmicpc.net/user/{baekjoon_id}")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
    return [f'BJ_{prob_id}' for prob_id in driver.find_element_by_class_name('panel-body').text.split()]
  except Exception as e:
    logger.warning(f"{e} {baekjoon_id}")
    driver.quit()
    return []


def get_id2solved(limit=10000):
  logger.info(f"get_id2solved({limit})")
  db = get_db_instance()
  user_dics = [user_snap.to_dict() for user_snap in islice(db.collection("user").where('bj_id', '!=', "").stream(), limit)]
  id2solved = {}

  with ThreadPoolExecutor() as ex:
    future2id = {ex.submit(get_solved, user_dic["bj_id"]): user_dic["id"] for user_dic in user_dics}
    for future in as_completed(future2id):
      id = future2id[future]
      id2solved[id] = future.result()
  return id2solved


if __name__ == "__main__":
  db = get_db_instance()
  for id, solved in get_id2solved().items():
    db.collection("user").document(id).set({"solved": solved}, merge=True)
