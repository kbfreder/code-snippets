#!/bin/bash

source .config

# script constants
UTIL_FILE_PATH=$SCRIPT_DIR/$UTIL_FILE

# arg defaults
step_name="PySpark"

usage="""
$(basename "$0")

Lots of arguments -- see code.
"""

while [ "$1" != "" ]; do
    case $1 in
        --cluster-id )          shift
                                cluster_id=$1
                                ;;
        --exec-mem )            shift
                                exec_mem=$1
                                ;;
        --driv-mem )            shift
                                driv_mem=$1
                                ;;
        --num-instances )       shift
                                num_instances=$1
                                ;;
        --script )              shift
                                script=$1
                                ;;
        --script-args )         shift
                                script_args=$1
                                ;;
        --step-name )           shift
                                step_name=$1
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
        * )                     echo "Error!"
                                echo "$usage"
                                exit 1
    esac
    shift
done

# echo $cluster_id


script_args_with_commas=${script_args//[ ]/,}

args=spark-submit,--deploy-mode,cluster,--conf,spark.yarn.maxAppAttempts=1,--conf,spark.dynamicAllocation.enabled=false,--conf,spark.executor.cores=5,--conf,spark.driver.cores=5,--conf,spark.executor.memoryOverhead=2g,--conf,spark.driver.memoryOverhead=2g,--conf,spark.executor.memory=$exec_mem,--conf,spark.driver.memory=$driv_mem,--conf,spark.executor.instances=$num_instances,--py-files,$UTIL_FILE_PATH,$SCRIPT_DIR/$script,$script_args_with_commas


# echo "Adding step $step_name to cluster $cluster_id"
cmd_out_sid=$(aws emr --profile $AWS_PROFILE add-steps\
    --cluster-id $cluster_id \
    --steps \
Name=$step_name,\
Type=CUSTOM_JAR,\
Jar="command-runner.jar",\
ActionOnFailure=TERMINATE_CLUSTER,\
Args=[$args] \
    --query 'StepIds'
)
step_id=$(echo $cmd_out_sid | sed 's/^"\(.*\)"$/\1/')
echo $step_id
