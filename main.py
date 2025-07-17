import logging

from blockchain.base import Blockchain
from user_interface.base import UserInterface

log = logging


def main():

    try:
        selection = 0
        ui = UserInterface()
        blockchain = Blockchain()

        while selection is not ui.EXIT:
            selection = ui.menu()
            ui.process_input(selection, blockchain)
    except Exception as e:
        msg = f'blockchain application ended due to the following: {e}'
        log.error(msg)


if __name__ == "__main__":
    main()
