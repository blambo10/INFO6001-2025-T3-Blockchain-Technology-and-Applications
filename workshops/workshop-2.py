import hashlib
import time
import asyncio

# Compute Merkle Root using recursion

def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def compute_merkle_root(transactions):

    if len(transactions) % 2 != 0:
        transactions.append(transactions[-1])

    root = hash_transactions(transactions)

    return root

def hash_transactions(transactions):
    if len(transactions) == 1:
        return transactions

    if len(transactions) >= 2:
        first_hash = str(sha256(transactions[0]))
        second_hash = str(sha256(transactions[1]))
        transactions.append(f"{first_hash}{second_hash}")
        transactions.pop(0)
        transactions.pop(1)

    root = hash_transactions(transactions)
    return root

# Example Usage
tnx = [
    "Transaction A",
    "Transaction B",
    "Transaction C",
    "Transaction D"
]

# merkle_root = compute_merkle_root(tnx)
# print("Merkle Root:", merkle_root)

# Simulate Proof Of Work

async def is_valid_proof(data, proof, difficulty):
    hash_data = f"{data}{proof}"
    proof_hash = sha256(hash_data)
    if proof_hash.startswith(difficulty):
        return True
    else:
        return False

async def mine_block(miner, block_data, difficulty):
    """TODO: Simulate mining by finding a nonce that satisfies the difficulty."""
    difficulty = difficulty * '0'
    start_time = time.perf_counter()
    valid_proof = False
    nonce = 0

    while valid_proof is False:
        print('checking for valid proof')
        if is_valid_proof(block_data, nonce, difficulty):
            print('found valid proof')
            break

        nonce += 1

    hash_data = f"{block_data}{nonce}"
    current_hash = sha256(hash_data)

    end_time = time.perf_counter()
    time_taken = end_time - start_time

    return [miner, nonce, current_hash, time_taken]


async def simulate_pow(miners, block_data, difficulty):
    """TODO: Simulate Proof of Work with multiple miners."""

    # create all tasks
    working_miners = [asyncio.create_task(mine_block(i, block_data, difficulty)) for i in range(miners)]
    # wait for all tasks to complete concurrently
    await asyncio.wait(working_miners)

    print(working_miners)
    print(working_miners[0].result())
    # exit(0)

    working_miners.sort(key=lambda miner: miner.result()[3])

    winner = working_miners[0].result()

    print(f"\nMiner {winner[0]} found the solution first!")
    print(f"Nonce: {winner[1]}")
    print(f"Block Hash: {winner[2]}")
    print(f"Time Taken: {winner[3]:.2f} seconds")

# Example Usage
miners = 5  # Number of miners
block_data = "Block Data"  # Data to be included in the block
difficulty = 4  # Number of leading zeros required

asyncio.run(simulate_pow(miners, block_data, difficulty))