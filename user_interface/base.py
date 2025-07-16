import logging

from user_interface.const import (ADD_NEW_BLOCK,
                                  GET_LATEST_BLOCK,
                                  DISPLAY_BLOCKCHAIN,
                                  VALIDATE_BLOCKCHAIN,
                                  LOAD_BLOCKCHAIN,
                                  SAVE_BLOCKCHAIN,
                                  EXIT)

log = logging


class UserInterface:
    def __init__(self):
        """Create a new UserInterface."""

        self.ADD_NEW_BLOCK = ADD_NEW_BLOCK
        self.GET_LATEST_BLOCK = GET_LATEST_BLOCK
        self.DISPLAY_BLOCKCHAIN = DISPLAY_BLOCKCHAIN
        self.VALIDATE_BLOCKCHAIN = VALIDATE_BLOCKCHAIN
        self.LOAD_BLOCKCHAIN = LOAD_BLOCKCHAIN
        self.SAVE_BLOCKCHAIN = SAVE_BLOCKCHAIN
        self.EXIT = EXIT
        self.menu_prompt = ('\n=== Blockchain Menu (INFO6001-2025-T3) ===\n'
                            f'{self.ADD_NEW_BLOCK}. '
                            'Add a new block\n'
                            f'{self.GET_LATEST_BLOCK}. '
                            'Get Latest Block\n'
                            f'{self.DISPLAY_BLOCKCHAIN}. '
                            'Get Blockchain\n'
                            f'{self.VALIDATE_BLOCKCHAIN}. '
                            'Validate Blockchain\n'
                            f'{self.LOAD_BLOCKCHAIN}. '
                            'Load Blockchain from file\n'
                            f'{self.SAVE_BLOCKCHAIN}. '
                            'Save Blockchain to file\n'
                            f'{self.EXIT}. Exit\n')

    def menu(self):
        """Display Application Menu and Allow selection

        Returns:
            string: user selection

        Raises:
            Exception: If menu logic fails
        """
        try:
            print(self.menu_prompt)

            user_input = input('Enter your choice: ')

            return user_input
        except Exception as e:
            msg = f'Unable to display menu due to {e}'
            raise Exception(msg)

    def process_input(self, user_input, blockchain):
        """Process user selection from menu

        Args:
            user_input (int): The length of the rectangle.
            blockchain (Blockchain): Blockchain containing list of blocks,
                                     Given python passes list around with
                                     the same behaves as pass by ref,
                                     any operation done to the blockchain
                                     will persist in memory on the
                                     original chain.

        Returns:
            string: user selection

        Raises:
            Exception: If any operations fail
        """
        try:
            empty_blockchain_msg = "Block chain empty not found"

            # [bl] process user selection
            match user_input:
                case self.ADD_NEW_BLOCK:
                    if blockchain is None:
                        raise Exception(empty_blockchain_msg)

                    data = input('Enter new block data: ')

                    if blockchain.add_data(data):
                        print('\nBlock added succesfully')
                    else:
                        print('\nUnable to add new block')
                case self.GET_LATEST_BLOCK:
                    if blockchain is None:
                        raise Exception(empty_blockchain_msg)

                    block = blockchain.get_latest_block()

                    output = (f'Block {block.index} | '
                              f'Hash: {block.hash} | '
                              f'Previous Hash: {block.previous_hash} | '
                              f'Timestamp: {block.timestamp} | '
                              f'data: {block.data} | '
                              f'Proof: {block.proof}')
                    print(output)

                case self.DISPLAY_BLOCKCHAIN:
                    if blockchain is None:
                        raise Exception(empty_blockchain_msg)

                    print('\n')
                    for block in blockchain.get_blockchain():
                        output = (f'Block {block.index} | '
                                  f'Hash: {block.hash} | '
                                  f'Previous Hash: {block.previous_hash} | '
                                  f'Timestamp: {block.timestamp} | '
                                  f'data: {block.data} | '
                                  f'Proof: {block.proof}')
                        print(output)

                case self.VALIDATE_BLOCKCHAIN:
                    if blockchain is None:
                        raise Exception(empty_blockchain_msg)

                    print(blockchain.is_chain_valid())
                case self.LOAD_BLOCKCHAIN:
                    output = ('\n================\n'
                              'Load blockchain\n'
                              '================\n')
                    print(output)
                    filename = input('Enter filename: ')

                    blockchain.load_blockchain(filename)

                case self.SAVE_BLOCKCHAIN:
                    output = ('\n================\n'
                              'Save blockchain\n'
                              '================\n')
                    print(output)
                    filename = input('Enter filename: ')

                    blockchain.save_blockchain(filename)

                case self.EXIT:
                    print('Exiting')
                    exit(0)
                case _:
                    print(user_input)
                    print('Invalid input')
        except Exception as e:
            msg = f'Unable to process selection due to {e}'
            raise Exception(msg)
