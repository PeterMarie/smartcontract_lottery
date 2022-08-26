from logging import exception
import pytest
import scripts.deploy as lottery
import scripts.functions as func
from brownie import network, config, exceptions
from web3 import Web3

def test_entrance_fee():
    if(network.show_active() not in func.LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("Only for Local Testing")
    #arrange
    contract = lottery.deploy()
    #act
    entrance_fee = contract.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    #assert
    assert entrance_fee == expected_entrance_fee

def test_enter_only_after_start():
    if(network.show_active() not in func.LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("Only for Local Testing")
    contract = lottery.deploy()
    with pytest.raises(exceptions.VirtualMachineError):
        contract.enter({"from": func.get_account(), "value": contract.getEntranceFee()})

def test_start_and_enter():
    if(network.show_active() not in func.LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("Only for Local Testing")
    account = func.get_account()
    contract = lottery.deploy()
    txn = contract.startLottery({"from": account})
    txn.wait(1)
    txn2 = contract.enter({"from": account, "value": contract.getEntranceFee()})
    txn2.wait(1)
    assert contract.players[0] == account
