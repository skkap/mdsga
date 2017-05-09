#!/bin/bash

cd /app/src

muts=( 0.0001 0.0005 0.001 0.005 0.01 0.05 )
for i in "${muts[@]}"
do
  echo $i
  echo $SAMPLE_PATH
  python ga_main.py $SAMPLE_PATH -g 100 -p 200 -m $i
done
