#!/usr/bin/python

# This script build control equivalence classes.

import os
import cPickle as pickle
import sys

from inst_database import instruction
from trace import trace_item


# get information of the program counter

if len(sys.argv) != 3:
    print('Usage: python control_equivalence_import.py [app_name] [isa]')
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]

approx_dir = os.environ.get('APPROXGEM5')
apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
app_prefix = apps_dir + '/' + app_name

db_filename = app_prefix + '_parsed.txt'
trace_filename = app_prefix + '_clean_dump_parsed_merged.txt'


db_info = [i for i in open(db_filename).read().splitlines()[1:]]
insts = [instruction(None,None,i) for i in db_info]
ctrl_insts = set([i.pc for i in insts if i.ctrl_flag])



# list of basic blocks. Each list element is a 2-length list with
# first element as start PC and second as end PC
basicblocks = set() # defaultdict(int)
# program represented as basic blocks with tick value at start of basic block
program_bb = [] 

basicblocks = pickle.load(open('basicblocks.p', 'rb'))
program_bb = pickle.load(open('program_bb.p', 'rb'))

print('Basic blocks created.')
print('Program length in bbs:', len(program_bb))
print('Number of basic blocks:', len(basicblocks))

equiclass_index_map = pickle.load(open('equiclass_index_map.p', 'rb'))
tick_equiv_id_map = pickle.load(open('tick_equiv_id_map.p', 'rb'))
print('Loaded equivalence class data.')

output_file = app_prefix + '_control_equivalence_int.txt' 
output = open(output_file, 'w')
bb_idx = -1
bb_id = None
bb_tick = None
with open(trace_filename) as trace:
    i = 0
    for line in trace:
        items = line.split()
        item = trace_item(items)
        tick = item.inst_num
        pc = item.pc
        if bb_idx < len(program_bb)-1:  # starting tick indicates new bb
            bb_tick = program_bb[bb_idx+1][0]
            if tick == bb_tick:
                bb_idx += 1
                bb_id = program_bb[bb_idx][1]
        if pc in ctrl_insts:  # ignore control instructions
            continue
        if item.is_store():  # store inst check
            continue  # stores will be handled w/ store equiv
        equiv_id = tick_equiv_id_map[bb_tick]
        output.write('%s:%s:%s\n' % (pc,equiv_id,tick))
        i += 1
        if (i % 10000) == 0:
            print('processed %d insts' % i)

output.close()
