
# multiple alarm scheduler

Design a solution for multiple alarms/callbacks in multithreaded environment. Each alarm will have the following properties:
  - number of seconds  after which the alarm expires
    - starting from the point the alarm was added
  - argument (`void *`)
  - callback function (`void (*callback)(void *);`)

Once the alarm expires, the callback function will be called with given argument. It can be expected that potentially many threads will register
alarms at once. The precision is seconds is fine.

You can start with simple/naive implementation and then refine it to a more effective (and possibly sophisticated) one.
The sound implementation should be using some of the thread synchronization mechanisms explained in the lecture.

Ideally write a set of unit tests for the functionality.
