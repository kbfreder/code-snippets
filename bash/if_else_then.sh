

if [ "$fname" = "a.txt" ] || [ "$fname" = "c.txt" ]

mini=true

if $mini
then
    python3 py_file.py -d $d --mini
else
    python3 py_file.py -d $d
fi