#!/bin/bash

cluster_id=$1

PROFILE=ml-data-pn

aws emr --profile $PROFILE add-step \
--cluster-id $cluster_id \
--steps \
Name="test-app",\
Type=CUSTOM_JAR,\
Jar="command-runner.jar"\
ActionOnFailure=CONTINUE,\
Args=spark-submit,--deploy-mode,cluster,--conf,spark.dynamicAllocation.enabled=false,\
s3://tvlp-ds-users/kendra-frederick/scripts/hello_world.py,--input,"2023-02-01"
