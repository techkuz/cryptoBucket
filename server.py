import json
import datetime as date

from flask import Flask
from flask import request

from cryptobucket import Block, NodeState, proof_of_work
from config import config


blockchain = NodeState(config['miner_address'], config['bucket']['depth'], config['peer_nodes'],
                       config['mode'])
node = Flask(__name__)
this_nodes_transactions = []


@node.route('/transaction', methods=['POST'])
def transaction():
    # Extract transaction data
    new_transaction = request.get_json()

    this_nodes_transactions.append(new_transaction)
    # Success -> log
    print("New transaction")
    print("FROM: {}".format(new_transaction['from'].encode('ascii', 'replace')))
    print("TO: {}".format(new_transaction['to'].encode('ascii', 'replace')))
    print("AMOUNT: {}\n".format(new_transaction['amount']))
    blockchain.consensus()
    # Inform client about success
    return "Transaction submission successful\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chains_to_send = []
    # Bocks to dicts, to send as json later
    for i in range(len(blockchain.chains)):
        chain = blockchain.chains[i]
        chain_to_send = []
        for j in range(len(chain)):
            block = chain[j]
            block_index = str(block.index)
            block_timestamp = str(block.timestamp)
            block_bucket_depth = str(block.bucket_depth)
            block_data = json.dumps(block.data)
            block_hash = block.hash
            block_prev_hash = block.previous_hash
            chain_to_send.append({
                "index": block_index,
                "timestamp": block_timestamp,
                "bucket_depth": block_bucket_depth,
                "data": block_data,
                "previous_hash": block_prev_hash,
                "hash": block_hash
            })
        chains_to_send.append(chain_to_send)
    chain_to_send = json.dumps(chains_to_send)
    return chain_to_send


@node.route('/mine', methods=['GET'])
def mine():
    blockchain.consensus()
    # Get the last proof of work
    last_block = blockchain.chains[0][len(blockchain.chains[0]) - 1]
    last_proof = last_block.data['proof-of-work']
    # Find the proof of work for
    # the current block being mined
    # Note: The program will hang here until a new
    #       proof of work is found
    proof = proof_of_work(last_proof)
    # Once we find a valid proof of work,
    # we know we can mine a block so
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
        {"from": "network", "to": blockchain.miner_address, "amount": 1}
    )
    # Now we can gather the data needed
    # to create the new block
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # Empty transaction list
    this_nodes_transactions[:] = []
    # Now create the
    # new block!
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        0,
        new_block_data,
        last_block_hash
    )
    blockchain.chains[0].append(mined_block)

    for i in range(1, len(blockchain.chains)):
        if blockchain.is_bucket_possible(i):
            blockchain.pack_blocks_into_bucket(i, proof)

    # Inform client that mined
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "bucket_depth": str(0),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"