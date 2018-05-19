import json
import requests
import hashlib as hasher
import datetime as date


# Define what a block is
class Block:
    def __init__(self, index, timestamp, backet_depth, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.bucket_depth = backet_depth
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(
            str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') +
            str(self.bucket_depth).encode('utf-8') + str(self.data).encode('utf-8') +
            str(self.previous_hash).encode(('utf-8')))
        return sha.hexdigest()


class NodeState:
    def __init__(self, miner_address, max_bucket_depth=1, peer_nodes=[]):
        self.chains = []
        self.miner_address = miner_address
        self.peer_nodes = peer_nodes
        for bucket_depth in range(max_bucket_depth):
            self.chains.append([create_genesis_block(bucket_depth)])

    def find_new_chains(self):
        other_chains = []
        for node_url in self.peer_nodes:
            # Get their chains using a GET request
            block = requests.get(node_url + "/blocks").content
            # Convert the JSON object to a Python dictionary
            block = json.loads(block)
            # Add it to our list
            other_chains.append(block)
        return other_chains

    def consensus(self):
        # Get the blocks from other nodes
        other_chains = self.find_new_chains()
        # If our chain isn't longest,
        # then we store the longest chain
        longest_chain = self.chains
        for chain in other_chains:
            if len(longest_chain[0]) < len(chain[0]):
                longest_chain = chain
        # If the longest chain isn't ours,
        # then we stop mining and set
        # our chain to the longest one
        self.chains = longest_chain

# Generate genesis block
def create_genesis_block(bucket_depth=0):
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), bucket_depth,
                 {"proof-of-work": 9, "transactions": None}, "0")


def proof_of_work(last_proof):
    # Create a variable that we will use to find
    # our next proof of work
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    # Once that number is found,
    # we can return it as a proof
    # of our work
    return incrementor
