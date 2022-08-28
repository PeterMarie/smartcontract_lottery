from brownie import network, accounts, VRFCoordinatorV2Mock, ExampleContract
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def useVRFMockV2():
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        account = accounts[0]
        VRF_contract = VRFCoordinatorV2Mock.deploy(25000000000000000, 1000000000, {"from": account})

        sub_id_txn = VRF_contract.createSubscription({"from": account})
        sub_id_txn.wait(1)
        sub_id = sub_id_txn.events["SubscriptionCreated"]["subId"]
        fund_amount_link = 3000000000000000000
        fund_vrf_txn = VRF_contract.fundSubscription(sub_id, fund_amount_link, {"from": account})

        keyhash = "0x79d3d8832d904592c0bf9818b621522c988bb8b0c05cdc3b15aea1b6e8db0c15" #goerli_keyhash
        minReqConf = 3 #MinimumRequestConfirmations
        gasLim = 1000000 #callbackGasLimit
        numwords = 1
        make_request_txn = VRF_contract.requestRandomWords(keyhash, sub_id, minReqConf, gasLim, numwords, {"from": account})
        make_request_txn.wait(1)
        requestID = make_request_txn.events["RandomWordsRequested"]["requestId"]

        contract = ExampleContract.deploy(VRF_contract.address, {"from": account}) #Change this line to YOUR contract
        fulfill_txn = VRF_contract.fulfillRandomWords(requestID, contract.address, {"from": account})
        fulfill_txn.wait(1)
        success = fulfill_txn.events["RandomWordsFulfilled"]["success"]
        print(f"Success is {success}")
        if(success):
            randomWord = contract.s_randomWords(0)
            print(f"Random number is {randomWord}")

def main():
    useVRFMockV2()
    