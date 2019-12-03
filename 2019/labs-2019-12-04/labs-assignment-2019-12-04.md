# Debugging (networking) code
  - make sure there are no file descriptor leaks (e.g. connect to the server enough times so that any leakage will hit the maximum limit imposed by `ulimit`)
    - can also be observed via `lsof` or via `/proc`
  - `strace` or `truss` can help you see problems when passing structures to syscalls
  - gdb (compile with -g)
  - `assert()`
  - `DEBUG()` macro (variadic)
  - traffic dump (`tcpdump` or `tshark` or `snoop` or Wireshark)

# TCP experiments

Try the programs in https://github.com/devnull-cz/unix-linux-prog-in-c-src/tree/master/tcp

- how do you know on server side that the client disconnected ?
  - use connect.c and simple echo server
- what happens if server writes to a socket that is associated with client that has disconnected in the mean time ?
  - - use connect.c and simple echo server (slow down writes in server)
- what happens without `SO_REUSEADDR` ? when is it relevant ?
  - use `netstat` to observe the connections
- how many TCP connections does server accept before `listen()` and `accept()` ?
  - modify connect.c to establish number of connections and sink server
- how long does it take for `connect()` to time out ?
  - use connect.c
- how does TCP handshake look like ?
- what happens if `read()` from network socket is interrupted with a (handled) signal
  - use TCP sink server and simple connect
  - see atomicio() in OpenSSH

# Simple TCP server with descriptor redirection

Implement a program that will start listening on a specified TCP port and address.
It will handle one connection at a time. Once current connection is closed,
new one can be accepted.
```
   usage: ./a.out <address> <port>
```
Once a connection is accepted, from the specified IP address,
the server will fork+exec a program and redirect `std{in,out,err}` to the network
connection.
Otherwise, it will behave as a echo server - what is read is written back
until the connection is closed.

## Notes/constrains:
 - the program has to support both IPv[46] but should use address family specific functions only when absolutely necessary (definitely not when creating/binding the socket !) i.e. only for address comparison after new connection was accepted.
 - port can be specified as a number or name of service
 - use netcat as a client for testing
 - for testing in non segregated network environment, it is highly advisable to let the server listen only on localhost addresses (and change the allowed address accordingly)
 - networking APIs that are sufficient (besides the usuall read/write/printf/etc.): socket, bind, listen, accept, getaddrinfo, getnameinfo, setsockopt (for `SO_REUSEADDR`)

## Variants:
   - restrict clients
```
   usage: ./a.out <address> <port> <allowed_address>
```
   - allow more simultaneous connections (both echo and shell)
   - the whitelist of IP addresses allowed to spawn a shell will be read from a file
   - the whitelist can consist of IP prefixes
   - make the server check a shared secret in the echo mode first and only if it matches (plus the IP address match) will it switch to shell mode
