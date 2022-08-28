from logging import exception
import pytest
import scripts.deploy as lottery
import scripts.functions as func
from brownie import network, Contract, Lottery
from web3 import Web3
import time

def test_can_pick_winner():
    if(network.show_active() in func.LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("NOT for Local Testing")
    account = func.get_account()
    contract = lottery.deploy()
    #contract = Contract.from_abi(Lottery._name, '0x942da7A77312c1a7216ddbe7B7F351DAAb183119', Lottery.abi)
    #print(contract.lottery_state())
    #time.sleep(120)
    txn = contract.startLottery({"from": account})
    txn.wait(1)
    txn2 = contract.enter({"from": account, "value": contract.getEntranceFee() + 1000})
    txn2.wait(1)
    txn3 = contract.enter({"from": account, "value": contract.getEntranceFee() + 1000})
    txn3.wait(1)
    txn4 = contract.endLottery({"from": account})
    time.sleep(60)
    assert contract.winner() == account
    assert contract.balance() == 0

