#!/bin/bash

for test_file in *input.txt
do
		cat $test_file | formatCBMCOutput | diff -u $(echo $test_file | cut -d'_' -f1)*_output.txt -
done	
