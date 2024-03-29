import json
from solcx import compile_standard
from web3 import Web3
import os
from dotenv import load_dotenv

# solcx.install_solc("0.8.11")
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.11",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#  Get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#  Connecting to ganache
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/b28a4ca8f39649ebbdfa6ff609765909")
)
chain_id = 4
my_address = "0xde7480E66AFF1E32EA141ed15cb88aF1fB98E0Cb"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
gas_price = w3.eth.gas_price

print("Deploying contract...")

# 1. Build a transaction
# 2. Sign the transaction
# 3. Send the transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce, "gasPrice": gas_price}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_recipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Contract successfully deployed....")

# Working with the contrct
#  We need two things to work with a contract
# 1. Contract Address
# 2. Contract ABI
simple_storage = w3.eth.contract(address=txn_recipt.contractAddress, abi=abi)

# We can interact with functions in the contract with
# Call -> To simulate making a call and getting a return value (do not make a state change)
# Transact -> To actually make a state change

# Initial vaklue of favorite number
print(
    "Initial value of favoriteNumber:" + str(simple_storage.functions.retrieve().call())
)
print("Initiating store() transaction...")
store_tx = simple_storage.functions.store(19000).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1, "gasPrice": gas_price}
)
signed_store_tx = w3.eth.account.sign_transaction(store_tx, private_key=private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
store_txn_recipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)
print(
    "Updated value of favoriteNumber:" + str(simple_storage.functions.retrieve().call())
)
