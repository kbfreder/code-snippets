
PROFILE=ml-data-pn

# --use-default-roles \
# --ec2-attributes file://ec2_attributes.json


aws emr --profile $PROFILE create-cluster \
--name kf-test-cli \
--release-label emr-5.36.0 \
--service-role EMR_DefaultRole \
--ec2-attributes InstanceProfile=EMR_EC2_DefaultRole,KeyName=kf-ml-data-pn \
--instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m5.xlarge \
InstanceGroupType=CORE,InstanceCount=2,InstanceType=c6g.xlarge \
--auto-termination-policy IdleTimeout=900 \
--applications Name=Spark Name=Hadoop \
--log-uri s3n://aws-logs-149036431886-us-east-1/elasticmapreduce/ \
--tags for-use-with-amazon-emr-managed-policies=true \
--visible-to-all-users