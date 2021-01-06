import unittest
import shutil
import os
from .api.doc import get_pages, get_header, download_html, html2json
from .api.gist import clone_files, display_gist
from .api.problem import update_leetcode, update_baekjoon_level, update_baekjoon, get_problems
from .api.student import update_solved, get_id2solved, get_students
from .common import PATH, get_chrome_driver, get_db_instance, get_logger

logger = get_logger(__name__)


class PageTester(unittest.TestCase):
  def setUp(self):
    logger.debug("Setting up")
    shutil.rmtree(PATH.TEST, ignore_errors=True)
    os.mkdir(PATH.TEST)

  def tearDown(self):
    logger.debug("Tearing down")
    shutil.rmtree(PATH.TEST)

  def test_common(self):
    logger.debug("Test common")
    driver = get_chrome_driver()
    self.assertIsNotNone(driver, "Failed to get Chrome Driver")

    db = get_db_instance()
    self.assertIsNotNone(db, "Failed to get Chrome Driver")

    sample_doc = {"id": "id", "title": "title"}
    db.collection("test").document(sample_doc["id"]).set(sample_doc, merge=True)
    self.assertEqual(db.collection("test").document(sample_doc["id"]).get().to_dict(), sample_doc, "Failed to get")

  def test_problem(self):
    logger.debug("Test problem")
    self.assertGreater(len(update_baekjoon_level(30)), 5, "Failted to get baekjoon")
    self.assertGreater(len(update_baekjoon(28, 31)), 50, "Failed to get baekjoon")
    self.assertEqual(len(update_leetcode(3)), 3, "Failed to get leetcode")
    self.assertGreater(get_problems("Syntax", "IO", "Print"), 3)

  def test_doc(self):
    logger.debug("Test doc")
    pages = get_pages(3)
    self.assertEqual(len(pages), 3, "Failed to get pages from firebase")
    page = pages[-1]

    html = download_html(page["doc_id"], page["id"], PATH.TEST)

    self.assertGreater(len(html), 300, "Failed to download html")
    doc_json = html2json(html)
    self.assertIsNotNone(doc_json, "Failed to convert to json")
    headers = get_header()
    self.assertIsNotNone(headers, "Header is empty")

  def test_gist(self):
    logger.debug("Test gist")
    sample_gist = "e7f4b99c5e625651abdeef29e328a423"
    clone_files(sample_gist, PATH.TEST)
    self.assertGreater(len(os.listdir(PATH.TEST / sample_gist)), 1, "Clone failed")

    html = display_gist(sample_gist)
    self.assertGreater(len(html), 100, "Failed to convert html")

  def test_student(self):
    logger.debug("Test students")
    self.assertGreater(len(update_solved("rbtmd1010")), 100, "Failed to crawl solved problems")
    self.assertEqual(len(get_id2solved(3).keys()), 3, "Failed to get all solved")
    self.assertGreater(len(get_students("prake")), 10, "Failed to get prake students")


if __name__ == '__main__':
  # run single_test
  suite = unittest.TestSuite()
  suite.addTest(PageTester("test_new"))
  runner = unittest.TextTestRunner()
  runner.run(suite)
  # unittest.main()
