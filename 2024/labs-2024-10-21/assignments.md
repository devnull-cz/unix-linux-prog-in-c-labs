
# env (warm-up)

TODO:

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

# simple `find`

Implement:
```
find /etc/ -type f -name '*foo*'
```

Extra: implement the `-mount` option (i.e. do not descent into other
file-systems)

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
