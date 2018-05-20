from server import node
from config import config

if __name__ == '__main__':
    # A completely random address of the owner of this node
    node.run(host='0.0.0.0', port=config['port'])
