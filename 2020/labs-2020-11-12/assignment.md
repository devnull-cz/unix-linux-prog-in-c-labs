
# dynamic library overriding open/read/write

- implement a library with 3 calls: `open`, `read`, `write`
- for each file descriptor opened the library will count the bytes read/written
- on close(), print the byte counts to `stderr`
- hint: in each function, use `RTLD_NEXT` to call the original implementation
  from libc after it does the needed processing
  - note that `open` is variadic function
- to test, use `LD_PRELOAD`

# process pool with signals

  - usage: `./a.out config_file`
  - on startup: read config file (contains single number N in text form),
    fork N processes, if one of them dies, fork a new one so that
    there is always approx. N processes around.
    - each child process will loop + random sleep + print its PID to stderr and exit
    - the parent will print its PID to a named pipe
      - create the named pipe beforehand with mkfifo(1)
  - signal handling:
    - `SIGHUP` - reload N from the config file
    - `SIGUSR1` - print current number of workers to `stderr`
  - verify with pstree(1)/ptree(1) run on parent's pid one it starts running
    - this is automatic thanks to the pipe semantics: reader and writer randezvous
```
    read pid </tmp/pool_fifo && while [ 1 ]; do pstree -p $pid; sleep 1; done
```
