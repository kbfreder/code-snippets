#!/bin/bash
#--------------------------------------
# if no argument given, 'd' defaults to yesterday's date

# the `-z` argument checks for an empty string
if [ -z "$1" ]
then
    echo "No argument supplied; using yesterday's date"
    d=$(date --date '-1 day' +%Y-%m-%d)
else
    d=$1
fi

echo "Date = $d"

#--------------------------------------
# sequential / ordered args

# check the number of arguments passed with `$#`
if [ $# -eq 0 ]
then
    echo "No arguments passed"
else
    # do things with the arg
    first=$1
    second=$2
    # etc
fi

#--------------------------------------
# loop through args, looking for flags

#!/bin/bash

usage="$(basename "$0") [-d date] [-m] [-h] -r required_param -- runs a neat program"

# if no argument, use yesterday's date 
d=$(date --date '-1 day' +%Y-%m-%d)
mini=false

while [ "$1" != "" ]; do
    case $1 in
        -r | --reqd )           shift
                                r=$1
                                ;;
        -d | --date )           shift
                                d=$1
                                ;;
        -m | --mini )           mini=true
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
        * )                     echo "$usage"
                                exit 1
    esac
    shift
done

if [[ $mini = true ]]
then
    python3 py_file.py -d $d --mini
else
    python3 py_file.py -d $d
fi

#----------------------------------
# a more better way to handle multiple optional args

usage="$(basename "$0") [-d date -b bucket -hb -hf] [-h]  -- runs eval_flow_bucket.py

# where:
#     -d   date in YYYY-MM-DD format (default is yetserday)
#     -b   bucket in HH:MM format
#     -hf  days forward from date to get honeynet logs
#     -hb  days back from date to get honeynet logs
#     -gn  include Greynoise scanner data
#     -s   save mini training data
#     -v   verbose output
#     -t   test mode
#     -h   show help text
# "

# set defaults for boolean args
verbose=false
test=false
save=false
gn=false

# parse args
while [ "$1" != "" ]; do
    case $1 in
        -d | --date )           shift
                                d=$1
                                ;;
        -b | --bucket )         shift
                                b=$1
                                ;;
        -hf )                   shift
                                hf=$1
                                ;;
        -hb )                   shift
                                hb=$1
                                ;;
        -gn | --greynoise )     gn=true
                                ;;
        -s | --save )           save=true
                                ;;
        -v | --verbose )        verbose=true
                                ;;
        -t | --test )           test=true
                                ;;
        -h | --help )           echo $usage
                                exit
                                ;;
        * )                     echo $usage
                                exit 1
    esac
    shift
done

# define base / default args
args="-d $d -b $b -hb $hb -hf $hf"

if [[ $verbose = true ]]
then
    args+=" -v"
fi

if [[ $test = true ]]
then
    args+=" -t"
fi

if [[ $save = true ]]
then
    args+=" -s"
fi

if [[ $gn = true ]]
then
    args+=" -gn"
fi

echo "Bash Script args: $args"