# Unix/Linux Programming in C, NSWI015, Labs, Oct 22, 2020

90 minutes is probably not enough time to finish all these tasks which
essentially cover the last two lectures.  Please finish those when you have
time, it is important stuff.

Next labs should primarily cover only the lecture that comes right before.

# foreword
- **always** compile with `-Wall -Wextra`

- **always** fix all the warnings before moving on

- for this lecture and labs, **never** use `fopen`, `fread`, `fwrite` etc.  Not
  today, not during any other lab sessions nor the exam.  Use syscalls `open`,
  `read`, `write`, etc.
	- there is nothing wrong with the standard C lib functions, quite the
	  contrary, but this lecture is about mastering the underlying
	  syscalls).

- try to use the existing code from the unix-linux-programming-in-c-src repo as
  little as possible.  You can truly learn only by making mistakes and then fix
  those.

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
- it is OK to use a buffer of size 1
- you may just process one file and ignore other arguments
- mind the `\n` at the end of the file (see the example below)
	- may not be there but usually is

```
$ echo "0123456789" > numbers.txt
$ cat numbers.txt
0123456789
$ ./rcat numbers.txt

9876543210$ echo .
.
$
```

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

# Use `FD_CLOEXEC`
- verify how it works
- use the `exec` line (we will get propertly to the `exec` calls later this
  year) from `read/redirect.c`
- see for yourself that the following will not print the error (as 2 is already
  closed!)
- use `fcntl` with `FD_CLOEXEC` to fix it

```C
close(2);
execl("/nonexistent", "nonexistent", NULL);
err(1, "execl");
```

# `stat`
- print inode number for a file from argv1
- print the times as well.  Find functions to use to properly format the time
  values.

# directory listing
- write code to list all files in the current directory
- as before, but provide a type of each file
	- feel free to use `d_type` present on Linux and some other systems
- as before, but recursively enter directories.  Use indentation to follow the
  directory tree
