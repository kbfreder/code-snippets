


print contents of a file:
- `cat file.txt`

copy output of a command to a variable:
- `var=$(head readme)`

Adding new path to PATH variable
- `export PATH=$PATH:~/path/to/new/thing`

search for string in file in directory:
- `grep -r '<search string>' <path>`

list files that *don't* match a pattern
- `ls --ignore=*.txt`

replace file contents with text:
- `echo "<text>" > file.txt`

append text to file:
- `echo "<text>" >> file.txt`

opening a file named '-'
- `cat ./-`
    - i.e. specify full path of file with `./`

opening a file with spaces:
- `cat "./file with spaces"`

loop through files in current directory:
-  `for f in ./*; do echo "$f:"; cat $f; echo -e "\n"; done`

find file of a particular size:
- `find . -size 1033c`
- note that to get true bytes, we need to use the suffix 'c' for the `-size` argument of `find` command

print a specific line of a file:
- `sed -n -e <line_no>p <file>`
- ex: line 50 from file data.txt:
    - `sed -n -e 50p data.txt`

print (cat) the latest file in a folder
- `cat <folder>"$(ls -rt <folder>/ | tail -n1)"


## commands
### common
- find
    - online documentation: https://www.gnu.org/software/findutils/manual/html_mono/find.html
- wc: word count
    - `-l` lines only
    - `-w` words only
- file: print info about file type
- awk
- diff: differences between two file
    - usage: `diff <file1> <file2>`
    - output:
        <line affected in 1st file><action><corresponding line in 2nd file>
        < <text in 1st file>
        <line affected in 1st file><action><corresponding line in 2nd file> (or '----' if only a change)
        > <text in 2nd file>

        - example:
            3d2
            < this text was deleted from file1
            5a5
            > this line was added to file2

        - example: https://unix.stackexchange.com/questions/81998/understanding-of-diff-output

    - actions:
        - d = deletion
        - a = addition
        - c = change
- zip

        

### interwebs
- nc: netcat
    - https://www.tutorialspoint.com/unix_commands/nc.htm
    - https://www.computerhope.com/unix/nc.htm
    - "used for anything TCP / UDP under the sun"
    - flags
        - `-z`: report open ports (but do not try to connect)
        - `-v`: verbose mode (need in conjuction with -z)
- openssl: better for establishing secure (SSL) connections
    - usage: `openssl s_client -connect <url>:<port>`
    - https://www.feistyduck.com/library/openssl-cookbook/online/ch-testing-with-openssl.html

- curl: transfer data to/from a server
    - `-o` (output) or `>` (redirect): save output to a file
    - `-L`: follow redirects ("Location')

### encodings
- xxd: hex dump
- od: octal dump
- gzip & gunzup
- bzip2
- uuencode & uudecode
- tar: tar archive
    - t: table of contents in archive
    - x: extract
    - v: verbose. list files processed
    - f: archive file to use.
    - common usage: tar xvf <archive_file>