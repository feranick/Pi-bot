#!/bin/bash

server="user@server.org"
folder="/home/user/ML/pirc"

if [ "$1" = "" ]; then
   trainFile="Training_splrcbxyz"
else
   trainFile=$1
fi

scp -C $trainFile.txt $server:$folder

echo "Running trainning..."
ssh -C $server $folder/piRC_ML.py -t $folder/$trainFile.txt 

scp -C $server:$folder/$trainFile.nnModelC.pkl .
