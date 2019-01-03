1) warm-up: report divisors of numbers in range [1, N]
   - create M threads (start with M = number of online CPUs in the system as reported by sysconf(3)
     where each thread continues processing until there is some work to do
     - or make it a tunable (a define or program option) and see what works best on given system
   - main thread will report:
     - the best result found so far
     - the overall progress in percent (use \r to refresh the terminal)

  - hints/questions:
    - use refactoring to avoid long functions
    - use condition variable (one is enough)
    - how many mutexes do you need actually ?
    - start with single threaded program so that you can check the correctness (and debug easier)

  - check: [1, 100000]: the winner is 83160 that has 128 divisors

  - variant: make this code generic so any sort of job can be used (e.g. convert this to parallelized
           port scanner/downloader/web crawler)

2) rewrite https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/non-blocking-connect.c 
   to use threads instead of non-blocking connect
   - create as many threads as there are addresses to connect to
   - deal with the timeout appropriately: use a signal handler and terminate/cancel still running threads
     - will need to keep track of the thread work state and processed address
   - make sure to perform cleanup (esp. closing the file descriptors)
     - so that the program can be converted into library calls which can be repeatedly used in the same program
       - this has other consequences: instead of exiting, terminate other threads and propagate the error value
     - use cleanup routines so that the cleanup can be generic
       - gotcha: pthread_cleanup_* are usually implemented as macros
   
   - variant: create up to MAX threads, use a queue to manage the work
              - insert addresses into the queue as they are returned from resolving library calls so that 
                the address family precedence is preserved
              - need to correctly report yet unprocessed items on timeout
              
   - variant: parallelize the resolving part too
            - each worker thread will spawn multiple connect threads (or enqueue jobs if working with the previous variant
              as a basis) based on resolved addresses.
