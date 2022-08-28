from brownie import Lottery, network, config, VRFCoordinatorV2Mock
import scripts.functions as func
import time

def deploy():
    account = func.get_account()
    sub_id = config["chainlink"]["subscription_id"]
    price_feed = func.get_contract("eth_usd_price_feed")
    keyhash = config["networks"][network.show_active()]["keyhash"]
    vrf_coordinator = func.get_contract('vrf_coordinator')
    entrance_fee = 50
    contract = Lottery.deploy(sub_id, price_feed, vrf_coordinator, keyhash, entrance_fee, {"from": account}, publish_source=func.get_verify())
    print("Deployed")
    return contract

def start():
    account = func.get_account()
    contract = Lottery[-1]
    txn = contract.startLottery({"from": account})
    txn.wait(1)
    print("IT HAS BEGUN!!!")

def enter():
    account = func.get_account()
    contract = Lottery[-1]
    entrance_fee = contract.getEntranceFee() + 100000
    txn = contract.enter({"from": account, "value": entrance_fee})
    txn.wait(1)
    txn2 = contract.enter({"from": account, "value": entrance_fee})
    txn2.wait(1)
    txn3 = contract.enter({"from": func.get_account(index=1), "value": entrance_fee})
    txn3.wait(1)
    txn4 = contract.enter({"from": func.get_account(index=2), "value": entrance_fee})
    txn4.wait(1)
    #print(f"You have entered the lottery with $50")

def end():
    account = func.get_account()
    contract = Lottery[-1]
    vrf_contract = VRFCoordinatorV2Mock[-1]
    sub_id_txn = vrf_contract.createSubscription({"from": account})
    sub_id_txn.wait(1)
    sub_id = sub_id_txn.events["SubscriptionCreated"]["subId"]
    fund_amount_link = 300000000000000000000
    fund_vrf_txn = vrf_contract.fundSubscription(sub_id, fund_amount_link, {"from": account})
    fund_vrf_txn.wait(1)
    print(f"Old lottery balance: {contract.balance()}")
    txn5 = contract.endLottery(sub_id, vrf_contract.address, {"from": account})
    txn5.wait(1)
    request_id = txn5.events["requestedRandomWords"]["requestId"]
    fulfill_txn = vrf_contract.fulfillRandomWords(request_id, contract.address, {"from": account})
    fulfill_txn.wait(1)
    randomWords = fulfill_txn.events["RandomWordsFulfilled"]["success"]
    print(f"Success is {randomWords}")
    #time.sleep(60)
    print(f"New lottery balance: {contract.balance()}")
    print("Lottery ended!")
    #print(f"Randomwords is {contract.s_randomWords(0)}")
    print(f"{contract.winner()} is the new Winner!")

def main():
    deploy()
    start()
    enter()
    end()