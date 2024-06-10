
# tar 
- note absense of `-` in command
tar cfz <tar-file-name.>.tar.gz <file or folder to zip>

## extract
- note presence of `-` in command
tar -xzvf archive.tar.gz -C /<dest>

## arguments:
- `-c`: create a new archive.
- `-f`: specify archive filename
- `-z`: use gzip compression
- `-x`: extract archive file to disk
- `-v`: verbose