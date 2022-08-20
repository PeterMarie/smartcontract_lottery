from re import S
from unittest import mock
from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_VALUE = 200000000000
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account():
    if((network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS) or (network.show_active() in FORKED_LOCAL_ENVIRONMENTS)):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    account = get_account()
    if(len(MockV3Aggregator) <= 0):
        print("Deploying Mocks...")
        mock_pricefeed_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_VALUE, {"from": account}
        )
        print("Deployed!")
    return MockV3Aggregator[-1].address

def get_price_feed(account):
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        return config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        mock_address = deploy_mocks()
        return mock_address

def get_verify():
    return config["networks"][network.show_active()].get("verify")
