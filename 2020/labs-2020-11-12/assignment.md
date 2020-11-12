
# dynamic library overriding open/read/write

- implement a library with these calls: `open`, `read`, `write`, `close`
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
    - `SIGUSR1` - print number of workers created so far to `stderr`
  - verify with pstree(1)/ptree(1) run on parent's pid one it starts running
    - this is automatic thanks to the pipe semantics: reader and writer randezvous
```
    read pid </tmp/pool_fifo && while [ 1 ]; do pstree -p $pid; sleep 1; done
```

# shared memory and pipe

- usage: `./a.out <file_to_mmap> <string>`
- file contents: `| length | byte_0 | byte_1 | ... | byte_N |`
  - e.g. `| 5 | h | e | l | l | o |` 
    - note: there is no terminating zero byte
- parent creates the file sufficiently large to hold the string (sans the terminating zero)
  - make sure the length fits one byte

sequence:
  1. parent: creates the file
  1. parent: forks a child
  1. parent: mmaps the file, writes the contents to memory
  1. parent: writes 1 string to the pipe to notify the child
  1. child: reads one char from the parent (via pipe)
  1. child: mmaps the same file
  1. child: read the memory, print the string to `stdout`
  1. cleanup - `wait()`, `unmap()`, ...
  
Try with both `MAP_SHARED` and `MAP_PRIVATE` flags.

Replace the pipe with signal.
