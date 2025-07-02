import hashlib
import time
import json
import re

BLOCKCHAIN_FILENAME = 'blockchain.json'

def calculate_hash(data):
    return hashlib.sha512(data.encode('utf-8')).hexdigest()

def create_genesis_block():
    genesis_previous_hash_data = calculate_hash('0')
    time_stamp = int(time.time())
    genesis_data = 'Genesis Block'
    proof_of_value = 0
    hash_data = f"{genesis_previous_hash_data}{time_stamp}{genesis_data}{str(proof_of_value)}"
    block_hash = calculate_hash(hash_data)

    genesis_block = {
        'index': 0,
        'timestamp': int(time.time()),
        'previous_hash': calculate_hash(genesis_previous_hash_data),
        'hash': block_hash,
        'data': genesis_data,
        'proof_of_value': proof_of_value
    }
    return genesis_block

# print(json.dumps(create_genesis_block(), indent=4))

def get_latest_item(items):

    if len(items) > 0:
        return items[len(items)-1]
    else:
        return "List is empty"

def add_entry(blockchain, new_block):
    if type(blockchain) != list:
        raise TypeError("chain must be a list")

    if type(new_block) != dict:
        raise TypeError("new_entry must be a dict")

    current_index = blockchain[-1]['index'] + 1

    previous_hash = blockchain[-1]['hash']

    proof_of_value, current_hash = get_proof_of_work(new_block['data'],
                                            [block['proof_of_value'] for block in blockchain])

    new_block_enriched = {
        'index': current_index,
        'timestamp': int(time.time()),
        'previous_hash': previous_hash,
        'hash': current_hash,
        'proof_of_value': proof_of_value,
        **new_block
    }

    blockchain.append(new_block_enriched)
    return blockchain

def is_valid_proof(data, proof):
    hash_data = f"{data}{proof}"
    proof_hash = calculate_hash(hash_data)
    if proof_hash.startswith('0000'):
        return True
    else:
        return False

def get_proof_of_work(data, existing_proof_of_values = []):
    valid_proof = False

    if len(existing_proof_of_values) > 0:
        proof_value = existing_proof_of_values[len(existing_proof_of_values)-1] + 1
        #TODO: continue here
    else:
        proof_value = 0

    while valid_proof is False:
        print('checking for valid proof')
        if is_valid_proof(data, proof_value) and proof_value not in existing_proof_of_values:
            print('found valid proof')
            break

        proof_value += 1

    hash_data = f"{data}{proof_value}"
    current_hash = calculate_hash(hash_data)

    return proof_value, current_hash

def validate_blocks(blockchain):
    for i, block in enumerate(blockchain):
        if i == 0:
            continue

        if 'previous_hash' not in block:
            return False

        if 'hash' not in blockchain[i-1]:
            return False

        if block['previous_hash'] != blockchain[i-1]['hash']:
            return False

    return True

def calculate_chain_difficulty(blockchain):
    regex = '^0+'
    total_sum = 0
    blockchain_hash_zeros = []

    for block in blockchain:

        search = re.search(regex, block['hash'])

        if search:
            leading_zeros_count = len(search.group(0))
            total_sum += leading_zeros_count
            blockchain_hash_zeros.append(leading_zeros_count)

    return total_sum / len(blockchain_hash_zeros)

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

# Blockchain Menu Example
print("\n=== Blockchain Menu ===")
print("1. Create blockchain")
print("2. Add a new block")
print("3. Get Latest Block")
print("4. Display the blockchain")
print("5. Validate the blockchain")
print("6. Check difficulty")
print("7. Exit")

user_input = input()

blockchain = []

#todo: add logic that adds the hash and previous hash to the block
# also add logic that checks for the index

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
        new_block = {'data': 'New Block'}
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
        blockchain = load_blockchain(BLOCKCHAIN_FILENAME)
        if blockchain == None:
            print(f"{BLOCKCHAIN_FILENAME} not found")
            exit(2)

        print(calculate_chain_difficulty(blockchain))
    case '7':
        print('Exiting')
        exit(0)
    case _:  # The underscore acts as a wildcard, similar to a default case
        print('Invalid input')