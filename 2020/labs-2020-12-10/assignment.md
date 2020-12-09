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
  - use command line tools

# thread pool with work queue

Add queue structure to the thread pool code for work distribution and thread
that insert items to the queue (use e.g. `TAILQ` from `sys/queue.h`).

usage: `a.out <thread_count> <number_of_items>`

The producer thread will generate set of random integers up to the given count,
insert them to the queue.

Each worker thread waits for an item to be inserted to the queue, grab it,
sleep for given number of seconds and exit.

# web scraper

Uses the code produced for the above tasks as a foundation.

usage: `a.out <input_file> <output_file>`

The work queue will be populated with request specifications from a file.
The file contents will look like this:
```
hostname#port/foo/bar
ip_address#port/x/y/z
...
```

The requests should be processed by the workers as the file is read.
Do not make any assumptions about the length of the input file (e.g. that it
will fit into memory). The queue should be limited in length. The limit should
be higher than the pool size.

Each worker will get the specification, makes a HTTP GET request according to
the specification, counts the number of bytes in the returned data and appends
the result to the output file.

The format of the output file will look like this:
```
hostname#port/foo/bar|42
ip_address#port/x/y/z|NA
...
```

The ordering of the lines in the output file is arbitrary. If the connect or the
GET request was not successful, the entry will have `NA`.

## graceful termination

When the program receives the `SIGINT` signal, it should gracefully terminate 
the current operations. I.e. the currently running workers are left to finish
however no new jobs are started. Then the workers are made to exit.
