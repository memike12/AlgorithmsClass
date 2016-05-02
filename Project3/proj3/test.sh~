#!/usr/bin/env bash

#Note, this program uses elapsed time. This is so that it can work with multithreaded programs. So it's not super accurate
red='\033[0;31m'
green='\e[0;32m'
endColor='\e[0m'
commandToRun="python3 solvemaze.py" #put java solvemaze or ./solvemaze or whatever you want to run your program
sizes=("10" "20" "50" "100" "200" "500" "1000") #Sizes to run on, only tests square mazes
#sizes=("10" "20") #uncomment this if you want a quick and dirty test
densities=("0" "1" "10") #Densities that it's run with 
methods=("rPrims" "fillFromPath") #methods used to generate the maze
if ! [ -d "test" ]; then #create the test directory where everything will reside
    mkdir test
    chmod 700 test
fi
#Checking if files exist, if not it generates and saves those files.
echo "Creating all mazes...Might take a while if it's your first time"
for method in "${methods[@]}"
do
    for density in "${densities[@]}"
    do
	for size in "${sizes[@]}"
	do
	    fname="test/$density$method$size"
	    echo $fname
	    if ! [ -f $fname ]; then 
		python3 genmaze.py $size $size $method $density > $fname
		echo "$method with $density density and $size size created"
		chmod 700 $fname
	    fi
	done
    done
done
echo "Done creating mazes"
echo "Running all methods...Will probably take a long time"
#Run your program on all of those files and give stats
for method in "${methods[@]}"
do
    for density in "${densities[@]}"
    do
	for size in "${sizes[@]}"
	do
	    fname="test/$density$method$size"
	    echo "Running $density$method$size"
	    s="s"
	    t=$( { /usr/bin/time -f "%e" $commandToRun < $fname > $fname$s; } 2>&1)
	    re='^[0-9]+([.][0-9]+)?$'
	    if ! [[ $t =~ $re  ]]; then
		echo -e "$red ERROR: it failed$endColor"
	    else
		good=$(echo "$t<3" | bc)
		if [ $good -eq "1" ]; then
		    echo -e "$green $t seconds$endColor"
		else
		    echo -e "$red $t seconds$endColor"
		fi
		output=$( { python3 scoremaze.py $fname $fname$s; }  2>test/tempfile)
		numCoins=$(grep 'Found a coin' test/tempfile | wc -l)
		foundExit=$(grep 'Found the finish' test/tempfile | wc -l)
		if [ $numCoins -eq "10" ]; then
		    echo -e "$green Found all the coins$endColor"
		else
		    echo -e "$red Found $numCoins coins$endColor"
	        fi
		if [ $foundExit -eq "1" ]; then
		    echo -e "$green Found the exit$endColor"
		else
		    echo -e "$red Did not find the exit$endColor"
		fi
		b="b"
		if ! [ -f $fname$b ]; then
		    echo -e "$green Score of $output . New best score.$endColor"
		    echo $output > $fname$b
		else
		    best=$(cat $fname$b)
		    if [ "$best" -lt "$output" ]; then
			echo -e "$green Score of $output . New best score.$endColor"
			echo $output > $fname$b
		    elif [ $best -eq $output ]; then
			echo -e "$green Score of $output$endColor"
		    else
			echo -e "$red scoore of $output$endColor"
		    fi
		fi
	    fi
	done
    done
done
