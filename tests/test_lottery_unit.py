from logging import exception
import pytest
import scripts.deploy as lottery
import scripts.functions as func
from brownie import network, config, exceptions, VRFCoordinatorV2Mock
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
    assert contract.players(0) == account

def test_end_lottery():
    if(network.show_active() not in func.LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("Only for Local Testing")
    account = func.get_account()
    contract = lottery.deploy()
    txn = contract.startLottery({"from": account})
    txn.wait(1)
    txn2 = contract.enter({"from": account, "value": contract.getEntranceFee()})
    txn2.wait(1)
    txn3 = contract.endLottery({"from": account})
    txn3.wait(1)
    assert contract.lottery_state() == 2

def test_can_pick_winner():
    if(network.show_active() not in func.LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("Only for Local Testing")
    account = func.get_account()
    contract = lottery.deploy()
    txn = contract.startLottery({"from": account})
    txn.wait(1)
    txn2 = contract.enter({"from": account, "value": contract.getEntranceFee()})
    txn2.wait(1)
    txn3 = contract.enter({"from": func.get_account(index=1), "value": contract.getEntranceFee()})
    txn3.wait(1)
    txn4 = contract.enter({"from": func.get_account(index=2), "value": contract.getEntranceFee()})
    txn4.wait(1)
    #balance_of_lottery = lottery.balance()
    vrf_contract = VRFCoordinatorV2Mock[-1]
    sub_id_txn = vrf_contract.createSubscription({"from": account})
    sub_id_txn.wait(1)
    sub_id = sub_id_txn.events["SubscriptionCreated"]["subId"]
    fund_amount_link = 3000000000000000000
    fund_vrf_txn = vrf_contract.fundSubscription(sub_id, fund_amount_link, {"from": account})
    fund_vrf_txn.wait(1)
    txn5 = contract.endLottery(sub_id, vrf_contract.address, {"from": account})
    txn5.wait(1)
    request_id = txn5.events["requestedRandomWords"]["requestId"]
    fulfill_txn = vrf_contract.fulfillRandomWords(request_id, contract.address, {"from": account})
    fulfill_txn.wait(1)
    randomWords = fulfill_txn.events["RandomWordsFulfilled"]["outputSeed"]
    fulfill_lottery = contract.fulfillRandomWords(request_id, randomWords, {"from": account})
    fulfill_lottery.wait(1)
    assert contract.balance() == 0
    
def test_reset_lottery():
    if(network.show_active() not in func.LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip("Only for Local Testing")
    account = func.get_account()
    contract = lottery.deploy()
    txn = contract.startLottery({"from": account})
    txn.wait(1)
    txn2 = contract.enter({"from": account, "value": contract.getEntranceFee()})
    txn2.wait(1)
    txn3 = contract.enter({"from": func.get_account(index=1), "value": contract.getEntranceFee()})
    txn3.wait(1)
    txn4 = contract.enter({"from": func.get_account(index=2), "value": contract.getEntranceFee()})
    txn4.wait(1)
    funded_amount = contract.senderaddresstoamontvalue(account)
    print(f"funded with {funded_amount}")
    txn1 = contract.resetLottery({"from": account})
    txn1.wait(1)
    new_funded_amount = contract.senderaddresstoamontvalue(account)
    print(f"funded with {new_funded_amount}")
    lottery_state = contract.lottery_state()
    assert lottery_state == 1
    assert contract.balance() == 0
    
