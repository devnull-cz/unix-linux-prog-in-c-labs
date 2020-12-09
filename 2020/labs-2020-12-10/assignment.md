# thread pool

usage: `./a.out <number_of_threads>`

- dynamically allocate number of threads and keep the count of threads the same
  even if some of them exit
  - the threads can sleep for a random amount of time and then return
  - use specified (on command line) number of threads
  - variant: use sysconf(3) to get number of online processors and create the
    same number of threads
    - option: add a command line option to set integer scaling factor so the
      number of threads will be the number of processors multiplied by the
      factor

- use condition variable to signal that thread is about to return so that main
  thread can resupply if needed
  - use `pthread_cleanup_push()` with `pthread_exit()` or just signal the
    condvar before return
    - beware: the `pthread_cleanup_pop`/`pthread_cleanup_push` can be
      implemented as macros, see the man page for details on how to use them
      properly

- detach the threads so no joining is needed
  - better using the thread attr for `pthread_create()` to avoid race condition
    which happens when using pthread_detach() in thread function
    (if the thread returned before call to pthread_detach())

- variant: use atomic integer and a signal to poke the main thread
  - the signal should be real-time or use sigqueue/siginfo not to lose events

- verify with ps(1) (use -L on Linux) that the number of threads in the pool
  remains more or less the same

# thread pool with work queue

Add queue structure to the thread pool code for work distribution and thread(s)
that insert items to the queue (use e.g. `TAILQ` from `sys/queue.h`)

The worker thread waits for an item to be inserted to the queue, grab it
and process it and exit

# use thread pool work queue for latency monitoring

TBD
