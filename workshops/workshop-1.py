import hashlib
import time
import json

BLOCKCHAIN_FILENAME = 'blockchain.json'

def calculate_hash(data):
    return hashlib.sha512(data.encode('utf-8')).hexdigest()

# print(calculate_hash("Blockchain"))

def create_genesis_block():
    genesis_hash_content = '0'
    genesis_message = 'Genesis Block'
    proof_of_value = 0

    genesis_block = {
        'index': 0,
        'timestamp': int(time.time()),
        'previous_hash': calculate_hash(genesis_hash_content),
        'data': genesis_message,
        'proof_of_value': proof_of_value
    }
    return genesis_block

# print(json.dumps(create_genesis_block(), indent=4))

def get_latest_item(items):

    if len(items) > 0:
        return items[len(items)-1]
    else:
        return "List is empty"

# print(get_latest_item([1]))
# print(get_latest_item([]))

def add_entry(chain, new_entry):
    if type(chain) != list:
        raise TypeError("chain must be a list")

    if type(new_entry) != dict:
        raise TypeError("new_entry must be a dict")

    chain.append(new_entry)
    return chain

# blockchain = [{'index': 0,
#                'data': 'Genesis Block'}]
# new_block = {'index': 1, 'data': 'New Block'}

# print(add_entry(blockchain, new_block))

def is_valid_proof(data, proof):
    hash_data = f"{data}{proof}"
    proof_hash = hashlib.sha512(hash_data.encode('utf-8')).hexdigest()
    if proof_hash.startswith('0000'):
        return True
    else:
        return False

# print(is_valid_proof("test", 1234))

def proof_of_work():
    proof = 0
    data = 'test'

    while is_valid_proof(data, proof) is False:
        proof += 1

    return proof

# print(proof_of_work())

def validate_blocks(blocks):
    for i, block in enumerate(blocks):
        if i == 0:
            continue

        if 'previous_hash' not in block:
            return False

        if 'hash' not in blocks[i-1]:
            return False

        if block['previous_hash'] != blocks[i-1]['hash']:
            return False

    return True

# blockchain = [
#     {"index": 0, "hash": "abcd"},
#     {"index": 1, "previous_hash": "abcd", "hash": "efgh"},
#     {"index": 2, "previous_hash": "efgh", "hash": "ijkl"}
# ]
# print(validate_blocks(blockchain))

def save_blockchain(blockchain, filename):
    formatted_json = json.dumps(blockchain, indent=4)

    with open(filename, 'w') as file:
        file.write(formatted_json)

def load_blockchain(filename):
    try:
        with open(filename, 'r') as file:
            blockchain = json.loads(file.read())
        return blockchain
    except FileNotFoundError:
        return None

# blockchain = [{"index": 0, "data": "Genesis Block"}]
# save_blockchain(blockchain, "blockchain.json")
# print(load_blockchain("blockchain.json"))

# Blockchain Menu Example
print("\n=== Blockchain Menu ===")
print("1. Create blockchain")
print("2. Add a new block")
print("3. Get Latest Block")
print("4. Display the blockchain")
print("5. Validate the blockchain")
print("6. Exit")

user_input = input()

blockchain = []

match user_input:
    case '1':
        blockchain = load_blockchain(BLOCKCHAIN_FILENAME)
        if blockchain is None:
            blockchain = create_genesis_block()
            save_blockchain([blockchain], BLOCKCHAIN_FILENAME)
        else:
            print(f"{BLOCKCHAIN_FILENAME} already exists")
    case '2':
        blockchain = load_blockchain(BLOCKCHAIN_FILENAME)
        if blockchain is None:
            print(f"{BLOCKCHAIN_FILENAME} not found")
            exit(2)
        new_block = {'index': 1, 'data': 'New Block'}
        add_entry(blockchain, new_block)
        save_blockchain(blockchain, BLOCKCHAIN_FILENAME)
    case '3':
        blockchain = load_blockchain(BLOCKCHAIN_FILENAME)
        if blockchain == None:
            print(f"{BLOCKCHAIN_FILENAME} not found")
            exit(2)

        print(get_latest_item(blockchain))
    case '4':
        blockchain = load_blockchain(BLOCKCHAIN_FILENAME)
        if blockchain == None:
            print(f"{BLOCKCHAIN_FILENAME} not found")
            exit(2)

        print(json.dumps(blockchain, indent=4))
    case '5':
        blockchain = load_blockchain(BLOCKCHAIN_FILENAME)
        if blockchain == None:
            print(f"{BLOCKCHAIN_FILENAME} not found")
            exit(2)

        print(validate_blocks(blockchain))
    case '6':
        print('Exiting')
        exit(0)
    case _:  # The underscore acts as a wildcard, similar to a default case
        print('Invalid input')