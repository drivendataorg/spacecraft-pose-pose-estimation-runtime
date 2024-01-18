#!/usr/bin/env bash

# create a temporary directory to stash individual chain CSVs in
temp_dir=$(mktemp -d)

# find all the chain directories in advance so we can parallelize in the next step
find ../data/images -maxdepth 1 -mindepth 1 -type d > directories.txt

# use GNU parallel to run main.py on all of the chain dirs we just found
# - the first argument {} will be a path to a chain dir, from each line of directories.txt
# - the second argument is the temporary directory we just created
# - the argument -j 0 means use all available cores
# - the argument -a directories.txt means use the file we just created as a list of inputs
parallel -j 0 -a directories.txt python main.py {} $temp_dir

# use our other script to put all these individual CSVs back together into the expected format
python assemble.py $temp_dir