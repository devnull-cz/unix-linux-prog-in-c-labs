# report divisors of numbers in range [1, N]
   - create M threads (start with M = number of online CPUs in the system as reported by sysconf(3)
     - each thread computes the divisors of given number and then proceeds to the next number
       - or make it a tunable (a define or program option) and see what works best on given system
     - compute the divisor count for given number using the most naive algorithm
       - cycle through the numbers and see if the division operation has no carry
     - each thread continues processing until there is some work to do
       - keep it simple: in the initial version, there is no need to deal with queues/stacks etc.

   - main thread will report:
     - the best result found so far
     - the overall progress in percent (use `\r` to refresh the terminal)

  - hints/questions:
    - use refactoring to avoid long functions
    - use condition variable (one is enough)
    - how many mutexes do you need actually ?
    - start with single threaded program so that you can check the correctness (and debug easier)

  - check: [1, 100000]: the winner is 83160 that has 128 divisors

  - variants:
    - make this code generic so any sort of job can be used (e.g. convert this to parallelized port scanner/downloader/web crawler)
      - this is where the queue/stack/list comes into consideration 
    - pass the information about the best number to the main thread so that no single number is lost (i.e. use a queue)
    - do not report percentage update for each computation update but only when
      new winner is found
      - this has consequences: main thread needs to be aware of terminating
	threads

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
