**Development mode launch:**  
Install packages:  
`$ pip install -r requirements.txt`

**Run node with all transactions:**   
in config/config: 
* choose port  
* peer_nodes: ip:port
* mode: 'full'

`$ python main.py`

To test:

`$ curl ip:port/mine`  
`$ curl ip:port/blocks`

Example Reply:  
`[[{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895127", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "0", "hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74"}, {"previous_hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74", "index": "1", "timestamp": "2018-05-20 10:58:21.050498", "data": "{\"proof-of-work\": 18, \"transactions\": [{\"to\": \"address_full\", \"from\": \"network\", \"amount\": 1}]}", "bucket_depth": "0", "hash": "3194b73177a461bd347abb777876436b6facce73779799327cf3853a427a03ae"}], [{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895217", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "1", "hash": "54e5ab87c87dabe6f3a52d6981dd61a0751e90488df06fc72bc97bfdb919dbb2"}]]`

**Node writing bucket transactions:**  
in config/config: 
* choose port  
* peer_nodes: ip:port
* mode: 'light'

`$ python main.py`

To test:

`$ curl ip:port/mine`  
`$ curl ip:port/blocks`


Example Reply:  
`[[{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895127", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "0", "hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74"}, {"previous_hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74", "index": "1", "timestamp": "2018-05-20 10:58:21.050498", "data": "{\"proof-of-work\": 18, \"transactions\": [{\"to\": \"address_full\", \"from\": \"network\", \"amount\": 1}]}", "bucket_depth": "0", "hash": "3194b73177a461bd347abb777876436b6facce73779799327cf3853a427a03ae"}], [{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895217", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "1", "hash": "54e5ab87c87dabe6f3a52d6981dd61a0751e90488df06fc72bc97bfdb919dbb2"}]]`

 
 Authors: 
 * Aleksandr Parfenov
 * Kuzma Leshakov
 
 Tested with `Python 3.6`