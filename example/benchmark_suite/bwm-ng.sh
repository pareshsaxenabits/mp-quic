#!/bin/bash

FILENAME="results.csv"

rm -f $FILENAME

flags=(
    -o csv
    -F $FILENAME        # Name of output csv file
    -C ","              # CSV delimiter
    -u bytes            # Units: 'bytes', 'bits', 'packets', 'errors'
    -T sum
    # -c 5                # Number of outputs
    -t 500             # Time interval between consecutive reading

    # List of interfaces to inspect
    -I s1-eth1,s2-eth1
)

echo "Starting bwm-ng"
bwm-ng "${flags[@]}"
echo "bwm-ng over"
