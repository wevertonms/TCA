#!/bin/bash

# echo "Número aleatórios"
# for N in 10 100 1000 10000; do
#     echo $N
#     shuf -i 0-$((N+1)) -n $N > numbers.txt
#     echo $N $(cat numbers.txt) | ./sort > meu.txt
#     echo $(cat numbers.txt) | tr ' ' '\n' | sort -n > shell.txt
#     diff meu.txt shell.txt    
# done

echo "Número em ordem decrescente"
for N in 10 100; do
    echo $N
    seq $N -1 1 > numbers.txt
    echo $N $(cat numbers.txt) | ./sort > meu.txt
    echo $(cat numbers.txt) | tr ' ' '\n' | sort -n > shell.txt
    diff meu.txt shell.txt
done
