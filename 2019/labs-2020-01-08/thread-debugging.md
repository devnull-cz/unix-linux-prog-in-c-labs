
# Thread debugging

## GDB

`info thread` - prints basic thread overview
`break <linespec> thread <threadnum>` inserts breakpoint for particular thread
  - if the thread specification is omitted the breakpoint applies for
    all threads
  - use e.g. like so:
```
break buffer.c:33 thread 7 if level > watermark
```

NOTE: single stepping in one thread does not affect other threads, i.e.
lots of instructions can fly by elsewhere while single stepping a thread.

### switching between threads

`thread <threadnum>

Commands like `backtrace` then take this into account.

### Applying a command to a group of threads


E.g.:
```
thread apply all bt
```


### Locking primitives

XXX
