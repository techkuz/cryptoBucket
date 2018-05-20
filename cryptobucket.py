import json
import requests
import hashlib as hasher
import datetime as date
from enum import Enum

bucket_size = 5
minimum_tail = 5


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
    class NodeMode(Enum):
        SERVICE_NODE = 1
        USER_NODE = 2

    def __init__(self, miner_address, max_bucket_depth=1, peer_nodes=[], mode=NodeMode.SERVICE_NODE):
        self.chains = []
        self.miner_address = miner_address
        self.peer_nodes = peer_nodes
        self.mode = mode
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

    def pack_blocks_into_bucket(self, bucket_depth, proof):
        last_bucket = self.chains[bucket_depth][len(self.chains[bucket_depth]) - 1]
        lborder = 1
        offset = self.chains[bucket_depth - 1][0].index

        if last_bucket.index != 0:
            lborder = last_bucket.data['to_block'] + 1
            lborder = lborder - offset

        rborder = lborder + bucket_size
        last_hash_before_bucket = self.chains[bucket_depth - 1][lborder - 1].hash
        last_hash_in_bucket = self.chains[bucket_depth - 1][rborder].hash
        new_bucket = Block(last_bucket.index + 1, date.datetime.now(), bucket_depth,
                           {"proof-of-work": proof, "from_block" : lborder + offset, "to_block": rborder + offset,
                            "last_hash_before_bucket": last_hash_before_bucket,
                            "last_hash_in_bucket": last_hash_in_bucket}, last_bucket.hash)
        self.chains[bucket_depth].append(new_bucket)

        if self.mode == NodeState.NodeMode.USER_NODE:
            self.chains[bucket_depth - 1] = self.chains[bucket_depth - 1][rborder:]

    def is_bucket_possible(self, bucket_depth):
        last_bucket = self.chains[bucket_depth][len(self.chains[bucket_depth]) - 1]
        lborder = 1

        if last_bucket.index != 0:
            lborder = last_bucket.data['to_block'] + 1

        newest_block = self.chains[bucket_depth - 1][len(self.chains[bucket_depth - 1]) - 1].index
        return newest_block - lborder > bucket_size + minimum_tail

# Generate genesis block
def create_genesis_block(bucket_depth=0):
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), bucket_depth,
                 {"proof-of-work": 9, "transactions": None}, "0")


def proof_of_work(last_proof):
    # Create a variable that we will use to find
    # our next proof of work
    incrementor = last_proof + last_proof
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += last_proof
    # Once that number is found,
    # we can return it as a proof
    # of our work
    return incrementor
