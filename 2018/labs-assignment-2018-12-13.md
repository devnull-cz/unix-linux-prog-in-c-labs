1) create a binary tree of threads

   usage: ./a.out number_of_layers
   
   e.g. for 3 it will look like this:
   
             o
            / \
          o     o
         / \   / \
        o   o o   o

  - the tree leaf nodes will sleep for random time (up to couple of seconds) and return
    - use `srandom(time())` and `random()`
  - all parent nodes will wait for their children
  - keep in mind that you do not need to know the total number of threads beforehand
  
  - use ps(1) to display info about the threads (-L on GNU, -M on BSD), e.g.:
```
$ ./a.out 3 &
[1] 51366
Thr#145158144 layer 2
Thr#145694720 layer 1
Thr#146231296 layer 1
Thr#147304448 layer 0
Thr#146767872 layer 0
Thr#147841024 layer 0
Thr#148377600 layer 0
$ ps -p $! -M
USER            PID   TT   %CPU STAT PRI     STIME     UTIME COMMAND
vladimirkotal 51366 s003    0.0 S    31T   0:00.00   0:00.00 ./a.out 3
              51366         0.0 S    31T   0:00.00   0:00.00 
              51366         0.0 S    31T   0:00.00   0:00.00 
              51366         0.0 S    31T   0:00.00   0:00.00 
              51366         0.0 S    31T   0:00.00   0:00.00 
              51366         0.0 S    31T   0:00.00   0:00.00 
              51366         0.0 S    31T   0:00.00   0:00.00 
```
  
2) Thread pool

   usage: `./a.out number_of_threads`

   - dynamically allocate number of threads and keep the count of threads the same even if some of them exit
     - the threads can sleep for a random amount of time
     - use specified (on command line) number of threads
     - variant: use sysconf(3) to get number of online processors and create the same number of threads

   - use condvar to signal that thread is about to return so that main thread can resupply if needed
     - use pthread_cleanup_push() with pthread_exit() or just signal the condvar before return
   
   - detach the threads so no joining is needed
     - better using the thread attr to avoid race condition when using pthread_detach() in thread function
   
   - variant: use atomic integer and a signal to poke the main thread
     - the signal should be real-time or use sigqueue/siginfo not to lose events

   - again, verify with ps(1) that the number of threads in the pool remains more or less the same
