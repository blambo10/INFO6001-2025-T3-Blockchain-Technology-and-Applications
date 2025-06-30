import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # TODO: Implement the hash calculation for the block
        # Hint: Combine all block attributes into a string and hash it using SHA-256
        pass


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Number of leading zeros required in the hash

    def create_genesis_block(self):
        # TODO: Create and return the genesis block (the first block in the chain)
        pass

    def get_latest_block(self):
        # TODO: Return the latest block in the chain
        pass

    def add_block(self, new_block):
        # TODO: Add a new block to the chain
        # Hint: Set the new block's previous_hash to the hash of the latest block
        pass

    def proof_of_work(self, block):
        # TODO: Implement the proof-of-work algorithm
        # Hint: Increment the proof value until the block's hash starts with the required number of leading zeros
        pass

    def add_data(self, data):
        # TODO: Create a new block with the provided data, perform proof of work, and add it to the chain
        pass

    def is_chain_valid(self):
        # TODO: Validate the integrity of the blockchain
        # Hint: Check that each block's hash is correct and that the previous_hash matches the hash of the previous block
        pass


# Example Usage
if __name__ == "__main__":
    blockchain = Blockchain()

    print("Mining block 1...")
    blockchain.add_data("Transaction data for Block 1")

    print("Mining block 2...")
    blockchain.add_data("Transaction data for Block 2")

    print("\nBlockchain validity:", blockchain.is_chain_valid())

    for block in blockchain.chain:
        print(f"Block {block.index} | Hash: {block.hash} | Previous Hash: {block.previous_hash}")