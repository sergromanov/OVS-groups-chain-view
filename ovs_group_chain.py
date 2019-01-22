#!/usr/bin/python

# from __future__ import print_function
import cmd, sys, argparse, re
from time import time

def print_group(cur_group_id, prefix = ''):
    if cur_group_id is not None:
        if cur_group_id in groups.keys():
            row = prefix + groups[cur_group_id]['text']
            tail = ""
            print(row.expandtabs(8) + tail)
            for k in groups[cur_group_id]['buckets'].keys():
                print_bucket(cur_group_id, k, prefix)
                print_group(groups[cur_group_id]['buckets'][k]['refgroup'], prefix+'\t')
        else:
            row = prefix + 'groupId = ' + cur_group_id + ': NOT FOUND'
            print(row.expandtabs(8))


def print_bucket(cur_group_id, cur_bucket, prefix = ''):
    if cur_group_id in groups.keys():
        row = prefix + 'bucket:' + str(cur_bucket) + ',' + groups[cur_group_id]['buckets'][cur_bucket]['text']
        print(row.expandtabs(8))

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(prog='ovs_group_chain.py')
    arg_parser.add_argument('--version', action='version', version='1.0')
    arg_parser.add_argument('-v', action='version', version='1.0')
    arg_parser.add_argument('-f', help='OVS-like switch dump-group file. STDIN used if omitted.', required=False)
    arg_parser.add_argument('groupID', help='Initial group ID')
    argv = vars(arg_parser.parse_args())

    groups = dict()
    dump = argv['f']
    if dump is None:
        lines = list()
        line = sys.stdin.readline()
        while line:
            lines.append(line)
            line = sys.stdin.readline()
    else:
        with open(dump, "r") as f:
            lines = f.read().splitlines()
            f.close()

    for line in lines:
        buckets = re.split(r"bucket=", line.strip())
        idx = -1
        for bucket in buckets:
            prog = re.compile(r"group_id=(\d+),type=(\w+),")
            m = prog.search(bucket)
            if m is not None:
                group_id = m.group(1)
                group = dict()
                group['type'] = m.group(2)
                group['text'] = bucket
                group['buckets'] = dict()
                groups[group_id] = group
                idx += 1
            elif idx >= 0:
                group_bucket = idx
                groups[group_id]['buckets'][group_bucket] = {'refgroup': None, 'text': bucket}
                prog = re.compile(r"group:(\d+)")
                m = prog.search(bucket)
                if m is not None:
                    group_refgroup = m.group(1)
                    groups[group_id]['buckets'][group_bucket]['refgroup'] = group_refgroup
                idx += 1


    group_types = dict()
    for group in groups.values():
        if group['type'] in group_types.keys():
            group_types[group['type']] += 1
        else:
            group_types[group['type']] = 1

    print('Switch group types statistics:')
    print('Total groups: ' + str(len(groups)))
    for k in group_types.keys():
        print('Type:' + str(k) + ' Num: ' + str(group_types[k]))

    print('\nChain for groupId '+ argv['groupID']+ ':')
    print_group(argv['groupID'], '')