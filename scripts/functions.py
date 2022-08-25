from re import S
from unittest import mock
from brownie import accounts, network, config, Contract, MockV3Aggregator, VRFCoordinatorV2Mock
from web3 import Web3

DECIMALS = 8
STARTING_VALUE = 200000000000
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorV2Mock
}

def get_account(index=None, id=None):
    if(index):
        return accounts[index]
    if(id):
        return accounts.load(id)
    if((network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS) or (network.show_active() in FORKED_LOCAL_ENVIRONMENTS)):
        return accounts[0]
    
    #default account
    return accounts.add(config["wallets"]["from_key"])

def deploy_mocks(contract_name):
    account = get_account()
    contract_type = contract_to_mock[contract_name]
    match contract_name:
        case 'eth_usd_price_feed':
            contract_type.deploy(DECIMALS, STARTING_VALUE, {"from": account})
        case _:
            pass

def get_contract(contract_name):
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        contract_type = contract_to_mock[contract_name]
        print(len(contract_type))
        if(len(contract_type) <= 0):
            print("Deploying...")
            deploy_mocks(contract_name)
            return contract_type[-1]
        return contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
        return contract

def get_price_feed():
    contract_name = "eth_usd_price_feed" 
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        return config["networks"][network.show_active()][contract_name]
    else:
        contract = get_contract(contract_name)
        return contract.address
  

def get_verify():
    return config["networks"][network.show_active()].get("verify")

def get_vrf_variables():
    return config["chainlink"]

