# Unix/Linux Programming in C, NSWI015, Labs, Oct 22, 2020

# foreword
- **always** compile with `-Wall -Wextra`

- **always** fix all the warnings before moving on

- for this lecture and labs, **never** use `fopen`, `fread`, `fwrite` etc.  Not
  today, not during any other lab sessions nor the exam.  Use syscalls `open`,
  `read`, `write`, etc.
	- there is nothing wrong with the standard C lib functions, quite the
	  contrary, but this lecture is about mastering the underlying
	  syscalls).

# getopt
- check out `unix-linux-prog-in-c-src/getopt/getopts.sh`, then write the same
  functionality in C.  Feel free to compile `getopt.c` and execute it but do not
  look at the source code until you finish your implementation.

```
$ ./getopts.sh
usage: getopts.sh command [-c code] [filename [filename [...]]]

$ ./getopts.sh boot -c 11 xxx yyy
first param (command): boot
option -c set to '11'
...done reading option arguments
filenames: xxx yyy

$ ./getopts.sh boot -x 11 xxx yyy
first param (command): boot
./getopts.sh: illegal option -- x
usage: getopts.sh command [-c code] [filename [filename [...]]]

$ ./getopts.sh attach
first param (command): attach
...done reading option arguments
no filenames entered
```

# simple cat
- implement a trival cat
- deal with error paths
- use the `err` and `errx` functions rather than the pure C way of `errno` and
  `strerror(errno)`

```
$ ./cat cat.c getopt.c ...
...

$ ./cat xxx
cat: xxx: No such file or directory
```

# simple cat modified
- read the whole line to a buffer first (check for `\n`)
- print out the buffer then
- max line length is 128 characters
- truncate longer lines
	- and test that truncation works as expected
- you can verify your implementation via redirecting the output to a file, then
  `diff` it with the original

# simple cp
- copy a file
- verify with `diff` it works as expected

```
$ ./cp /etc/passwd mypasswd
$ diff /etc/passwd mypasswd
$ echo $?
0
```

# create a file
- arg1 is a filename, arg2 is its mode
- verify the right mode was used
	- beware of the dog: 777 != 0777

```
$ ./touch myfile 0554
```

# reverse cat
- print a file reversed char by char
- you may use arg1 only
- mind the `\n` (see the example below)

```
$ echo "0123456789" > numbers.txt
$ cat numbers.txt
0123456789
$ ./rcat numbers.txt

9876543210$ echo .
.
$
```

# simple mkfile
- create a file of certain size
- `./mkfile [-p <char>] [-f] <size> <filename>`
- use `lseek` and write just 1 byte to make the file of the right site
- size is in bytes, use `k` as a suffix for kilobytes
- with `-p <char>`, fill out the whole file with the character
- without `-f`, `mkfile` will not overwrite an existing file.  You need the
  force flag to truncate an existing file on opening it.

# emulate `wc -l`

```
$ ./lc file1 file2
file1	30
file2	3
```
