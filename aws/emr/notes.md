

## Creating a cluster
- `create-cluster.sh`: works
    - doesn't use any local config / .json files
    

## Adding a step
- successfully did so using a combination of the command line and `step_def.json`:
    > aws emr --profile ml-data-pn add-steps --cluster-id j-308XCCAEBCXAW --steps file://step_def.json
