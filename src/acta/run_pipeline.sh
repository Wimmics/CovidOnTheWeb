#!/usr/bin/env bash

source activate test

#filename: name of the batch file without the ".json"
#datafolder: path to folder with batch files

data_dir='../data/v7/clustered/'

python pipeline.py --fname 3 --data_dir $data_dir

