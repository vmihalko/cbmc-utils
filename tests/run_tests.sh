#!/bin/bash

error=0
for test_file in $(ls test_inputs)
do
    echo -n "${test_file/.input}: "
	if cat test_inputs/$test_file\
			| ../cbmc_utils/formatCBMCOutput.py\
			| diff -u test_outputs/${test_file/.input}.output - \
			&& csgrep test_outputs/${test_file/.input}.output >> /dev/null
    then
        echo -e "\e[1m\e[92mPASS\e[0m"
    else
		error=1
        echo -e "\e[1m\e[91mFAIL\e[0m"
    fi  
done	
exit $error
