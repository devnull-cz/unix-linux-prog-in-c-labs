# getcwd vs limits

1. find the value of `PATH_MAX` on your system
2. see if that corresponds to the value returned by `pathconf(homedir , _PC_PATH_MAX)` where `homedir` is your home directory
3. create path longer than `PATH_MAX`, `cd` into it and run a program which will call `getcwd()` with buffer longer than `PATH_MAX`
  - on Glibc, you can try passing `NULL` as a buffer. Trace the system calls of the program to see what happens under the hood.

NetBSD's getcwd (`lib/libc/gen/getcwd.c`):
```C

char *
__ssp_real(getcwd)(char *pt, size_t size)
{
    char *npt;

    /*
     * If a buffer is specified, the size has to be non-zero.
     */
    if (pt != NULL) {
        if (size == 0) {
            /* __getcwd(pt, 0) results ERANGE. */
            errno = EINVAL;
            return (NULL);
        }
        if (__getcwd(pt, size) >= 0)
            return (pt);
        return (NULL);
    }

    /*
     * If no buffer specified by the user, allocate one as necessary.
     */
    size = 1024 >> 1;
    do {
        if ((npt = realloc(pt, size <<= 1)) == NULL)
            break;
        pt = npt;
        if (__getcwd(pt, size) >= 0)
            return (pt);
    } while (size <= MAXPATHLEN * 4 && errno == ERANGE);

    free(pt);
    return (NULL);
}
```

musl libc (`src/unistd/getcwd.c`):
```C

char *getcwd(char *buf, size_t size)
{
	char tmp[buf ? 1 : PATH_MAX];
	if (!buf) {
		buf = tmp;
		size = sizeof tmp;
	} else if (!size) {
		errno = EINVAL;
		return 0;
	}
	long ret = syscall(SYS_getcwd, buf, size);
	if (ret < 0)
		return 0;
	if (ret == 0 || buf[0] != '/') {
		errno = ENOENT;
		return 0;
	}
	return buf == tmp ? strdup(buf) : buf;
}
```

# `namei`

Implement the `namei(1)` program. You can `strace` the execution of `namei` to see what syscalls it uses to perform its job.

Example output (on Ubuntu):
```
$ namei /usr/bin/java
f: /usr/bin/java
 d /
 d usr
 d bin
 l java -> /etc/alternatives/java
   d /
   d etc
   d alternatives
   l java -> /usr/lib/jvm/java-17-openjdk-amd64/bin/java
     d /
     d usr
     d lib
     d jvm
     d java-17-openjdk-amd64
     d bin
     - java
```
The `strerror()` is written next to the path component on error, e.g.:
```
$ namei $PWD/foo
f: /home/vkotal/MFF/Unix/unix-linux-prog-in-c-src/readdir/foo
 d /
 d home
 d vkotal
 d MFF
 d Unix
 d unix-linux-prog-in-c-src
 d readdir
 l foo -> /etc/nonexistent
   d /
   d etc
     nonexistent - No such file or directory
```

Bonus sub-task: implement the `-x` option to display the mount points, e.g.:
```
$ namei -x /media/vkotal/KINGSTON/UNIX/raw.c 
f: /media/vkotal/KINGSTON/UNIX/raw.c
 D /
 d media
 d vkotal
 D KINGSTON
 d UNIX
 - raw.c
```

Again, use `strace` to see what it does (esp. w.r.t. `/`).

# simple `find`

Implement:
```
find /etc/ -type f -name '*foo*'
```

Extra:
  - implement the `-mount` option (i.e. do not descent into other file-systems)
  - `-maxdepth`
  - `-mmin`

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
