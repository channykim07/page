def create_conroller(type_):
  if type_ == "CONSOLE":
    return ConsoleBankController()

class ConsoleBankController:
  def __init__(self, _model):
    self._model = _model

  def run(self, command):
    if command == "9":
      self.model.status = Status.OVER
      return True

    if self.model.status == Status.CARD_YET:
      if command == "1":
        self.model.status = Status.PIN_YET
    elif self.model.status == Status.PIN_YET:
      if command == "1":
        self.
    elif self.model.status == Status.READY:
      