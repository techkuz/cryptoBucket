#!/bin/sh

for i in {1..100}
do
	for j in {1..20}
	do
		curl "$1/transaction" -H "Content-Type: application/json" \
			-d '{"from": "usr1", "to":"usr2", "amount": 3}' > /dev/null 2>&1
	done
	curl $1/mine > /dev/null 2>&1
done

curl $2/mine > /dev/null 2>&1

echo "Full history size (bytes):"
curl -sI $1/blocks | grep Content-Length
echo "Bucketed history size (bytes):"
curl -sI $2/blocks | grep Content-Length
