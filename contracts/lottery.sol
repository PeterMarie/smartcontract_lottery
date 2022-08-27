// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBaseV2, Ownable {
    
    address payable[] public players;
    mapping(address=>uint) public senderaddresstoamontvalue;
    uint public USDEntrance_fee;
    AggregatorV3Interface internal ETHUSDPriceFeed;
    bytes32 public keyHash;
    address payable public winner;

    VRFCoordinatorV2Interface COORDINATOR;
    uint64 s_subscriptionId = 396;
    uint16 requestConfirmations = 3;
    uint32 callbackGasLimit = 100000;
    uint32 numWords = 2;
    uint public s_requestId;
    uint256[] public s_randomWords;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    event requestedRandomWords(uint requestId);

  constructor(
        uint64 subscriptionId,
        address _priceFeedAddress,
        address _VRFCoordinator,
        bytes32 _keyhash,
        uint _entrance_fee
    ) VRFConsumerBaseV2(_VRFCoordinator) {
        COORDINATOR = VRFCoordinatorV2Interface(_VRFCoordinator);
        s_subscriptionId = subscriptionId;
        ETHUSDPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        USDEntrance_fee = _entrance_fee * (10**18);
        keyHash = _keyhash;
        lottery_state = LOTTERY_STATE.CLOSED;
  }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "One Lottery Contract has already been opened!");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.OPEN, "One Lottery Contract has already been opened!");
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        requestRandomWords();
        emit requestedRandomWords(s_requestId);
    }

  // Assumes the subscription is funded sufficiently.
  function requestRandomWords() public onlyOwner {
    // Will revert if subscription is not set and funded.
    s_requestId = COORDINATOR.requestRandomWords(
      keyHash,
      s_subscriptionId,
      requestConfirmations,
      callbackGasLimit,
      numWords
    );
  }

  function fulfillRandomWords(
    uint256, /* requestId */
    uint256[] memory randomWords
  ) internal override {
    s_randomWords = randomWords;
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "Not yet time");
        require(randomWords.length > 0, "Randomness incorrect");
        uint indexOfWinner = randomWords[0] % players.length;
        winner = players[indexOfWinner];
        winner.transfer(address(this).balance);
        players = new address payable[](0);
        for (uint i = 0; i < players.length; i++){
          address player = players[i];
          delete senderaddresstoamontvalue[player];
        }
        lottery_state = LOTTERY_STATE.CLOSED;
  }
  
    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery is NOT open");
        require(msg.value >= getEntranceFee(), "Entrance Fee is $50!");
        players.push(payable(msg.sender));
        senderaddresstoamontvalue[msg.sender] += msg.value;
    }

    function getEntranceFee() public view returns(uint){
        (, int price, , , ) = ETHUSDPriceFeed.latestRoundData();
        uint adjustedPrice = uint(price) * (10**10);
        uint precision = 1 * (10**18);
        uint entranceFeeInWei = (USDEntrance_fee * precision) / adjustedPrice;
        return entranceFeeInWei;
    }
    
    function resetLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CLOSED;
        //return money to entrants
        for(uint i = 0; i < players.length; i++){
          address payable player = players[i];
          player.transfer(senderaddresstoamontvalue[player]);
          delete senderaddresstoamontvalue[player];
        }
        players = new address payable[](0);
    }
}

