#!/bin/bash

# load configs
source .config

# script constants
UTIL_FILE_PATH=$SCRIPT_DIR/$UTIL_FILE

# arg defaults
cluster_name="$USER_INITS-PCP"

usage="""
$(basename "$0")

Lots of arguments -- see code.
"""

while [ "$1" != "" ]; do
    case $1 in
        --core-family )         shift
                                core_fam=$1
                                ;;
        --core-size )           shift
                                core_size=$1
                                ;;
        --core-num )            shift
                                core_num=$1
                                ;;
        --master-family )       shift
                                master_fam=$1
                                ;;
        --master-size )         shift
                                master_size=$1
                                ;;
        --master-num )          shift
                                master_num=$1
                                ;;
        --cluster-name )        shift
                                base_cluster_name=$1
                                ;;
        --extra-bootstrap )     shift
                                extra_bootstrap=$1
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
        * )                     echo "$usage"
                                exit 1
    esac
    shift
done


if [ $master_fam  == "" ]; then
    master_fam = $core_fam
fi

if [ $core_fam  == "c6g" ]; then
    exec_mem="8g"
    if [ $master_fam == "m6g" ]; then
        driv_mem="8g"
    elif [ $master_fam == "c6g" ]; then
        driv_mem="5g"
    fi
elif [ $core_fam  == "m6g" ]; then
    exec_mem="19g"
    driv_mem="14g"
elif [ $core_fam  == "r6g" ]; then
    exec_mem="40g"
    driv_mem="30g"
else
    echo "Core family value: $core_fam not recognized. Please check spelling / that it exists in options"
    exit 1
fi

# The number of vCPU is consistent between different sizes of the c6g, m6g, and r6g
# instance families. If you need to use a different instance type, confirm that the
# following values still apply.
if [ $core_size  == "2xlarge" ]; then
    vcpu_per_inst=8
elif [ $core_size  == "4xlarge" ]; then
    vcpu_per_inst=16
elif [ $core_size  == "8xlarge" ]; then
    vcpu_per_inst=32
elif [ $core_size  == "12xlarge" ]; then
    vcpu_per_inst=48
else
    echo "Core size value: $core_size not recognized. Please check spelling / that it exists in options"
    exit 1
fi

# reserve one core for the driver, then divide by the number of cores per executor,
# which we fix at 5
## bash doesn't do floating point math, so this automatically rounds down for us
exec_per_inst=$(( ($vcpu_per_inst-1)/5 ))
# from this we can calculate the total number of executors across the cluster
num_instances=$(( ($exec_per_inst*$core_num)-1 ))


cluster_name="$USER_INITS-$base_cluster_name"
bootstrap_args="Name=InstallBoto3,Path=s3://tvlp-ds-users/kendra-frederick/scripts/bootstrap/install_boto.sh"


if [ "$extra_bootstrap" ]; then
    if [ $extra_bootstrap == 'pandas' ]; then
        bootstrap_args+=" Name=InstallPandas,Path=s3://tvlp-ds-users/kendra-frederick/scripts/bootstrap/install_pandas.sh"
    fi
fi


cmd_out_cid=$(aws emr --profile $AWS_PROFILE create-cluster \
    --name $cluster_name \
    --release-label emr-6.13.0 \
    --instance-groups InstanceGroupType=MASTER,Name="Master - 1",InstanceType=$master_fam.$master_size,InstanceCount=$master_num InstanceGroupType=CORE,Name="Core - 2",InstanceType=$core_fam.$core_size,InstanceCount=$core_num \
    --service-role EMR_DefaultRole \
    --ec2-attributes InstanceProfile=EMR_EC2_DefaultRole,KeyName=$EC2_KEY_PAIR \
    --auto-termination-policy IdleTimeout=900 \
    --applications Name=Spark Name=Hadoop \
    --log-uri s3n://aws-logs-XXXXX-us-east-1/elasticmapreduce/ \
    --tags for-use-with-amazon-emr-managed-policies=true tvpt:cluster-name=datascience-$AWS_USER_NAME.pn \
    --bootstrap-actions $bootstrap_args \
    --visible-to-all-users \
    --auto-terminate \
    --query 'ClusterId'
)
cluster_id=$(echo $cmd_out_cid | sed 's/^"\(.*\)"$/\1/')
echo $cluster_id $exec_mem $driv_mem $num_instances
