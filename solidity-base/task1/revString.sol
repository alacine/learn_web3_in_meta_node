// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract RevString {
    function revString(string memory s) public pure returns (string memory) {
        bytes memory bs = bytes(s);
        uint256 len = bs.length;
        bytes memory nbs = new bytes(len);
        for (uint256 i = 0; i < len; i++) {
            nbs[i] = bs[len - 1 - i];
        }
        return string(nbs);
    }
}
