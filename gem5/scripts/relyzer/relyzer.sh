#!/bin/bash

# This script combines many steps of pre-processing into one (in progress)

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Usage : ./relyzer.sh [app_name] [isa] (pop_coverage_size)"
    exit 1
fi

app_name=$1
isa=$2
pop_size=100
if [ $# -eq 3 ]; then
    pop_size=$3
fi

apps_dir=$APPROXGEM5/workloads/$isa/apps/$app_name
curr_dir=$PWD

cd $APPROXGEM5/gem5/scripts/relyzer

if [ ! -f $apps_dir/${app_name}_parsed.txt ]; then
    python inst_database.py $apps_dir/${app_name}.dis $apps_dir/${app_name}_parsed.txt
fi

python control_equivalence_export.py $app_name $isa

python control_equivalence_import.py

cd $apps_dir; sort -t ':' -k1 ${app_name}_control_equivalence_int.txt -o ${app_name}_control_equivalence_int.txt

cd $APPROXGEM5/gem5/scripts/relyzer

python control_equivalence_final.py $app_name $isa

python store_equivalence.py $app_name $isa

python def_use.py $app_name $isa

python bounding_address.py $app_name $isa

python pruning_database.py $app_name $isa

python inj_create.py $app_name $isa $pop_size

