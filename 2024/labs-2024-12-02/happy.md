# happy eyeballs problem (original)

Write function:

```C
    int multi_connect(char *hostname, char *port, unsigned int timeout);
```

that implement the algorithm specified in RFC 6555.

where `hostname`/`port` is the specification of the target service to which the
client has to connect to. `timeout` is maximum time in milliseconds to wait for
connection establishment for given IP address.

`getall` is boolean value that states whether to wait till the timeout or grab
first functional connection.

Required features:
  - the function will initiate TCP connect to the first IP address in the list
  - if the first connection is not successful within the `timeout` (say 300 ms), next AF in the list is tried
  - for the next iterations it will stick to the AF
  - if none of the connects were successful, -1 is returned
  - (for debugging) after max 1/10th of the timeout value the state of the
    connections is printed:
    - fd number
    - address family
    - state (timeout, connection refused, unsupported address family, success)

The Happy Eyeballs algorithm according to RFC 6555 sort of assumes that `getaddrinfo()`
returns IPv6 address first, 

When the hostname resolves to a sequence of only IPv4 addresses, it should try to connect to them in sequence.

Note: at each step, there could be max. 2 simultaneous connection attempts in progress.

Example of hostname with A+AAAA DNS records: www.kame.net

Variants:
  - print also IP address of the remote end in the state dump
  - print also relative time from the connect() call for each socket

