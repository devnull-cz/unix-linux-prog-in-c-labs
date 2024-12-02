# The happy eyeballs algorithm (original)

Write function:

```C
    int multi_connect(char *hostname, char *port, unsigned int timeout);
```

that implement the algorithm specified in RFC 6555.

where `hostname`/`port` is the specification of the target service to which the
client has to connect to. `timeout` is maximum time in milliseconds to wait for
connection establishment for given IP address.

Required features:
  - the function will initiate TCP connect to the first IP address in the list
  - if the first connection is not successful within the `timeout` (say 300 ms), next AF in the list is tried
  - for the remaining iterations it will stick to the AF
  - if none of the connects were successful, -1 is returned
  - (for debugging) after max 1/10th of the timeout value the state of the
    connections is printed:
    - fd number
    - address family
    - state (timeout, connection refused, unsupported address family, success)

The Happy Eyeballs algorithm according to RFC 6555 sort of assumes that `getaddrinfo()`
returns IPv6 address first, then if not successful, it will proceed to IPv4 addresses in the list.
This can be made to work in generic way, e.g. if IPv4 addresses are preferred, it will try to connect
to the first IPv4 addresses, if that fails, it will try the different AF addresses.

The question is what should happen when the hostname resolves to a sequence of only IPv4 addresses (or only IPv6 addresses). 
Either it can try to connect to them in sequence or bail if the attempt to connect to the first one
(within the timeout) is not successful.

Note: at each step, there could be max. 2 simultaneous connection attempts in progress.

## Testing tips

The Linux lab machines at Mala Strana (`u-plX.ms.mff.cuni.cz`) are configured with both IPv4 and global IPv6 addresses.

A firewall (e.g. `iptables` on Linux or PF on BSD) can be used to simulate the connection delays.
Or, you can `LD_PRELOAD` library that wraps the `connect()` and delays the function return based on the `sockaddr` value
(so that it selectively delay given address or address family).

Example of hostname with A+AAAA DNS records:
  - www.kame.net
  - speed.cloudflare.com

## Variants

  - print also IP address of the remote end in the state dump
  - print also relative time from the connect() call for each socket

