import json
import re
import os
from ..common import PATH, get_logger, get_db_instance, get_chrome_driver
from itertools import islice, chain
from firebase_admin import credentials, firestore, initialize_app
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

logger = get_logger(__name__)


def display_problem(problem):
  if 'id' not in problem or 'title' not in problem or 'level' not in problem:
    return ''
  pid, title, level = problem['id'], problem['title'], problem['level']
  logger.debug(f"display_problem({pid}, {title}, {level})")
  if pid[:2] == "BJ":
    html = f'<a href="http://acmicpc.net/problem/{pid[3:]}" style="color:blue;">{title} ({level})</a>'
  elif pid[:2] == "LC":
    html = f'<a href="http://leetcode.com/problem/{title}" style="color:blue;">{title} ({level})</a>'
  elif pid[:2] == "KT":
    html = f'<a href="https://open.kattis.com/problems/{pid[3:]}" style="color:blue;">{title} ({level})</a>'
  else:
    return f''
  for user in problem.get("unsolved_by", []):
    html += user + " "
  return html + "<br>"


def get_problems(h1, h2, h3):
  db = get_db_instance()
  return [prob.to_dict() for prob in db.collection("problem").where('h1', '==', h1).where('h2', '==', h2).where('h3', '==', h3).get()]


def update_baekjoon_level(level):
  logger.info(f"update_baekjoon_level({level})")
  driver = get_chrome_driver()
  db = get_db_instance()
  problems = []
  try:
    id_title = []
    for page in range(1, 100):
      driver.get(f"https://solved.ac/problems/level/{level}?sort=id&direction=asc&page={page}")
      logger.debug(f"https://solved.ac/problems/level/{level}?sort=id&direction=asc&page={page}")
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'contents')))
      lines = driver.find_element_by_class_name('contents').text
      if '해당하는 문제가 없습니다' in lines:
        break
      for line in lines.split("\n"):                      # ex)
        line = line.strip("STANDARD").strip()             # 10430 나머지 계산 STANDARD -> 10430 나머지 계산
        id_title = line.split(' ', 1)                     # 10430 나머지 계산 -> [10430, 나머지 계산]
        if id_title[0].isdigit() and len(id_title) == 2:
          id, title = id_title
          doc = {'id': f"BJ_{id}", "title": title, 'level': level}
          logger.debug(str(doc))
          problems.append(doc)
  except Exception as e:
    logger.warn(e)
    driver.quit()
  else:
    driver.quit()
  return problems


def update_baekjoon(lo=0, hi=31):
  logger.info(f"update_baekjoon({lo}, {hi})")
  docs = []
  with ThreadPoolExecutor() as ex:
    future2level = {ex.submit(update_baekjoon_level, level): level for level in range(lo, hi)}
    for future in as_completed(future2level):
      docs.extend(future.result())
  return docs


def update_leetcode(total_count=10000):
  logger.info(f"update_leetcode({total_count})")
  driver = get_chrome_driver()
  problems = []

  try:
    driver.get(f"https://leetcode.com/problemset/all/")

    select = Select(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'select'))))
    select.select_by_visible_text('all')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-control')))

    data = driver.find_element_by_class_name("reactable-data").find_elements_by_tag_name("tr")
    for prob in islice(data, total_count):
      id, title, level = prob.text.split('\n')
      doc = {'id': f"LC_{id}", 'title': title, 'level': {"Easy": 1, "Medium": 2, "Hard": 3}[level[level.find(' ') + 1:]]}
      logger.debug(f"{id} {title}")
      problems.append(doc)
  except Exception as e:
    logger.error(e)
  return problems


if __name__ == "__main__":
  db = get_db_instance()
  bj_probs = update_baekjoon()
  for prob in bj_probs:
    db.collection("problem").document(prob["id"]).set(prob, merge=True)
  lc_probs = update_leetcode()
  for prob in lc_probs:
    db.collection("problem").document(prob['id']).set(prob, merge=True)
