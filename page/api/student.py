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


def get_students(id):
  db = get_db_instance()
  students = []
  for student in db.collection("class").document("prake").get().to_dict()["user_ids"]:
    students.append(db.collection("user").document(student).get().to_dict())
  return students


def get_solved(id):
  return db.collection("user").document(id).get().to_dict()["solved"]


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


def update_solved(baekjoon_id):
  logger.info(f"update_solved({baekjoon_id})")
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
    future2id = {ex.submit(update_solved, user_dic["bj_id"]): user_dic["id"] for user_dic in user_dics}
    for future in as_completed(future2id):
      id = future2id[future]
      id2solved[id] = future.result()
  return id2solved


if __name__ == "__main__":
  db = get_db_instance()
  for id, solved in get_id2solved().items():
    db.collection("user").document(id).set({"solved": solved}, merge=True)
