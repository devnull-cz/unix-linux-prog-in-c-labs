# Slightly happy eyeballs problem

Parallel TCP connect() for hostnames with multiple IP addresses

variant: "primitive eyeballs" (draft-ietf-v6ops-happy-eyeballs analogy)

Write function:

```C
    int multi_connect(char *hostname, char *port, bool getall, unsigned int timeout);
```

where `hostname`/`port` is the specification of the target service to which the
client has to connect to. `timeout` is maximum time in milliseconds to wait for
connection establishment for given IP address. The default value for testing
should be 5000 ms.

`getall` is boolean value that states whether to wait till the timeout or grab
first functional connection.

Required features:
  - the function will initiate TCP connect to all addresses for given hostname
    "simultaneously"
  - if any of these connections is successfully established and  the `getall`
    parameter is false, the function immediatelly returns the file descriptor
    for the new connection
  - if none connect was successful, -1 is returned
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

