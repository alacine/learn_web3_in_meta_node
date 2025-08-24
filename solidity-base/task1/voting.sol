// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Voting {
    mapping(string => int32) private voteCount;
    string[] private candidates;
    address owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "only owner can do");
        _;
    }

    function vote(string memory addr) public {
        voteCount[addr]++;
        candidates.push(addr);
    }

    function getVote(string memory addr) public view returns (int32) {
        return voteCount[addr];
    }

    function resetVote() public {
        for (uint256 i = 0; i < candidates.length; i++) {
            voteCount[candidates[i]] = 0;
        }
    }
}
