
PROFILE=ml-data-pn

aws emr --profile $PROFILE create-cluster file://cluster-config.json