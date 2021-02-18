def create_view(type_, model):
  if type_ == "CONSOLE":
    return ConsoleBankView(model)

class ConsoleBankView():
  def __init__(self, _model):
    self._model = _model

  def run(self):
    if self.model.status == Status.OVER:
      print("Thank you")
    else:
      print("[Selct option]")
      if self.model.status == Status.CARD_YET:
        print("1: Insert Card")
        print("9: Turn off")
      elif self.model.status == Status.PIN_YET:
        print("1: Enter Pin")
        print("9: Turn off")
      elif self.model.status == Status.READY:
        print("1: Withdraw")
        print("2: Deposit")
        print("9: Turn off")