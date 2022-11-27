# Tasks for NSWI095 labs, Nov 28, 2022

## POSIX semaphores

- do not use our code in the labs repo
- run multiple processes, all synchronizing with the same POSIX semaphore set
  with the n=1 (== binary semaphore)
- each process tries to lock using the semaphore
	- when locked, picks a random number of seconds, and each second prints
	  out its PID to the **standard error** output
- you should print helpful debugging messages
- test with multiple processes, each started from the same terminal.  One one
  should be writing at every single moment.

## `shlock`

- implement `shlock` or its subset.  See https://linux.die.net/man/1/shlock
