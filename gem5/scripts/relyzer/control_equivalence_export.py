#!/usr/bin/python

# This script build control equivalence classes.

import pickle
import os
import random
import sys

from inst_database import instruction
from trace import trace_item

seed_val = 1  # seed to ensure consistency when selecting pilots

# get information of the program counter

if len(sys.argv) != 3:
    print('Usage: python control_equivalence_export.py [app_name] [isa]')
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


with open(trace_filename) as trace:
    bbstart = None
    bbend = None
    start_of_bb = True
    pc = None
    prev_pc = pc
    for line in trace:
        items = line.split()
        item = trace_item(items)
        pc = item.pc
        inst_num = item.inst_num
        if pc in ctrl_insts:
            if not start_of_bb:
                start_of_bb = True
        elif start_of_bb:
            basicblocks.add(pc)
            program_bb.append([inst_num, pc])
            start_of_bb = False

# instructions after the last control block are to be included; the last instruction probably is a control instruction though.        
print('Basic blocks created.')
program_len = len(program_bb)
print('Program length in bbs:', len(program_bb))
print('Number of basic blocks:', len(basicblocks))



# create equivalence classes and find their ticks
# length of elements in equivalence class
equiclass_depth = min(50,program_len)
equiclass_cap = 50 # cap on number of equivalence classes per basic block
equiclass_map = {}   # list of equivalence classes
equiclass_index_map = {} # stores indices for members of equivalence class
equiclass_ticks_map = {}  # start times corresponding to each equivalence class instance
tick_equiv_id_map = {} # given bb_id tick, 
equiclass_bb_count = {}
bb_id_depth = {}

def create_equiclass(bbseq, tick_val, index, bb_id):
    global equiclass_map
    global equiclass_index_map
    global equiclass_ticks_map
    global equiclass_bb_count

    equiv_match = False

    if bb_id not in equiclass_map:
        equiclass_map[bb_id] = {}
        equiclass_index_map[bb_id] = {}
        equiclass_ticks_map[bb_id] = {}
    for equiv_id in equiclass_map[bb_id]: 
        if bbseq == equiclass_map[bb_id][equiv_id]:
            equiv_match = True
            equiclass_index_map[bb_id][equiv_id].append(index)
            equiclass_ticks_map[bb_id][equiv_id].append(tick_val)
            break
    if not equiv_match:
        equiclass_map[bb_id][index] = bbseq
        equiclass_index_map[bb_id][index] = [index]
        equiclass_ticks_map[bb_id][index] = [tick_val]
        equiv_id = index


    # check number of equiclasses for each bb
    if bb_id not in equiclass_bb_count:
        equiclass_bb_count[bb_id] = set()
    equiclass_bb_count[bb_id].add(equiv_id)
    tick_equiv_id_map[tick_val] = equiv_id



for main_index in range(0,len(program_bb)-equiclass_depth+1):
    index = main_index # distinguishing main_index from index for clarity
    bb_id = program_bb[index][1]
    curr_depth = bb_id_depth.get(bb_id, equiclass_depth)
    bbseq = [item[1] for item in program_bb[index:index+curr_depth]]
    tick_val = program_bb[index][0]
    create_equiclass(bbseq, tick_val, index, bb_id)
    
    
    # dynamically resize until the number of equivalence classes within cap
    if len(equiclass_bb_count[bb_id]) > equiclass_cap:
        total_indices = []
        for equiv_id in equiclass_index_map[bb_id]:
             for index in equiclass_index_map[bb_id][equiv_id]:
                total_indices.append(index)

        new_depth = curr_depth - 1
        while len(equiclass_bb_count[bb_id]) > equiclass_cap:
            # reset data structures associated with bb_id
            equiclass_map[bb_id] = {}
            equiclass_index_map[bb_id] = {}
            equiclass_ticks_map[bb_id] = {}
            equiclass_bb_count[bb_id] = set()
            
            for index in total_indices:
                bbseq = [item[1] for item in program_bb[
                         index:index+new_depth]]
                tick_val = program_bb[index][0]
                
                create_equiclass(bbseq, tick_val, index, bb_id)
                
            new_depth -= 1
        curr_depth = new_depth
    bb_id_depth[bb_id] = curr_depth

# edge case towards the end of the array
for main_index in range(len(program_bb)-equiclass_depth,len(program_bb)):
    index = main_index # distinguishing main_index from index for clarity
    bb_id = program_bb[index][1]
    curr_depth = bb_id_depth.get(bb_id, equiclass_depth)
    end_depth = min(curr_depth,len(program_bb)-(len(
                program_bb)-equiclass_depth))
    bbseq = [item[1] for item in program_bb[index:index+end_depth]]
    tick_val = program_bb[index][0]

    create_equiclass(bbseq, tick_val, index, bb_id)
    
    
    # dynamically resize until the number of equivalence classes within cap
    if len(equiclass_bb_count[bb_id]) > equiclass_cap:
        total_indices = []
        for equiv_id in equiclass_index_map[bb_id]:
             for index in equiclass_index_map[bb_id][equiv_id]:
                total_indices.append(index)

        new_depth = curr_depth - 1
        while len(equiclass_bb_count[bb_id]) > equiclass_cap:
            # reset data structures associated with bb_id
            equiclass_map[bb_id] = {}
            equiclass_index_map[bb_id] = {}
            equiclass_ticks_map[bb_id] = {}
            equiclass_bb_count[bb_id] = set()
            
            for index in total_indices:
                if index == total_indices[-1]:
                    bbseq = [item[1] for item in program_bb[
                             index:index+end_depth]]
                    
                else: 
                    bbseq = [item[1] for item in program_bb[
                             index:index+new_depth]]
                tick_val = program_bb[index][0]
                create_equiclass(bbseq, tick_val, index, bb_id)
            new_depth -= 1
        curr_depth = new_depth
    bb_id_depth[bb_id] = curr_depth
    # print('Finished iteration: %d' % index)    
        
print('Equivalence classes created.')


# pc_equiclass_map = {}
# pc -> equiclass_id: [ ticks belonging to that equiclass id ]
pickle.dump(basicblocks, open('basicblocks.p', 'wb'))
pickle.dump(program_bb, open('program_bb.p', 'wb'))
pickle.dump(equiclass_index_map, open('equiclass_index_map.p', 'wb'))
pickle.dump(tick_equiv_id_map, open('tick_equiv_id_map.p', 'wb'))

