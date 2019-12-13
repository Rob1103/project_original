#!/bin/bash
if (($# < 1))
then
	echo -e "Missing argument : number of nodes"
	echo "Usage : ./init_file_system.sh <number_of_nodes>"
	exit
fi

python3 master.py "$1" 1024 &

for ((i=0; i<$1; i++))
do
	python3 node.py $((2000+i)) &	# port number will be sys.argv[1] in python code
done
