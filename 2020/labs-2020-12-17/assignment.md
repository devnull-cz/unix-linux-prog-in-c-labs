# Tasks for NSWI095 labs, Dec 17, 2020

## thread synchronization

Create multiple threads with the main thread, in a loop, putting a random number
into a shared variable (maximum is the number of threads), and the thread with
that ID will wake up and print its number.  Other threads may wake up as well
but only the right thread may print the message.

Use proper synchronization.

## barrier

See pthreads/implement-barrier.c and understand the hang.  Then fix it.  After
you successfully fix it, check out pthreads/implement-barrier-fixed.c and
compare your solution to ours.
