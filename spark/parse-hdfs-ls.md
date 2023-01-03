
- in a jupyter cell run
!hdfs dfs -ls $inputPath > temp.txt

- the first line is header info we don't need
with open('temp.txt') as file:
    tempList = file.readlines()[1:]

- parse the output, to get just the file/path list
fileList = [x.split(" ")[-1].strip() for x in tempList]