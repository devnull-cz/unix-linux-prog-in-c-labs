# happy eyeballs problem

Write function:

```C
    int multi_connect(char *hostname, char *port, unsigned int timeout);
```

where `hostname`/`port` is the specification of the target service to which the
client has to connect to. `timeout` is maximum time in milliseconds to wait for
connection establishment for given IP address.

`getall` is boolean value that states whether to wait till the timeout or grab
first functional connection.

Required features:
  - the function will initiate TCP connect to the first IP address in the list
  - if the first connection is not successful within the `timeout`, next AF in the list is tried
  - if none of the connects were successful, -1 is returned
  - (for debugging) after max 1/10th of the timeout value the state of the
    connections is printed:
    - fd number
    - address family
    - state (timeout, connection refused, unsupported address family, success)

The true Happy Eyeballs algoritmus according to RFC 6555 connects to the IP
addresses in sequence, with timeout of 300 ms. If the first connection does not
succeed in 300 ms, it will try the next distinct address family. If the 1st
connect attempt succeeds in the meantime, it will use that.
If the 2nd is not successful, it will try the addresses from the list regardless
of AF with timeout of 5 seconds.

Note: at each step, there could be max. 2 simultaneous connection attempts in progress.

Example of hostname with A+AAAA DNS records: www.kame.net

Variants:
  - print also IP address of the remote end in the state dump
  - print also relative time from the connect() call for each socket

