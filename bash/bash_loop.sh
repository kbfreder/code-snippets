#!/bin/bash


dir=/Users/kendrafrederick/Documents/Example/Flat_Folder
cd $dir
# touch new_file.txt

for i in `seq -w 1 50`
do
    fn=random_file_$i.txt
    # echo $fn
    touch $fn
done


for repo in "${repositories[@]}"; do
    {
        cp $USFJCS_ROOT_DIR/.env $USFJCS_ROOT_DIR/$repo/ 
    } || {
        echo "Could not find $repo locally"
    }
done