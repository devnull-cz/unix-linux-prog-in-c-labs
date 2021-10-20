# File API: cat

Implement a cat (like in `read/cat.c` but do not look at that code).

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

# lseek

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

- use a single `write` to fill the file with dots (`.`)
- use `lseek` and `write(.., .., 1)` to write the `x` characters and the
  newlines (`\n`)
- that is, do **not** write the file in a single loop, printing either `.`, `x`,
  or `\n`