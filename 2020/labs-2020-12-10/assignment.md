# thread pool

usage: `./a.out <number_of_threads>`

- dynamically allocate number of worker threads and keep the count of threads
  the same even if some of them exit
  - the threads can sleep for a random amount of time and then return
  - use specified (on command line) number of threads
  - variant: use sysconf(3) to get number of online processors and create the
    same number of threads
    - option: add a command line option to set integer scaling factor so the
      number of threads will be the number of processors multiplied by the
      factor

- use condition variable to notify that a thread is about to return so that main
  thread can resupply if needed
  - use `pthread_cleanup_push()` as a way to signal the condition variable
    before return from the worker thread function

- detach the threads so no joining is needed
  - using the thread attribute for `pthread_create()` is better as it avoids a
    race condition which happens when using `pthread_detach()` in thread
    function (if the thread returned/exited before the call to
    `pthread_detach()`)

- verify that the number of threads in the pool remains more or less the same

# thread pool with work queue

Add queue structure to the thread pool code for work distribution and thread(s)
that insert items to the queue (use e.g. `TAILQ` from `sys/queue.h`)

The worker thread waits for an item to be inserted to the queue, grab it
and process it and exit

# use thread pool work queue for latency monitoring

TBD
