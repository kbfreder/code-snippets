#!/bin/bash

# pass 2 positional arguments to the script: the start date and the end date to process

PROFILE=ml-data-pn

aws emr --profile $PROFILE create-cluster \
--name kf-c6g.12xl_cli \
--release-label emr-5.36.0 \
--service-role EMR_DefaultRole \
--ec2-attributes InstanceProfile=EMR_EC2_DefaultRole,KeyName=kf-ml-data-pn \
--instance-groups file://instance_groups_raw_estream.json \
--auto-termination-policy IdleTimeout=900 \
--applications Name=Spark Name=Hadoop \
--log-uri s3n://aws-logs-149036431886-us-east-1/elasticmapreduce/ \
--tags for-use-with-amazon-emr-managed-policies=true \
--visible-to-all-users \
--auto-terminate \
--steps \
Name="KF-Estream-Agg",\
Type=CUSTOM_JAR,\
Jar="command-runner.jar",\
ActionOnFailure=TERMINATE_CLUSTER,\
Args=[spark-submit,--deploy-mode,cluster,--conf,spark.dynamicAllocation.enabled=false,--conf,spark.executor.cores=5,--conf,spark.driver.cores=5,--conf,spark.executor.memory=9g,--conf,spark.driver.memory=9g,--conf,spark.executor.instances=70,--jars,s3://tvlp-ds-users/kendra-frederick/scripts/argparse4j-0.8.1.jar,--class,LowestFaresEstreamAggWithArgs,s3://tvlp-ds-users/kendra-frederick/scripts/ti-lowestfaresestreamagg_2.11-2.2.0.jar,$1,$2]