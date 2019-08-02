from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import sys
import time

def main():

    api = LedgerApi('127.0.0.1', 8100)

    print('Generating keys...')

    entity1 = Entity()

    with open('./workdir/transfer/server_private.key', 'w') as private_key_file:
        entity1.dump(private_key_file)

    entity2 = Entity()

    with open('./workdir/transfer/client_private.key', 'w') as private_key_file:
        entity2.dump(private_key_file)

    print('Generating keys...complete')
    print('Adding Funds...')

    api.sync(api.tokens.wealth(entity2, 1000))

    print('Adding Funds...complete')

if __name__ == '__main__':
    main()
