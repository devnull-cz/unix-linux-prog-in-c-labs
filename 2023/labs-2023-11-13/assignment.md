# Debugging (networking) code
  - make sure there are no file descriptor leaks (e.g. connect to the server enough times so that any leakage will hit the maximum limit imposed by `ulimit`)
    - can also be observed via `lsof` or via `/proc`
  - `strace` or `truss` can help you see problems when passing structures to syscalls
  - gdb (compile with -g)
  - `netstat` / `route`
    - use `netstat -peanut` to display which connections belong to which process
  - `assert()`
  - `DEBUG()` macro (variadic)
  - use Netcat / Socat for testing/probing
  - traffic dump (`tcpdump` or `tshark` or `snoop` or Wireshark)
  - firewall
    - to simulate unreachable hosts
    - some firewalls (e.g. PF on OpenBSD) can simulate packet loss with certain probability
  - tools to simulate certain latency and/or bandwidth
  - syscall error injection (`strace` can do it)

# TCP experiments

Try the programs in https://github.com/devnull-cz/unix-linux-prog-in-c-src/tree/master/tcp

- how does the TCP handshake look like ?
  - why there is a handshake at all ?
- what happens "on the wire" with established TCP connection if a client process with established connection is terminated ?
  - RST or FIN ?
- what happens if server writes to a socket that is associated with client that has disconnected in the mean time ?
  - use connect.c and simple echo server (slow down writes in server)
- what happens for TCP server side socket without the `SO_REUSEADDR` socket option ? when is it relevant ?
  - use `netstat` to observe the connections
- how many TCP connections does the server accept after `listen()` and before `accept()` ?
  - does it match the `backlog` argument of `listen()` ?
  - modify `connect.c` to establish number of connections and sink server and experiment with listen backlog value
- how long does it take for `connect()` to time out when connecting to unreachable service ? (i.e. service that drops packets, not a service that refuses connections)
  - modify `connect.c`
- what happens on the network when `shutdown()` is called with read or write only flag ?
- what happens if `read()` from network socket is interrupted with a (handled) signal (say `SIGTERM` or `SIGINT`)
  - use TCP sink server and simple connect
  - see `atomicio()` in the OpenSSH source code

# Simple TCP exec server with descriptor redirection

Implement a program that will start listening on a specified TCP port and address.
It will handle one connection at a time. Once current connection is closed,
new one can be accepted.
```
   usage: ./a.out <address> <port> <program> [arguments]
```
Once a connection is accepted, the server will redirect `std{in,out,err}` to the network
connection and fork+exec the program.

## Notes/constrains:
 - use numeric IPv4 address and port for the time being. Once the lecture is past address resolution APIs (in particular `getaddrinfo, getnameinfo`), return back and fix the program so that it is address family agnostic.
 - use netcat as a client for testing
 - the executed program can be e.g. a shell. In that case the program will become de facto backdoor therefore for testing in non segregated network environment it is highly advisable to let the server listen only on localhost addresses (also see the allowed address variant below)
 - networking APIs that are sufficient (besides the usuall read/write/printf/etc.): `socket, bind, listen, accept, setsockopt` (for `SO_REUSEADDR`)

## Variants:
   - restrict clients based on IP address
```
   usage: ./a.out <address> <port> <allowed_address>
```
   - allow more simultaneous connections (both echo and shell)
   - the whitelist of IP addresses allowed to spawn a shell will be read from a file
   - the whitelist can consist of IP prefixes
   - make the server check a shared secret in the echo mode first and only if it matches (plus the IP address match) will it switch to shell mode
