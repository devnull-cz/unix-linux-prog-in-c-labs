# Leaky

write a program that leaks fds on purpose, by calling open() or dup() in a endless cycle.
Observe when the respective syscall will start returning -1. What is the `errno` value ?

Retrieve the limit of open file descriptors using `getrlimit()` and `sysconf()`. Then raise the limit using
`setrlimit()` and see if it had any effect (it should).

Q: how to debug file descriptor leaks ?

# File API: `cat`

Implement a `cat` command (like in `read/cat.c` but do **not** look at that code
until you have finished and verified your version).

```
./cat file1 [file2 [file3 ... ] ]
```

To verify, cat a few files with your binary and then `/bin/cat`, then `diff` it.

```
$ dd if=/dev/urandom bs=1k count=128 of=data
$ ./a.out /etc/passwd data /etc/passwd > output1
$ /bin/cat /etc/passwd data /etc/passwd > output2
$ diff output1 output2
$ echo $?
0
```

## Variant: allow zero arguments

usage: `./cat [file ...]`

Also, allow `-` to be specified as file, reading standard input in such case.

# `lseek`

Write an X cross to a file.  The first argument is the size of the rectangle.

```
$ ./xcross 10 outputfile
$ cat outputfile
x........x
.x......x.
..x....x..
...x..x...
....xx....
....xx....
...x..x...
..x....x..
.x......x.
x........x
```

- you can assume (or enforce in the program) that the number is even and bigger or equal to 4
- if the file does not exist, create it. If it exists, truncate it.
- use a single `write` to fill the file with dots (`.`)
- use `lseek` and `write(.., .., 1)` to write the `x` characters and the
  newlines (`\n`)
- that is, do **not** write the file in a single loop, printing either `.`, `x`,
  or `\n`

# Redirection

Implement:

```
$ cat <infile >outfile
```

via:

```
$ ./a.out infile outfile
```

- do the redirection in your code, create or truncate the `outfile` if needed
- then implement a simple loop that reads from file descriptor `0` and writes to
  `1` until `read` returns 0 (or an error).
- verify with `diff` that `infile` and `outfile` are identical

# retouch

Implement variant of touch(1) with implicit `-r`, `-a` and `-m`.
That is, write a program with the following usage:
```
./retouch ref_file dst_file
```
That will read the access/modified time stamps from `ref_file` and apply
them to `dst_file`. Create `dst_file` if it does not exist.

This will make it easy to preserve times on modification/access like so:
  - `retouch orig_file time_file`
  - access/change `orig_file`
  - `retouch time_file orig_file`

Try with multiple calls that modify the time values, observe different levels of
precision.
