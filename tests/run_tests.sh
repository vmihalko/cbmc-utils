#!/bin/bash
for test_file in $(ls *input.txt)
do
		cat $test_file | ./../formatCBMCOutput.py | diff -u $(echo $test_file | cut -d'_' -f1)*_output.txt -
done	
