#!/bin/bash

# =================================
# DATES
# =================================

# get X days from today, in GNU:
date --date '-90 days'

# default to yesterday's date
d=$(date --date '-1 day' +%Y-%m-%d)

# loop over dates
	# see gist

# =================================
# FILES
# =================================

# upload file to bastion
$REMOTE_DIR=/home/USERNAME/.local/share/jupyter/snippets
$BASTION01=ascbastion01.idc1.level3.com

scp -r ./*.py kfrederick@$BATION01:$REMOTE_DIR

# =================================
# MISC
# =================================

# math
- addition: `expr 5 + 5`
- multiplication: `expr 5 \* 5`

# increment
i=$((i+1))

# sequence
	# numbers
for i in `seq 22 28`
do
	echo $i
done

	# formatted numbers
for i in `seq -w 1 12`
do
	echo $i
done

	# date
start_date=2020-01-01
end_date=2020-01-05
d=$start_date

while [ "$d" != "$end_date" ]; do 
    echo $d
  	# d=$(date -d "$d + 1 day")

  # mac option for d decl (the +1d is equivalent to + 1 day)
    d=$(date -j -v +1d -f "%Y-%m-%d" $d +%Y-%m-%d)
done


# pipe output to a file
command > file 2>&1


# list filename in a dir
hdfs dfs -ls <path> | sed '1d;s/  */ /g' | cut -d\  -f8
ls -l <path> | sed '1d;s/  */ /g' | cut -d\  -f8


# increment through minutes:
	# uses 'epoch time'
	# ideal for checking if flow index files exist
time=0
epoch="1970-01-01 00:00:00 UTC"
while [[ $time -lt 86400 ]]; do
	hour=$(date -d "$epoch $time seconds" +"%H:%M")
	echo $hour
	((time+=300))
done


# quick git change

# Syntax: takoquick '<comment>'
function quicktako() {
	git add *
	if [ "$#" -lt 1 ]; then quoted_args="[Tako] minor changes" ; else quoted_args="[Tako] $(printf "${@}")" ; fi
	git commit -m "$(echo $quoted_args)" ; git rebase tako_mods ; maxbuff ; git push origin tako_mods
  #highbuff #<-- maxbuff
}


# loop over files in dir:

for filename in dir/*.csv; do # or: *.csv for files in current dir
	echo "$filename $(cat $filename | wc -l)
done

for filename in *.csv; do echo "$filename $(cat $filename | wc -l) done


# print out folder sizes in a directory (only one-level deep -- not sub-directories)
du -h -s <dir>/*