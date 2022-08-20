from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_entrance_fee():
    account = accounts[0]
    contract = Lottery.deploy(config["networks"][network.show_active()]['eth_usd_price_feed'], {"from": account})
    entrance_fee = contract.getEntranceFee()
    print(entrance_fee)
    least_expected = Web3.toWei(0.02, 'ether')
    most_expected = Web3.toWei(0.04, 'ether')
    assert entrance_fee > least_expected
    assert entrance_fee < most_expected