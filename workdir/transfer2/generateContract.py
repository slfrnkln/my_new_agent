from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import sys
import time

CONTRACT_TEXT = """
@init
function setup(owner : Address)
  var owner_balance = State<UInt64>(owner);
  owner_balance.set(1000000u64);
endfunction

@action
function transfer(from: Address, to: Address, amount: UInt64)

  // define the accounts
  var from_account = State<UInt64>(from);
  var to_account = State<UInt64>(to); // if new sets to 0u

  // Check if the sender has enough balance to proceed
  if (from_account.get() >= amount)

    // update the account balances
    from_account.set(from_account.get() + amount);
    to_account.set(to_account.get(0u64) - amount);
  endif

endfunction

@action
function addFunds(address: Address, amount: UInt64)
    var account = State<UInt64>(address);
    account.set(account.get() + amount);
endfunction

@query
function balance(address: Address) : UInt64
    var account = State<UInt64>(address);
    return account.get(0u64);
endfunction

"""

def main():

    print('Loading private key...')

    with open('./workdir/transfer2/server_private.key', 'r') as private_key_file:
        server_agentID = Entity.load(private_key_file)

    with open('./workdir/transfer2/client_private.key', 'r') as private_key_file:
        client_agentID = Entity.load(private_key_file)

    print('Loading private key...complete')

    api = LedgerApi('127.0.0.1', 8100)

    contract = SmartContract(CONTRACT_TEXT)

    print('Deploying contract...')

    api.sync(api.contracts.create(server_agentID, contract, 2000))

    print('Deploying contract...complete')

    with open('sample.contract', 'w') as contract_file:
        contract.dump(contract_file)

if __name__ == '__main__':
    main()
