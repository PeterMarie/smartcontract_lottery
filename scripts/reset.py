from brownie import Lottery
import scripts.functions as func

def reset():
    account = func.get_account()
    contract = Lottery[-1]
    old_balance = contract.balance()
    print(f"Initial Lottery Balance is {old_balance}")
    txn1 = contract.resetLottery({"from": account})
    txn1.wait(1)
    print("Lottery reset")
    new_balance = contract.balance()
    print(f"New Lottery Balance is {new_balance}")

def get_values():
    account = func.get_account()
    contract = Lottery[-1]
    #requestedvalue = contract.lottery_state()
    #requestedvalue = contract.s_randomWords()
    requestedvalue = contract.s_requestId()
    print(f"Requested value is {requestedvalue}")
    

def main():
    get_values()