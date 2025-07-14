import hashlib
import time
import asyncio
import logging
from utils import sha256
from const import (GENESIS_BLOCK_DATA,
                   GENESIS_BLOCK_PREVIOUS_HASH_INPUT)

log = logging

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        try:
            hash_data = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.proof}"
            return sha256(hash_data)
        except Exception as e:
            msg = f"unable to calculate block hash: {e}"
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

    def add_block(self, index, previous_hash, time_stamp, data, proof):

        self.chain.append(Block(index,
                                previous_hash,
                                time_stamp,
                                data,
                                proof,
                            )
                        )

    async def proof_of_work(self, index, previous_hash, time_stamp, data):
        miner_tasks = [asyncio.create_task(self.mine_block(index,
                                                           previous_hash,
                                                           time_stamp,
                                                           data)) for i in range(self.miners)]
        await asyncio.wait(miner_tasks,
                           return_when=asyncio.FIRST_COMPLETED)

        if len(miner_tasks) == 0:
            msg = f"no miners have generated any usable blocks"
            raise Exception(msg)

        if not hasattr(miner_tasks[0], 'result'):
            msg = f"miner task data type is missing result, Block not created"
            raise Exception(msg)

        proof = miner_tasks[0].result()

        return proof

    def add_data(self, data):
        try:
            index = self.chain[len(self.chain) - 1].index + 1
            previous_hash = self.chain[len(self.chain)-1].hash
            time_stamp = int(time.time())

            proof = asyncio.run(self.proof_of_work(index,
                                                   previous_hash,
                                            time_stamp,
                                            data))

            self.add_block(index, previous_hash, time_stamp, data, proof)
        except Exception as e:
            log.error(f"unable to add data to block: {e}")

    def is_chain_valid(self):
        try:
            for i, block in enumerate(self.chain):
                if i == 0:
                    continue

                if not hasattr(block, 'previous_hash'):
                    return False

                if not hasattr(self.chain[i - 1], 'hash'):
                    return False

                if block.previous_hash != self.chain[i - 1].hash:
                    return False

            return True
        except Exception as e:
            log.error(f"unable to validate chain: {e}")
            return False

    async def mine_block(self, index, previous_hash, time_stamp, data):
        valid_proof = False
        proof = 0

        while valid_proof is False:
            if self.is_valid_proof(index, previous_hash, time_stamp, data, proof):
                valid_proof = True
            else:
                proof += 1

        return proof

    def is_valid_proof(self, index, previous_hash, time_stamp, data, proof):
        difficulty = self.difficulty * '0'
        hash_data = f"{index}{previous_hash}{time_stamp}{data}{proof}"

        proof_hash = sha256(hash_data)
        if proof_hash.startswith(difficulty):
            return True
        else:
            return False

# Example Usage
if __name__ == "__main__":
    blockchain = Blockchain()

    print("Mining block 1...")
    blockchain.add_data("Transaction data for Block 1")

    print("Mining block 2...")
    blockchain.add_data("Transaction data for Block 2")

    print("\nBlockchain validity:", blockchain.is_chain_valid())

    for block in blockchain.chain:
        print(f"Block {block.index} | Hash: {block.hash} | Previous Hash: {block.previous_hash} | Timestamp: {block.timestamp} | data: {block.data} | Proof: {block.proof}")