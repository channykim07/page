import concurrent.futures
import unittest
import shutil
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models.team import Team
from .models.doc import Doc
from .models.member import Member
from .models.gist import Gist
from .models.problem import Problem
from .models.mock import Mock
from .database import remote_db, local_db
from .common import *
from google.cloud import firestore


class PageTester(unittest.TestCase):
  def test_database(self):
    logger.debug("test_database()")
    self.assertIsNotNone(get_oauth_credential())
    self.assertIsNotNone(get_git_credential())
    self.assertIsNotNone(get_service_account_credential())
    self.assertIsNotNone(remote_db)

    mock = Mock("sample")
    self.assertIsNotNone(remote_db.add("mock", mock, overwrite=True))
    self.assertFalse(remote_db.add("mock", mock, overwrite=False))
    self.assertEqual(remote_db.get("mock", "sample"), remote_db.get("mock")[0], mock)
    self.assertTrue(remote_db.delete("mock", "sample"))
    self.assertIsNone(remote_db.get("mock", "sample"))

    self.assertIsNotNone(local_db.add("mock", mock, overwrite=True))
    self.assertFalse(local_db.add("mock", mock, overwrite=False))
    self.assertEqual(local_db.get("mock", "sample"), local_db.get("mock")[0],  mock)
    self.assertTrue(local_db.delete("mock", "sample"))
    self.assertIsNone(local_db.get("mock", "sample"))

  def test_models(self):
    logger.debug("test_models()")
    self.assertIsNotNone(get_chrome_driver())
    self.assertEqual(len(Problem.get_leetcode_problems(3)), 3)
    self.assertGreater(len(Problem.get_baekjoon_problems_level(30)), 5)
    self.assertGreater(len(Problem.get_baekjoon_problems(28, 31)), 50)
    self.assertTrue(Member.update_baekjoon_solved(remote_db.get("member", "rbtmd1010")))
    self.assertTrue(Member.update_all_baekjoon_solved([member for member in remote_db.get("member") if len(member.baekjoon_id) != 0], 2))

    gist = Gist.get_gist("e7f4b99c5e625651abdeef29e328a423")
    self.assertGreater(len(gist.html), 100)
    self.assertTrue(Gist.get_all_gist(["c81940d03e79296936616c733d2b4f57", "e7f4b99c5e625651abdeef29e328a423"]))

    self.assertIsNotNone(Doc.get_doc("C++", "1dtPPhF9V5z5-mG44ixMHMrEK7j8QkEOVV_XLOWxO060"))

  def test_new(self):
    pass
    # Member.update_all_baekjoon_solved([member for member in remote_db.get("member") if len(member.baekjoon_id) != 0])


if __name__ == '__main__':
  # run single_test
  # suite = unittest.TestSuite()
  # suite.addTest(PageTester("test_new"))
  # runner = unittest.TextTestRunner()
  # runner.run(suite)

  unittest.main()
