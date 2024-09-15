#!/bin/bash

#compile sum_baseline.c
gcc -O2 -o sum_baseline.o sum_baseline.c

#test value
values=(100000000 1000000000 10000000000)

#run test
for value in "${values[@]}"
do 
  echo "Testing with N = $value"
  time ./sum_baseline.o $value
  echo "-----------------------"
done

