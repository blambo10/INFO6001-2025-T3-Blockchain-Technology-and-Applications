import hashlib
import time
import asyncio
import logging
from utils import sha256
from const import (GENESIS_BLOCK_DATA,
                   GENESIS_BLOCK_PREVIOUS_HASH_INPUT)

log = logging

#TODO: debug why the second hash is not respecting the difficulty, then clean up the code
#Blockchain validity: None
# Block 0 | Hash: e658f2002f88a83ad3c24f97e58054f987ac2471fbe88fe76c87857ddf916a04 | Previous Hash: 5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9
# Block 1 | Hash: 000081b8103b1539bd4c165dd50b630d27414ea3c8f3505fb7220887d0ff45eb | Previous Hash: e658f2002f88a83ad3c24f97e58054f987ac2471fbe88fe76c87857ddf916a04
# Block 2 | Hash: d44371e328672bbf4f76762af28cb910656a51dcb681d25bc890bb9ac397fe3a | Previous Hash: 000081b8103b1539bd4c165dd50b630d27414ea3c8f3505fb7220887d0ff45eb


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
        try:
            hash_data = f"{self.previous_hash}{self.timestamp}{self.data}{self.proof}"
            return sha256(hash_data)
        except Exception as e:
            msg = f"unable to calculate block has due to the following exception: {e}"
            raise Exception(msg)


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Number of leading zeros required in the hash
        self.miners = 6

    def create_genesis_block(self):
        try:
            index = 0
            proof = 0

            # if len(self.chain) > 0:
            #     msg = 'Blockchain has already been created'
            #     log.info(msg)
            #     return self.get_geneisis_block()

            previous_hash = hashlib.sha256(GENESIS_BLOCK_PREVIOUS_HASH_INPUT.encode('utf-8')).hexdigest()

            return Block(index,
                        previous_hash,
                        int(time.time()),
                        GENESIS_BLOCK_DATA,
                        proof,
                    )

        except Exception as e:
            msg = 'unable to create genesis block due to the following exception: {e}'
            raise Exception(msg)

    def get_geneisis_block(self):
        return self.chain[0]

    def get_latest_block(self):
        try:
            if len(self.chain) > 0:
                return self.chain[len(self.chain) - 1]
            else:
                log.error('Blockchain has not been created')
        except Exception as e:
            msg = f"unable to get latest block due to the following exception: {e}"
            raise Exception(msg)

    def add_block(self, data, proof):
        # TODO: Add a new block to the chain
        # Hint: Set the new block's previous_hash to the hash of the latest block
        current_index = self.chain[len(self.chain) - 1].index + 1

        previous_hash = self.chain[len(self.chain) - 1].hash

        # new_block = {
        #     'index': current_index,
        #     'previous_hash': previous_hash,
        # }
        #
        #
        # new_block = {
        #     'timestamp': int(time.time()),
        #     'data': data,
        # }

        self.chain.append(Block(current_index,
                        previous_hash,
                        int(time.time()),
                        data,
                        proof,
                    )
            )

    async def proof_of_work(self, data, previous_hash, time_stamp):
        # TODO: Implement the proof-of-work algorithm
        # Hint: Increment the proof value until the block's hash starts with the required number of leading zeros
        miner_tasks = [asyncio.create_task(self.mine_block(i,
                                                           data,
                                                           previous_hash,
                                                           time_stamp)) for i in range(self.miners)]
        await asyncio.wait(miner_tasks,
                           return_when=asyncio.FIRST_COMPLETED)

        if len(miner_tasks) == 0:
            msg = f"no miners have generated any usable blocks"
            log.error(msg)

        if not hasattr(miner_tasks[0], 'result'):
            msg = f"Miner task data type is missing result, Block not created"
            log.error(msg)

        proof = miner_tasks[0].result()

        return proof

    def add_data(self, data):
        # TODO: Create a new block with the provided data, perform proof of work, and add it to the chain

        previous_hash = self.chain[len(self.chain)-1].hash
        time_stamp = int(time.time())

        # asyncio.run(self.proof_of_work(data,
        #                                 previous_hash,
        #                                 time_stamp))
        pow_results = asyncio.run(self.proof_of_work(data,
                                        previous_hash,
                                        time_stamp))

        self.add_block(data, pow_results)

    def is_chain_valid(self):
        # TODO: Validate the integrity of the blockchain
        # Hint: Check that each block's hash is correct and that the previous_hash matches the hash of the previous block
        pass

    def _is_valid_proof(self, data, previous_hash, time_stamp, proof):
        difficulty = self.difficulty * '0'
        hash_data = f"{previous_hash}{time_stamp}{data}{proof}"
        proof_hash = sha256(hash_data)
        if proof_hash.startswith(difficulty):
            return True
        else:
            return False

    async def mine_block(self, miner, data, previous_hash, time_stamp):
        valid_proof = False
        proof = 0

        while valid_proof is False:
            if self._is_valid_proof(data, previous_hash, time_stamp, proof):
                break

            proof += 1

        return proof


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