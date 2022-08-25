from brownie import Lottery
import scripts.functions as func

def deploy_lottery():
    account = func.get_account()
    chainlink_variables = func.get_vrf_variables()
    price_feed = func.get_price_feed()
    entrance_fee = 50
    print(f"Price feed: {price_feed}")
    #contract = Lottery.deploy(chainlink_variables["subscription_id"], price_feed, chainlink_variables["vrf_coordinator"], chainlink_variables["keyhash"], entrance_fee, {"from": account})
    #print("Deployed")

def main():
    deploy_lottery()