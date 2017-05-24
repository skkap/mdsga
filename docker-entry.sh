#!/bin/bash

cd /app/src

#muts=( 0.0001 0.0005 0.001 0.005 0.01 0.05 )
#for i in "${muts[@]}"
#do
#  echo $i
#  echo $SAMPLE_PATH
#  python ga_main.py $SAMPLE_PATH -g 100 -p 200 -m $i
#done


co=( 1p 2p 3p mp u )
for i in "${co[@]}"
do
  echo $i
  echo $SAMPLE_PATH
  echo $TRIES
  for t in $(seq $TRIES);
  do
    python ga_main.py $SAMPLE_PATH -g 100 -m 0.001 -c $i
  done
done