**Запуск в режиме разработки:**
Установка пакетов:
`$ pip install -r requirements.txt`

**Запуск ноды, записывающей все блоки:**
в config/config:
* выберите port
* peer_nodes: ip:port
* mode: 'full'

`$ python main.py`

Проверьте, что получается:

`$ curl ip:port/mine`
`$ curl ip:port/blocks`

Вариант ответа:
`[[{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895127", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "0", "hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74"}, {"previous_hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74", "index": "1", "timestamp": "2018-05-20 10:58:21.050498", "data": "{\"proof-of-work\": 18, \"transactions\": [{\"to\": \"address_full\", \"from\": \"network\", \"amount\": 1}]}", "bucket_depth": "0", "hash": "3194b73177a461bd347abb777876436b6facce73779799327cf3853a427a03ae"}], [{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895217", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "1", "hash": "54e5ab87c87dabe6f3a52d6981dd61a0751e90488df06fc72bc97bfdb919dbb2"}]]`

**Запуск ноды, записывающей бакеты:**
в config/config:
* выберите port
* peer_nodes: ip:port
* mode: 'light'

`$ python main.py`

Проверьте, что получается:

`$ curl ip:port/mine`
`$ curl ip:port/blocks`


Вариант ответа:
`[[{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895127", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "0", "hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74"}, {"previous_hash": "f2a61cf10e5adbd5ea41551580ec2b648065ab21117da5f2cc547effaa2eff74", "index": "1", "timestamp": "2018-05-20 10:58:21.050498", "data": "{\"proof-of-work\": 18, \"transactions\": [{\"to\": \"address_full\", \"from\": \"network\", \"amount\": 1}]}", "bucket_depth": "0", "hash": "3194b73177a461bd347abb777876436b6facce73779799327cf3853a427a03ae"}], [{"previous_hash": "0", "index": "0", "timestamp": "2018-05-20 10:58:18.895217", "data": "{\"proof-of-work\": 9, \"transactions\": null}", "bucket_depth": "1", "hash": "54e5ab87c87dabe6f3a52d6981dd61a0751e90488df06fc72bc97bfdb919dbb2"}]]`

Чтобы повторить результаты:
1) Запустите ноду, записывающую все результаты, по инструкции выше или используя настройки из файла `config_examples/full_node_config.yml`
2) Запустите ноду, записывающую бакеты, по инструкции выше или используя настройки из файла `config_examples/lite_node_config.yml`
3) Запустите скрипт `bench.sh <full_node_address> <lite_node_address>`. При использовании настроек из примера: `bench.sh 127.0.0.1:5000 127.0.0.1:5001`

 Авторы:
 * Александр Парфенов
 * Кузьма Лешаков

 Проверено на `Python 3.6`
