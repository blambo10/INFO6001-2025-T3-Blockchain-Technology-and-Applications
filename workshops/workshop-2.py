from collections import Counter
import hashlib
import time
import asyncio
import logging
import random
import json

log = logging

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

# Simulate Proof Of Work

def is_valid_proof(data, proof, difficulty):
    hash_data = f"{data}{proof}"
    proof_hash = sha256(hash_data)
    if proof_hash.startswith(difficulty):
        return True
    else:
        return False

async def mine_block(miner, block_data, difficulty):
    """TODO: ¸Simulate mining by finding a nonce that satisfies the difficulty."""
    difficulty = difficulty * '0'
    start_time = time.perf_counter()
    valid_proof = False
    nonce = 0

    while valid_proof is False:
        if is_valid_proof(block_data, nonce, difficulty):
            break

        nonce += 1

    hash_data = f"{block_data}{nonce}"
    current_hash = sha256(hash_data)

    end_time = time.perf_counter()
    time_taken = end_time - start_time

    current_epoch_time = time.time()
    return [miner, nonce, current_hash, current_epoch_time]


async def simulate_pow(miners, block_data, difficulty):

    start_time = time.perf_counter()

    # log.info(f"Simulating Proof of Work - Starting {miners} Blockchain Miners")
    print(f"Simulating Proof of Work")
    print(f"Starting {miners} Blockchain Miners")
    print(f"Difficulty: {difficulty}")
    print(f"Block Data: {block_data}")

    working_miners = [asyncio.create_task(mine_block(i, block_data, difficulty)) for i in range(miners)]
    await asyncio.wait(working_miners)

    working_miners.sort(key=lambda miner: miner.result()[3])

    winner = working_miners[0].result()

    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"\nMiner {winner[0]} found the solution first!")
    print(f"Nonce: {winner[1]}")
    print(f"Block Hash: {winner[2]}")
    print(f"Time Finished: {winner[3]:.2f} seconds")
    # print(f"Finish time: {winner[4]} seconds")

    print(f"Finish time of slower other miners: {working_miners[1].result()[3]} {working_miners[2].result()[3]} {working_miners[3].result()[3]}")

    print(f"overall time taken {time_taken}")

# Simulate Proof Of Stake

TOTAL_TOKENS = 5000

def get_validators_stakes(validators):
    for i, validator in enumerate(validators):
        # print(validator)
        stake = (validators[validator] / TOTAL_TOKENS) * 100
        print(stake)
        validators[validator] = stake

def select_validator(validators):
    selected_validator = random.choices(list(validators.keys()),
                                        weights=validators.values(),
                                        k=1)[0]
    return selected_validator

def simulate_pos(validators):
    start_time = time.perf_counter()
    get_validators_stakes(validators)
    selected_validator = select_validator(validators)
    end_time = time.perf_counter()

    time_taken = end_time - start_time

    print("Validators and their stakes:")
    print(json.dumps(validators, indent=4))

    print(f"\nValidator {selected_validator} has been chosen to create the next block!")

    print(f"Overall Time Taken: {time_taken}")


# Simulate DPoS

def collect_votes(token_holders, delegate_choices):
    """
    Allow token holders to vote for delegates.
    Returns a dictionary mapping each token holder to their chosen delegate.
    """
    votes = {}

    for token_holder in token_holders:
        votes[token_holder] = random.choice(delegate_choices)

    return votes

def simulate_dpos(votes, num_delegates=3):
    """
    Simulate Delegated Proof of Stake:
    - Count votes.
    - Select top delegates to create blocks.
    """
    delegates = {}

    print(votes)

    for voter, vote in votes.items():
        delegates[vote] = delegates.get(vote, 0) + 1

    delegates = sorted(delegates.items(), key=lambda item: item[1], reverse=True)
    chosen_delegates = delegates[0:num_delegates]

    print(f"\nTop Delegates {chosen_delegates} have been chosen to create the blocks!")

    print(delegates[0:3])

# Compute Merkle Root using recursion

merkle_root = compute_merkle_root(tnx)
print("Merkle Root:", merkle_root)


# Simulate Proof Of Work

miners = 6  # Number of miners
block_data = "Block Data"  # Data to be included in the block
difficulty = 4  # Number of leading zeros required

asyncio.run(simulate_pow(miners, block_data, difficulty))


# Simulate Proof Of Stake

validators = {
    "Alice": 100,
    "Bob": 50,
    "Charlie": 200,
    "Diana": 75
}

simulate_pos(validators)

# Simulate DPoS and select 3 delegates

# Token holders (voters)
token_holders = [
    "Voter1", "Voter2", "Voter3", "Voter4", "Voter5",
    "Voter6", "Voter7", "Voter8", "Voter9", "Voter10"
]

# Candidates for delegate
delegate_candidates = ["Alice", "Bob", "Lee", "Diana"]

# Collect votes randomly for demonstration
votes = collect_votes(token_holders, delegate_candidates)

simulate_dpos(votes, num_delegates=3)