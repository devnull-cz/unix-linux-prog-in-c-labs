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

  - variants:
    - make this code generic so any sort of job can be used (e.g. convert this to parallelized port scanner/downloader/web crawler)
    - pass the information about the best number to the main thread so that no single number is lost (i.e. use a queue)

  - example output:

```
	$ ./a.out 1 100000
	Num of CPUs: 8
	n1=1 n2=100000
	Created 8 threads.
	(0%) best number so far 6, has 4 divisors
	(0%) best number so far 12, has 6 divisors
	(0%) best number so far 24, has 8 divisors
	(0%) best number so far 36, has 9 divisors
	(0%) best number so far 48, has 10 divisors
	(0%) best number so far 60, has 12 divisors
	(0%) best number so far 120, has 16 divisors
	(0%) best number so far 180, has 18 divisors
	(0%) best number so far 240, has 20 divisors
	(0%) best number so far 360, has 24 divisors
	(0%) best number so far 720, has 30 divisors
	(0%) best number so far 840, has 32 divisors
	(1%) best number so far 1260, has 36 divisors
	(1%) best number so far 1680, has 40 divisors
	(2%) best number so far 2520, has 48 divisors
	(5%) best number so far 5040, has 60 divisors
	(7%) best number so far 7560, has 64 divisors
	(10%) best number so far 10080, has 72 divisors
	(15%) best number so far 15120, has 80 divisors
	(20%) best number so far 20160, has 84 divisors
	(25%) best number so far 25200, has 90 divisors
	(27%) best number so far 27720, has 96 divisors
	(45%) best number so far 45360, has 100 divisors
	(50%) best number so far 50400, has 108 divisors
	(55%) best number so far 55440, has 120 divisors
	(83%) best number so far 83160, has 128 divisors
	Job done, joining all the threads now.
	Best number: 83160 (divisors 128)
```

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
   
   - sub-variant: it does not mean that all the connect() calls are in progress once all the threads start running, i.e. after all the pthread_create() calls complete. This might matter if the timeout is low (use setitimer(2) to get sub-second timeouts) or there is high number of threads. The main thread should start the timer only after all the connections are initiated.
   
   - variant: create up to MAX threads, use a queue to manage the work
              - insert addresses into the queue as they are returned from resolving library calls so that 
                the address family precedence is preserved
              - need to correctly report yet unprocessed items on timeout
              
   - variant: parallelize the resolving part too
            - each worker thread will spawn multiple connect threads (or enqueue jobs if working with the previous variant
              as a basis) based on resolved addresses.
