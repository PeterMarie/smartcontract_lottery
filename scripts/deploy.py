from brownie import Lottery, network, config
import scripts.functions as func
import time

account = func.get_account()

def deploy():
    sub_id = config["chainlink"]["subscription_id"]
    price_feed = func.get_contract("eth_usd_price_feed")
    keyhash = config["networks"][network.show_active()]["keyhash"]
    vrf_coordinator = func.get_contract('vrf_coordinator')
    entrance_fee = 50
    contract = Lottery.deploy(sub_id, price_feed, vrf_coordinator, keyhash, entrance_fee, {"from": account}, publish_source=func.get_verify())
    print("Deployed")
    return contract

def start():
    contract = Lottery[-1]
    txn = contract.startLottery({"from": account})
    txn.wait(1)
    print("IT HAS BEGUN!!!")

def enter():
    contract = Lottery[-1]
    entrance_fee = contract.getEntranceFee() + 100000
    txn = contract.enter({"from": account, "value": entrance_fee})
    txn.wait(1)
    print(f"You have entered the lottery with $50")

def end():
    contract = Lottery[-1]
    txn = contract.endLottery({"from": account})
    txn.wait(1)
    time.sleep(60)
    print("Lottery ended!")
    print(f"{contract.winner()} is the new Winner!")


def main():
    deploy()
    start()
    enter()
    end()