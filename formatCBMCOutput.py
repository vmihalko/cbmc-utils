#!/usr/bin/env python3
'''
usage: cbmc <file> <checks> --verbosity 4 --json-ui | ./format_cbmc_output 
'''

import sys, json
from collections import defaultdict, OrderedDict #OrderedDict for removing duplicates
NL = '\n'


def parse_source_location(array_info):
    source_loc = array_info['sourceLocation']
    line_num, file_name = source_loc['line'], source_loc['file']
    return f"{file_name}:{line_num}: note: "


def parse_data(array_info):
    return array_info['data'] if 'data' in array_info else "?"


def parse_assingment(array_info):
    result_str = []
    result_str.append(parse_source_location(array_info))

    if array_info['assignmentType'] == "actual-parameter":
        result_str.append(f"function_parameter_set_in:")
    if 'function' not in array_info['sourceLocation']:
        result_str.append(f"entry_point_function:")
    else:
        result_str.append(f"{array_info['sourceLocation']['function']}:")
    result_str.append(
        f"{array_info['sourceLocation']['line']}:{array_info['value']['name']}:{8*' '}{array_info['lhs']} = "
    )
    if 'elements' in array_info['value']:
        result_str.append(
            f"{[parse_data(val['value']) for val in array_info['value']['elements']]}{NL}"
        )
    else:
        result_str.append(f"{parse_data(array_info['value'])}{NL}")
    return ''.join(result_str)


def parse_function(array_info):
    result_str = []
    result_str.append(parse_source_location(array_info))

    if 'function' not in array_info['sourceLocation']:
        result_str.append(f"from_entry_point_function:")
    else:
        result_str.append(f"from_{array_info['sourceLocation']['function']}:")

    result_str.append(
        f"{array_info['stepType']}:{array_info['function']['displayName']}{NL}")
    return ''.join(result_str)


def parse_trace(trace_arr):
    result_str = []
    for index, step in enumerate(trace_arr):
        if 'hidden' in step and step['hidden'] or \
           'internal' in step and step['internal']  or \
           'sourceLocation' not in step:
            continue
        if 'function' in step:
            result_str.append(parse_function(step))
        elif 'assignmentType' in step:
            result_str.append(parse_assingment(step))
        elif 'reason' in step:
            result_str.append(
                f"{parse_source_location(step)}{step['reason']}{NL}")

    return ''.join(list(OrderedDict.fromkeys(result_str)))  #remove duplicates


def parse_it():
    parsed = json.load(sys.stdin)
    errors = defaultdict(list)

    for result in parsed[-3]['result']:
        if result['status'] == "FAILURE":
            info = result['trace'][-1:]
            trace = parse_trace(result['trace'])
            source_loc = info[0]['sourceLocation']

            file_name = source_loc['file']
            fun_name = source_loc['function']
            line_num = source_loc['line']

            reason = info[0]['reason']
            proprty = info[0]['property']

            errors[(file_name, fun_name)].append(
                (line_num, reason, proprty, trace))
    return errors


def print_it(error_dict):
    for file_and_func_name in error_dict.keys():
        file_name, func_name = file_and_func_name
        print(f"{file_name}: In function ‘{func_name}’:")
        for err in error_dict[file_and_func_name]:
            line_num, proprty, trace = err[0], err[1], err[3]
            reason = err[2].split('.')[1]
            print(
                f"{file_name}:{line_num}: error: {reason} : {proprty}{NL}{trace}"
                , end="")


print_it(parse_it())
