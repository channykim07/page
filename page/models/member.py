from flask_login import UserMixin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import islice
from ..common import get_chrome_driver, PATH, logger
import json
import re
import os
import time


class Member(UserMixin):
  def __init__(self, member_id="", baekjoon_id="", team_id="", en_name="", kr_name="", solved_problem_ids=None, is_admin=False, id=""):
    self.id = member_id  # for flask_login mixin
    self.member_id = member_id
    self.baekjoon_id = baekjoon_id
    self.team_id = team_id
    self.en_name = en_name
    self.kr_name = kr_name
    self.solved_problem_ids = set(solved_problem_ids) if solved_problem_ids else set()
    self.is_admin = is_admin

  def __repr__(self):
    return f"{self.id}"

  @staticmethod
  def update_baekjoon_solved(member):
    from ..database import remote_db
    driver = get_chrome_driver()
    try:
      driver.get(f"https://www.acmicpc.net/user/{member.baekjoon_id}")
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
      member.solved_problem_ids = list(f'BJ_{prob_id}' for prob_id in driver.find_element_by_class_name('panel-body').text.split())
      remote_db.add("member", member)
      return True
    except Exception as e:
      logger.warning(f"{e}")
      logger.warning(f"{member}")
      return False
    finally:
      driver.quit()

  @staticmethod
  def update_all_baekjoon_solved(members, limit=10000):
    logger.debug(f"update_all_baekjoon_solved({members})")

    with ThreadPoolExecutor() as ex:
      futures = [ex.submit(Member.update_baekjoon_solved, member) for member in islice(members, limit)]
      return all(future.result() for future in as_completed(futures))
