from common import Status, logger, LOCAL_DB_PATH
from hashlib import sha224
import traceback
import json
import os
import glob


def hash(str_):
  return sha224(str_.encode()).hexdigest()


class JsonUserDB():
  def __init__(self, user_id, hashed_pin_id, balance):
    self.user_id = user_id
    self.hashed_pin_id = hashed_pin_id
    self.balance = balance

  @classmethod
  def get_user(cls, user_id):
    logger.info("get_user")
    try:
      with open(f"{LOCAL_DB_PATH}/{user_id}.json", "r") as read_file:
        data = json.load(read_file)
      return data
    except:
      return None

  def update_user(self):
    logger.info("update_user")
    try:
      with open(f"{LOCAL_DB_PATH}/{self.user_id}.json", "w") as f:
        user_dto = {"user_id": self.user_id, "hashed_pin_id": self.hashed_pin_id, "balance": self.balance}
        json.dump(user_dto, f)
    except Exception as e:
      traceback.print_exc()
      logger.warning(f"{e}")
      return False


class BankModel():
  def __init__(self, db_type="json"):
    self._status = Status.CARD_YET
    if db_type == "json":
      self.user_model = JsonUserDB
    else:
      throw("Unknown model")
    self.current_user = None

  def __repr__(self):
    return f"BankModel {self.__dict__}"

  def delete_all_user(self):
    logger.info("delete_all_user()")
    files = glob.glob(f'{LOCAL_DB_PATH}/*')
    for f in files:
      os.remove(f)

  def register_user(self, user_id, pin_id, balance=0):
    logger.info(f"register_user({user_id}, {pin_id})")
    if self.user_model.get_user(user_id) != None:
      logger.warn(f"User already exists")
      return False
    try:
      logger.info(f"writing to {LOCAL_DB_PATH}/{user_id}.json")
      user = self.user_model(user_id, hash(pin_id), balance)
      user.update_user()
      return True
    except Exception as e:
      logger.warning(str(e))
      traceback.print_exc()
      return False
    return self.user_model.register(user_id, pin_id)

  def _verify_pin(self, user_id, pin):
    if self.user_model.hashed_pin == hash(pin):
      console.info("Pin failed")
      return True
    else:
      return False

  def deposit(self, amount):
    self.current_user.balance += amount
    return True

  def withdraw(self, amount):
    if self.current_user.balance < amount:
      logger.info("Not enough money")
      return False
    self.current_user.balance -= amount
    return True

  def signin(self, user_id, pin_id):
    logger.info(f"signin({user_id}, {pin_id})")
    try:
      data = self.user_model.get_user(user_id)
      if hash(pin_id) != data["hashed_pin_id"]:
        logger.warning(f"login failed")
      else:
        logger.info(f"login Succeeded")
        self.current_user = self.user_model(data["user_id"], hash(pin_id), data["balance"])
    except Exception as e:
      traceback.print_exc()
      logger.warning(f"{e}")
      return False
    return self.current_user != None
