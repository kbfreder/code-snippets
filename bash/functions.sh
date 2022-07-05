

function git_del_branches {
    pattern=$1
    im=$2

    usage="git_del_branch -p pattern [-i] 
    Match and delete git branches that match <pattern>. 
    Use the -i (--inverse) flag to delete branches that do
    not match <pattern>"

    if [ "$pattern" = "-h" ]; then
        echo "$usage"
    else

        if [ "$im" = "" ]; then
            invert=false
        else
            invert=true
        fi

        if $invert; then
            git branch | grep -v "$pattern" | xargs git branch -D
        else
            git branch | grep "$pattern" | xargs git branch -D
        fi
    fi
}
