import json
import datetime as date
from flask import Flask
from flask import request
from cryptobucket import Block, NodeState, proof_of_work


miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
blockchain = NodeState(miner_address, 2, [], NodeState.NodeMode.USER_NODE)
node = Flask(__name__)
this_nodes_transactions = []


@node.route('/txion', methods=['POST'])
def transaction():
    # On each new POST request,
    # we extract the transaction data
    new_txion = request.get_json()
    # Then we add the transaction to our list
    this_nodes_transactions.append(new_txion)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print("New transaction")
    print("FROM: {}".format(new_txion['from'].encode('ascii', 'replace')))
    print("TO: {}".format(new_txion['to'].encode('ascii', 'replace')))
    print("AMOUNT: {}\n".format(new_txion['amount']))
    # Then we let the client know it worked out
    return "Transaction submission successful\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chains_to_send = []
    # Convert our blocks into dictionaries
    # so we can send them as json objects later
    for i in range(len(blockchain.chains)):
        chain = blockchain.chains[i]
        chain_to_send = []
        for j in range(len(chain)):
            block = chain[j]
            block_index = str(block.index)
            block_timestamp = str(block.timestamp)
            block_bucket_depth = str(block.bucket_depth)
            block_data = str(block.data)
            block_hash = block.hash
            chain_to_send.append({
                "index": block_index,
                "timestamp": block_timestamp,
                "bucket_depth": block_bucket_depth,
                "data": block_data,
                "hash": block_hash
            })
        chains_to_send.append(chain_to_send)
    chain_to_send = json.dumps(chains_to_send)
    return chain_to_send


@node.route('/mine', methods=['GET'])
def mine():
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

    # Let the client know we mined a block
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "bucket_depth": str(0),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"