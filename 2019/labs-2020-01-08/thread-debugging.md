
# Thread debugging

## GDB

- `info thread` - prints basic thread overview
- `break <linespec> thread <threadnum>` inserts breakpoint for particular thread
  - if the thread specification is omitted the breakpoint applies for
    all threads
  - use e.g. like so (this references structure member):
```
    break divisors.c:90 if res.divisors > 100 thread 7
```

NOTE: single stepping in one thread does not affect other threads, i.e.
lots of instructions can fly by elsewhere while single stepping a thread.

### switching between threads

`thread <threadnum>`

Commands like `backtrace` then take this into account.

### Applying a command to a group of threads

E.g.:
```
thread apply all bt
```

### Locking primitives

gdb does not seem to have special commands to query pthread synchronization primitives (such as [getting list of locked mutexes for given thread](https://stackoverflow.com/q/3983676/11582827)) however it will print e.g. mutex or condvar nicely:

```
(gdb) print g_best_mtx 
$8 = pthread_mutex_t = {
  Type = Normal,
  Status = Acquired, possibly with waiters,
  Owner ID = 14246,
  Robust = No,
  Shared = No,
  Protocol = None
}
(gdb) p g_best_cnd
$9 = pthread_cond_t = {
  Threads known to still execute a wait function = 1,
  Clock ID = CLOCK_REALTIME,
  Shared = No
}
```
