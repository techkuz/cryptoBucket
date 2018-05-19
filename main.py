from cryptobucket import create_genesis_block
from server import node

if __name__ == '__main__':

    # A completely random address of the owner of this node
    miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
    # This node's blockchain copy
    blockchain = []
    blockchain.append(create_genesis_block())
    # Store the transactions that
    # this node has in a list
    # this_nodes_transactions = []
    # Store the url data of every
    # other node in the network
    # so that we can communicate
    # with them
    peer_nodes = []
    # A variable to deciding if we're mining or not
    mining = True

    node.run()
