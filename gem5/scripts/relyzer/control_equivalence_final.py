#!/usr/bin/python

# This script build control equivalence classes.

import os
import random
import sys

from inst_database import instruction
from trace import trace_item

seed_val = 1  # seed to ensure consistency when selecting pilots
random.seed(seed_val)

# get information of the program counter

if len(sys.argv) != 3:
    print('Usage: python control_equivalence_final.py [app_name] [isa]')
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]

approx_dir = os.environ.get('APPROXGEM5')
apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
app_prefix = apps_dir + '/' + app_name

in_filename = app_prefix + '_control_equivalence_int.txt'
out_filename = app_prefix + '_control_equivalence.txt'

output = open(out_filename, 'w')
output.write('pc:population:pilot:members\n')

pc = ''
equiv_id = ''
pop = 0
members = []

def print_equiclass():
    global pc
    global pop
    global members
    global output
    pilot = members[random.randint(0,pop-1)]
    output.write('%s:%d:%s:%s\n' % (pc, pop, pilot, ' '.join(members))) 
    pop = 0
    members = []
    

with open(in_filename) as f:
    for line in f:
        line_split = line.rstrip().split(':')
        curr_pc = line_split[0]
        curr_equiv_id = line_split[1]
        tick = line_split[2]
        if pc == '':
            pc = curr_pc
            equiv_id = curr_equiv_id
        if curr_pc != pc:
            print_equiclass()
            pc = curr_pc
            equiv_id = curr_equiv_id
        if curr_equiv_id != equiv_id:
            print_equiclass()
            equiv_id = curr_equiv_id
        members.append(tick)
        pop += 1
            
output.close()

