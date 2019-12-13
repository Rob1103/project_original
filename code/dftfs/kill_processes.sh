#!/bin/bash
if (($# < 2))
then
    echo "Usage : ./kill_nodes.sh <number_of_nodes> <first_pid>"
fi

for ((i=$2; i < $(($1+$2)); i++))
do
    kill $i
done
