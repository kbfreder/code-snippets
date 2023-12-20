#!/bin/bash


CLUSTER_NAME="pcp-collect-ts"
STEP_NAME="CollectTimestamps"
script="collect_timestamps.py"

master_fam="r6g"
master_size="xlarge"
master_num=1

core_fam="r6g"
core_size="4xlarge"
core_num=4

usage="""
$(basename "$0")

Args:
--script-args: Arguments to pass to script. Enclose in single quotes,
    e.g.: --script-args '--date-start 2023-01-01'. See $script 
    for expected arguments.
-h, --help: Print this message and exit.
"""

while [ "$1" != "" ]; do
    case $1 in
        --script-args )         shift
                                script_args=$1
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
        * )                     echo "Unexpected argument!"
                                echo "$usage"
                                exit 1
    esac
    shift
done


cc_out=$(./create-cluster.sh --master-family $master_fam --master-size $master_size --master-num $master_num --core-family $core_fam --core-size $core_size --core-num $core_num --cluster-name $CLUSTER_NAME) 

cluster_id=$(echo $cc_out | cut -f1 -d' ')
exec_mem=$(echo $cc_out | cut -f2 -d' ')
driv_mem=$(echo $cc_out | cut -f3 -d' ')
num_instances=$(echo $cc_out | cut -f4 -d' ')

echo ClusterID: $cluster_id

ss_out=$(./submit-step.sh --cluster-id $cluster_id --exec-mem $exec_mem --driv-mem $driv_mem --num-instances $num_instances --script $script --step-name $STEP_NAME --script-args "$script_args")

echo StepID: $ss_out
