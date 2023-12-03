#!/bin/bash

input=$1

PROFILE=ml-data-pn

# --auto-terminate \
# InstanceGroupType=CORE,InstanceCount=1,InstanceType=c6g.xlarge \

aws emr --profile $PROFILE create-cluster \
--name kf-test-cli \
--release-label emr-5.36.0 \
--service-role EMR_DefaultRole \
--ec2-attributes InstanceProfile=EMR_EC2_DefaultRole,KeyName=kf-ml-data-pn \
--instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m5.xlarge \
--auto-termination-policy IdleTimeout=900 \
--applications Name=Spark Name=Hadoop \
--log-uri s3n://aws-logs-149036431886-us-east-1/elasticmapreduce/ \
--tags for-use-with-amazon-emr-managed-policies=true \
--visible-to-all-users \
--steps file://step_def_ex.json
