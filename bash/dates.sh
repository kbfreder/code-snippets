
# ref: https://www.howtogeek.com/410442/how-to-display-the-date-and-time-in-the-linux-terminal-and-use-it-in-bash-scripts/


date_str=$(date +'%Y-%m-%d')

# yesterday's date
date -d "yesterday" '%Y-%m-%d'

# loop over dates
d=2022-10-04
end_d=2022-10-13 # +1 from actula finish

while [ "$d" != "$end_d" ]; do
    echo $d
    d=$(date -I -d "$d + 1 day")
done


# on a mac:
## date math
date -j -v +11d -f "%Y-%m-%d" $date_var +%Y-%m-%d

## convert date format:
date -j -f "%Y-%m-%d" $date_var +%Y-%m-%d
