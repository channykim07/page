# README

## Question

> Requirements

* Write code for a simple ATM.
  * Insert Card => PIN number => Select Account => See Balance / Deposit / Withdraw
  * A bank API wouldn't give the ATM the PIN number, but it can tell you if the PIN number is correct or not.
  * There are only 1 dollar bills in this world, no cents

* It doesn't need any UI nor REST API, RPC
  * a controller should be implemented and tested.
  * We may want to integrate it with a real bank system in the future
  * Test code for controller part (not including bank system, cash bin etc)

## Solution

> MVC Pattern

![mvc](images/20210219_190939.png)

* View (WIP)
  * Handler rendering logic
* Controller (WIP)
  * Handler user input logic
* Model
  * Service logic for bank account
* Database
  * JsonDB stores data in local db

* Sample main loop logic

```py
from main import Status
from model import create_model
from view import create_view
from controller import create_controller

VIEW_TYPE = "CONSOLE"
CONTROLLER_TYPE = "CONSOLE"
MODEL_TYPE = "MEMORY"

model = create_model(MODEL_TYPE)
view = create_view(VIEW_TYPE, model)
controller = create_controller(CONTROLLER_TYPE, model)

view.show_option(model.status)

while not Status.OVER:
  command = input()
  controller.run(command())
  view.run()
```