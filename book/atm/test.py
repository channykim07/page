from model import BankModel
import unittest
import logging
import hashlib


class ATMTester(unittest.TestCase):
  def setUp(self):
    self.model = BankModel()
    self.test_name = "sean"
    self.test_pin = "1234"
    self.test_wrong_pin = "1235"
    self.test_small_amount = 10
    self.test_big_amount = 100
    self.model.register_user(self.test_name, self.test_pin)

  def testModel(self):
    # SignIn
    self.assertIsNotNone(self.model)
    self.assertFalse(self.model.signin(self.test_name, self.test_wrong_pin))
    self.assertTrue(self.model.signin(self.test_name, self.test_pin))

    self.assertTrue(self.model.deposit(self.test_small_amount))
    self.assertFalse(self.model.withdraw(self.test_big_amount))
    self.assertTrue(self.model.withdraw(self.test_small_amount))

  def tearDown(self):
    pass
    # self.model.delete_all_user()


if __name__ == "__main__":
  unittest.main()
