import hashlib
import time
import json
import asyncio
import logging
from utils import sha256
from blockchain.const import (GENESIS_BLOCK_DATA,
                              GENESIS_BLOCK_PREVIOUS_HASH_INPUT)

log = logging


class Block:

    def __init__(self,
                 index,
                 previous_hash,
                 timestamp,
                 data,
                 proof,
                 hash=None):

        """Create a new Block
           The hash for the block will be generated automatically
           unless the hash is explicitly specified,
           the use case for this is if a blockchain is
           loaded back in from a file.

        Returns:
            string: The calculated hash of all attributes of
                    the block including nonce (proof)

        Raises:
            Exception: If hash calculation fails.
        """

        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof

        # Allow for hash to be specified in the
        # event of loading blockchain back from file,
        # instead of performing hash compute on every re-entry
        if hash is None:
            self.hash = self.calculate_hash()
        else:
            self.hash = hash

    def calculate_hash(self):
        """Calculates block hash.

        Returns:
            string: The calculated hash of all attributes
                    of the block including nonce (proof)

        Raises:
            Exception: If hash calculation fails.
        """
        try:
            hash_data = (f"{self.index}{self.previous_hash}"
                         f"{self.timestamp}{self.data}{self.proof}")
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
        """Create the genesis block in the blockchain.

        Returns:
            string: The generated genesis block

        Raises:
            Exception: If block creation fails.
        """

        try:
            index = 0
            proof = 0

            previous_hash = (hashlib.sha256(
                             GENESIS_BLOCK_PREVIOUS_HASH_INPUT
                             .encode('utf-8'))
                             .hexdigest())

            return Block(index,
                         previous_hash,
                         int(time.time()),
                         GENESIS_BLOCK_DATA,
                         proof)

        except Exception as e:
            msg = (f'unable to create genesis block '
                   f'due to the following exception: {e}')
            raise Exception(msg)

    def get_geneisis_block(self):
        """Get the genesis block in the blockchain.

        Returns:
            string: The generated genesis block

        Raises:
            Exception: If block creation fails.
        """
        return self.chain[0].__dict__

    def get_latest_block(self):
        """Gets the latest block in the blockchain.

        Returns:
            dict: The latest block from the blockchain

        Raises:
            Exception: If fails to find the latest block.
        """

        try:
            if len(self.chain) > 0:
                block = self.chain[len(self.chain) - 1]
                return block
            else:
                log.error('blockchain has not been created')
        except Exception as e:
            msg = (f"unable to get latest block "
                   f"due to the following exception: {e}")
            raise Exception(msg)

    def get_blockchain_json(self):
        """Gets the entire blockchain.

        Returns:
            dict: blockchain in json format

        Raises:
            Exception: if blockchain doesnt exist.
        """
        try:
            if len(self.chain) > 0:
                blockchain = []
                for block in self.chain:
                    blockchain.append(block.__dict__)

                return blockchain

            else:
                msg = 'blockchain has not been created'
                raise Exception(msg)
        except Exception as e:
            msg = (f"unable to get blockchain "
                   f"due to the following exception: {e}")
            raise Exception(msg)

    def get_blockchain(self):
        """Gets the entire blockchain.

        Returns:
            Blockchain: blockchain

        Raises:
            Exception: if blockchain doesnt exist.
        """
        try:
            if len(self.chain) > 0:
                return self.chain
            else:
                msg = 'blockchain has not been created'
                raise Exception(msg)
        except Exception as e:
            msg = (f"unable to get blockchain "
                   f"due to the following exception: {e}")
            raise Exception(msg)

    def add_block(self,
                  index,
                  previous_hash,
                  time_stamp,
                  data, proof,
                  hash=None):
        """Add block to the blockchain.

        Args:
            index (int): The length of the rectangle.
            previous_hash (str): The width of the rectangle.
            time_stamp (int): The width of the rectangle.
            data (str): The width of the rectangle.
            proof (int): The width of the rectangle.
        """

        self.chain.append(Block(index,
                                previous_hash,
                                time_stamp,
                                data,
                                proof,
                                hash=hash))

    async def proof_of_work(self, index, previous_hash, time_stamp, data):
        """Proof of work algorithm,
           where orchestration of the asynchronous miners is managed

        Args:
            index (int): The length of the rectangle.
            previous_hash (str): The width of the rectangle.
            time_stamp (int): The width of the rectangle.
            data (str): The width of the rectangle.

        Returns:
            int: nonce which has been mined and
                 found to generate hash with appropriate difficulty

        Raises:
            Exception: if unable to generate nonce
        """
        try:
            miner_tasks = [
                asyncio.create_task(self.mine_block(index,
                                    previous_hash,
                                    time_stamp,
                                    data)) for i in range(self.miners)]

            await asyncio.wait(miner_tasks,
                               return_when=asyncio.FIRST_COMPLETED)

            if len(miner_tasks) == 0:
                msg = "no miners have generated any usable blocks"
                raise Exception(msg)

            if not hasattr(miner_tasks[0], 'result'):
                msg = ("miner task data type is missing result, "
                       "Block not created")
                raise Exception(msg)

            proof = miner_tasks[0].result()

            return proof
        except Exception as e:
            msg = (f"unable to generate nonce for the blockchain "
                   f"due to the following exception: {e}")
            raise Exception(msg)

    def add_data(self, data):
        """Add data which is used along with
           nonce to then create and add block to blockchain.

        Args:
            data (str): The width of the rectangle.

        Returns:
            bool: indicating if the data is used and
                  block generated successfully adds blockchain.

        Raises:
            Exception: if unable to mine nonce,
                       create block or add block to blockchain.
        """
        try:
            index = self.chain[len(self.chain) - 1].index + 1
            previous_hash = self.chain[len(self.chain) - 1].hash
            time_stamp = int(time.time())

            proof = asyncio.run(self.proof_of_work(index,
                                                   previous_hash,
                                                   time_stamp,
                                                   data))

            self.add_block(index, previous_hash, time_stamp, data, proof)
            return True
        except Exception as e:
            log.error(f"unable to add data to block: {e}")
            return False

    def is_chain_valid(self):
        """Validates blockchain by iterating blocks
           and ensuring referencial integrity,
           achieved by comparing current blocks
           'previous_hash' and previous blocks 'hash'.

        Returns:
            bool: if data is used and block
                  generated successfully adds blockchain.

        Raises:
            Exception: if unable to mine nonce,
                       create block or add block to blockchain.
        """
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
        """Mine for a valid nonce using block header attributes

        Returns:
            int: nonce used to generate valid hash

        Raises:
            Exception: if unable to mine nonce.
        """
        valid_proof = False
        proof = 0

        while valid_proof is False:
            if self.is_valid_proof(index,
                                   previous_hash,
                                   time_stamp,
                                   data,
                                   proof):
                valid_proof = True
            else:
                proof += 1

        return proof

    def is_valid_proof(self, index, previous_hash, time_stamp, data, proof):
        """Validates the nonce using block header attributes,
           nonce is incremented by 1 until it combined
           with other attributes generate a hash that matches the difficulty.

        Returns:
            bool: indicates if current nonce is
                  valid in conjunction with block header data.
        """
        difficulty = self.difficulty * '0'
        hash_data = f"{index}{previous_hash}{time_stamp}{data}{proof}"

        proof_hash = sha256(hash_data)
        if proof_hash.startswith(difficulty):
            return True
        else:
            return False

    def save_blockchain(self, filename):
        """Saves the current blockchain in memory to filename specified.
        """
        try:
            formatted_json = json.dumps(self.get_blockchain_json(), indent=4)

            with open(filename, 'w') as file:
                file.write(formatted_json)

            print(f'\nSaved blockchain to {filename} Successfully!')
        except Exception as e:
            msg = (f"unable to save blockchain to filename: {filename}"
                   f" due to the following exception: {e}")
            log.error(msg)

    def load_blockchain(self, filename):
        """Loads blockchain from filename specified into memory,
           Overwriting blockchain in self.chain.
        """
        try:
            original_blockchain = self.chain
            new_blockchain = None

            self.chain = []

            with open(filename, 'r') as file:
                new_blockchain = json.loads(file.read())

            for block in new_blockchain:
                self.add_block(block['index'],
                               block['previous_hash'],
                               block['timestamp'],
                               block['data'],
                               block['proof'],
                               hash=block['hash'])

            if not self.is_chain_valid():
                self.chain = original_blockchain
                log.error(f"unable to validate chain {filename} - "
                          "reverted to original chain")
            else:
                print(f'\nLoaded blockchain from file {filename} Successfully!')

        except Exception as e:
            msg = (f"unable to load blockchain from filename: {filename}"
                   f" due to the following exception: {e}")
            log.error(msg)
