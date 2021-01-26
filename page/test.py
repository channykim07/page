import concurrent.futures
import unittest
import shutil
import os
import requests
import threading
import multiprocessing
import line_profiler
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models.team import Team
from .models.doc import Doc
from .models.member import Member
from .models.gist import Gist
from .models.problem import Problem
from .models.mock import Mock
from .database import remote_db, local_db
from .common import *
from .app import create_app
from flask import url_for


time_profile = line_profiler.LineProfiler()


class PageTester(unittest.TestCase):
  @time_profile
  def test_database(self):
    logger.debug("test_database()")
    self.assertIsNotNone(get_oauth_credential())
    self.assertIsNotNone(get_git_credential())
    self.assertIsNotNone(get_service_account_credential())
    self.assertIsNotNone(remote_db)
    mock = Mock("sample")
    self.assertIsNotNone(remote_db.add("mock", mock, overwrite=True))
    self.assertFalse(remote_db.add("mock", mock, overwrite=False))
    self.assertEqual(remote_db.get("mock", "sample"), list(remote_db.get_all("mock").values())[0], mock)
    self.assertTrue(remote_db.delete("mock", "sample"))

    self.assertIsNotNone(local_db.add("mock", mock, overwrite=True))
    self.assertFalse(local_db.add("mock", mock, overwrite=False))
    self.assertEqual(local_db.get("mock", "sample"), list(local_db.get_all("mock").values())[0],  mock)
    self.assertTrue(local_db.delete("mock", "sample"))

  @time_profile
  def test_models(self):
    logger.debug("test_models()")
    self.assertEqual(len(Problem.get_leetcode_problems(3)), 3)
    self.assertGreater(len(Problem.get_baekjoon_problems_level(30)), 5)
    self.assertGreater(len(Problem.get_baekjoon_problems(28, 31)), 50)
    self.assertTrue(Member.update_baekjoon_solved(remote_db.get("member", "rbtmd1010")))

    gist = Gist.get_gist("e7f4b99c5e625651abdeef29e328a423")
    print(gist)
    self.assertGreater(len(gist.html), 100)
    self.assertTrue(Gist.get_all_gist(["c81940d03e79296936616c733d2b4f57", "e7f4b99c5e625651abdeef29e328a423"]))
    self.assertIsNotNone(Doc.get_doc("C++", "1dtPPhF9V5z5-mG44ixMHMrEK7j8QkEOVV_XLOWxO060"))

  @time_profile
  def test_ui(self):
    logger.debug("test_ui()")
    client = create_app().test_client()
    # res = (client.get('/'))
    # future2level = {ex.submit(Problem.get_baekjoon_problems_level, level): level for level in range(lo, hi)}
    # download_thread = threading.Thread(target=app.run, kwargs={'port': os.environ.get("PORT"), 'use_reloader': False}, daemon=True)
    # download_thread.start()
    # remote_db.get("test", "sample")

  def tearDown(cls):
    time_profile.print_stats()


if __name__ == '__main__':
  # run single_test
  # suite = unittest.TestSuite()
  # suite.addTest(PageTester("test_ui"))
  # runner = unittest.TextTestRunner()
  # runner.run(suite)
  unittest.main()
