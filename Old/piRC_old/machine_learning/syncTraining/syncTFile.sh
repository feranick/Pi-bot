#!/bin/bash

server="user@server.org"
folder="/home/user/ML/pirc"

if [ "$1" = "" ]; then
   trainFile="Training_splrcbxyz"
else
   trainFile=$1
fi

echo
echo "Transferring training file (" $trainFile.txt ") to:" $server
scp -C $trainFile.txt $server:$folder

echo
echo "Running training using:" $trainFile.txt
ssh -C $server $folder/piRC_ML.py -t $folder/$trainFile.txt

echo "Transferring training model (" $trainFile.nnModelC.pkl ") from:" $server
scp -C $server:$folder/$trainFile.nnModelC.pkl .
echo
