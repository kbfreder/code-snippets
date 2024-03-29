aws emr create-cluster \
 --name "kf-jupyter-reduced" \
 --log-uri "s3n://aws-logs-149036431886-us-east-1/elasticmapreduce/" \
 --release-label "emr-5.36.0" \
 --service-role "EMR_DefaultRole_V2" \
 --ec2-attributes '{"InstanceProfile":"EMR_EC2_DefaultRole","EmrManagedMasterSecurityGroup":"sg-0f66e63d9c0bc0a66","EmrManagedSlaveSecurityGroup":"sg-072364a416673d10f","KeyName":"kf-ml-data-pn","AdditionalMasterSecurityGroups":[],"AdditionalSlaveSecurityGroups":[],"SubnetId":"subnet-02081f320cb5351ea"}' \
 --tags "for-use-with-amazon-emr-managed-policies=true" \
 --applications Name=Hadoop Name=Hive Name=JupyterEnterpriseGateway Name=Spark \
 --instance-groups '[{"InstanceCount":2,"InstanceGroupType":"CORE","Name":"Core - 2","InstanceType":"c6g.2xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}},{"InstanceCount":1,"InstanceGroupType":"MASTER","Name":"Master - 1","InstanceType":"m5.xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}}]' \
 --bootstrap-actions '[{"Args":[],"Name":"Custom action","Path":"s3://tvlp-ds-users/kendra-frederick/scripts/bootstrap/eda-bootstrap.sh"}]' \
 --steps '[{"Name":"pull-data","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Args":["spark-submit","--deploy-mode","cluster","s3://tvlp-ds-users/kendra-frederick/scripts/pull-sample-data.py"],"Type":"SPARK_APPLICATION"},{"Name":"pull-data","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Args":["spark-submit","--deploy-mode","cluster","s3://tvlp-ds-users/kendra-frederick/scripts/pull-sample-data.py"],"Type":"SPARK_APPLICATION"}]' \
 --scale-down-behavior "TERMINATE_AT_TASK_COMPLETION" \
 --ebs-root-volume-size "10" \
 --auto-termination-policy '{"IdleTimeout":900}' \
 --os-release-label "2.0.20220912.1" \
 --region "us-east-1"