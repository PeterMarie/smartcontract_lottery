pragma solidity >=0.6.0 <0.9.0;

/// @title A title that should describe the contract/interface
/// @author The name of the author
/// @notice Explain to an end user what this does
/// @dev Explain to a developer any extra details

contract Lottery {
    address payable[] players;
    mapping(address=>uint) addresstoamountfunded;

    constructor() public{

    }

    function startLottery() public {

    }

    function endLottery() public {

    }

    function enter() public payable returns(uint){

    }

    function getEntranceFee() public returns(uint){

    }
}