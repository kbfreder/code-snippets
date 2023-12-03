

if [ "$fname" = "a.txt" ] || [ "$fname" = "c.txt" ]

mini=true

if $mini
then
    python3 py_file.py -d $d --mini
else
    python3 py_file.py -d $d
fi


if CLAUSE
then
    ACTION
elif CONDITION2
then 
    ACTION2
else 
    ACTION3
fi


"""
In Bash, the test command takes one of the following syntax forms:

test EXPRESSION
[ EXPRESSION ]
[[ EXPRESSION ]]
Copy
To make the script portable, prefer using the old test [ command, which is available on all POSIX shells. The new upgraded version of the test command [[ (double brackets) is supported on most modern systems using Bash, Zsh, and Ksh as a default shell.

To negate the test expression, use the logical NOT (!) operator. When comparing strings , always use single or double quotes to avoid word splitting and globbing issues.
"""