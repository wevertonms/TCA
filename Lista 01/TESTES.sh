#!/bin/bash

for N in 10 100 1000 10000; do
    echo $N
    shuf -i 0-$((N+1)) -n $N > numbers.txt
    echo $N $(cat numbers.txt) | ./sort > meu.txt
    echo $(cat numbers.txt) | tr ' ' '\n' | sort -n > shell.txt
    diff meu.txt shell.txt    
done
 