//  SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

/// @title A title that should describe the contract/interface
/// @author The name of the author
/// @notice Explain to an end user what this does
/// @dev Explain to a developer any extra details

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    mapping(address=>uint) addresstoamountfunded;
    uint public USDEntrance_fee;
    AggregatorV3Interface internal ETHUSDPriceFeed;

    constructor(address _priceFeedAddress) public{
        ETHUSDPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        USDEntrance_fee = 50 * (10**18);
    }

    function startLottery() public {

    }

    function endLottery() public {

    }

    function enter() public payable returns(uint){
        require(msg.value == getEntranceFee(), "Entrance Fee is $50!");
        players.push(payable(msg.sender));

    }

    function getEntranceFee() public returns(uint){
        (, int price, , , ) = ETHUSDPriceFeed.latestRoundData();
        uint adjustedPrice = uint(price) * (10**10);
        uint entranceFeeInUSD = 50 * (10**18);
        uint precision = 1 * (10**18);
        uint entranceFeeInWei = entranceFeeInUSD / adjustedPrice;
        return entranceFeeInWei;
    }
}