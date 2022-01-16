// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <=0.9.0;

contract SimpleStorage {
    uint256 favoriteNumber = 5;

    struct People {
        uint256 favNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public peopleMap;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favNumber: _favoriteNumber, name: _name}));
        peopleMap[_name] = _favoriteNumber;
    }

    function retrievePeople() public view returns (People[] memory) {
        return people;
    }
}
