# if [ $? -eq 0 ]; then exit 0; else exit 1; fi
if [ $? -eq 0 ]; then "Exit 0"; else echo "Exit 1"; fi