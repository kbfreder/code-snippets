
d=2022-10-04
end_d=2022-10-13 # +1 from actula finish

while [ "$d" != "$end_d" ]; do
    echo $d
    d=$(date -I -d "$d + 1 day")
done
