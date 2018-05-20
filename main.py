from server import node
from config import config

if __name__ == '__main__':
    # A completely random address of the owner of this node
    node.run(port=config['port'])
