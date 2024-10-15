# MQTT server specification

This is the official specification of the "[femto](https://en.wikipedia.org/wiki/Metric_prefix)"
MQTT server implementation. Why femto ? Because there are minimal MQTT implementations
out there, one of them called "nanoMQ" and the one specified here is sort of
two degrees of magnitude below, hence femto.

The purpose of this task is to learn the basics of Unix network programming
and debugging and also to get credits for the "Linux/Unix system programming in C"
class taught at the Mathematical physical faculty of Charles University, Prague.

The MQTT protocol is widely used for IoT (Internet Of Things) applications,
where the MQTT clients are often microcontrollers of small physical shape,
connected over possibly high latency networks, often powered by batteries.

For example, on my terrace I have a battery powered microcontroller
that wakes up periodically, gathers metrics from the attached sensors
(temperature/humidity/battery capacity) and sends them to MQTT broker.
See https://github.com/vladak/shield for details.
The metrics are then read by distinct MQTT client and stored in a time series
database which is then queried for data presentation and alerting by various tools.

The goal of this task is to write minimal MQTT server/broker from scratch.
*Minimal MQTT broker* means that the implementation is compliant to a subset
of the MQTT protocol specification so that it can provide commonly used
functionality.

The expectation is that the LOC sum of complete implementation should be around 1k,
definitely not longer than 2k even if you include lots of logging statements etc.
This is so that you get an idea of the size, not complexity.
Debugging network servers can sometimes require large amounts of time,
even though the code size is not that big.

## Changelog

This specification will likely have to be adjusted/completed. Here is the list of changes done:

- 2023/11/18: move the testing information to the `tests` subdirectory
- 2023/11/27: add a note about Remaining length for SUBSCRIBE/PUBLISH packets in the MQTT specification
- 2024/01/01: add note about RETAIN flag for the PUBLISH message
- 2024/01/05: add note on the provided tests
- 2024/10/15: add note on makefile syntax and running the server on different Unix systems

## Basic information

The server will communicate over plain text only, i.e. no TLS layer,
using TCP sockets, no authentication.

By default, the server will listen on TCP port 1883. Alternative port can be specified
with the `-p` command line option that supports numeric option argument.

### Compilation

There should be a `Makefile` that by default produces binary called `mqttserver` with the default target.
Ideally, use makefile syntax that is common across different `make` implementations,
so that the `make` can be run without relying e.g. on GNU or BSD extensions.
If you deem necessary to rely on specific `make` implementation, please state so in the comments in the makefile.

The `Makefile` should use the `$(CC)` macro for the compiler, so that the compiler
can be overridden.
This is important so that a lecturer can run the tests on submitted code
without fiddling around with files in student's repository.

The choice of the compiler is arbitrary, as long as the code can be compiled
using either Clang or GCC on the machines in the Unix lab at Malá Strana.

The code can be spread across multiple `.c` and `.h` files, although it is perfectly
fine to use just a single source code file.

The code should be written in strict C99, i.e. avoid GNU C extensions or such.
The compilation of the program should pass with `-std=c99 -Werror=pedantic` (GCC, Clang).

## Implementation

Firstly, when in doubt what about the specification, ask on the mailing list.
You will find pointer to the mailing list on the [course page](https://devnull-cz.github.io/unix-linux-prog-in-c/).

### General

Although the server will be primarily tested on Linux, it should be possible to run the server on different Unix systems,
because it relies on standard set of interfaces which should have the same behavior everywhere.
I will test the imlementation on Gentoo Linux in the lab, then possibly on different Unixes (macOS, OpenBSD, maybe Solaris).

It must be possible to restart the server gracefully even if there are lingering client connections present
at the time it is being terminated, i.e. it should not wait for the connections to close correctly
w.r.t. MQTT protocol.

The server does **not** have to be multiprocess/multithreaded. If you decided this is what you want to try,
it is recommended to implement the server as single threaded, make sure it passes the tests, submit the
assignment, then reimplement and resubmit.

The server must be address family agnostic, i.e. support both IPv4 and IPv6.
If a system supports IPv6, the server has to be able to accept connections for both address families
on all available interfaces/addresses in the system.

The client sockets can be all blocking, i.e. you can assume that read()/write() syscalls will
not block for inordinate amounts of time on average.

### MQTT

The basic specification is MQTT [version 3.1.1](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html).

[Appendix B](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718134)
of the specification contains all the items that have to be implemented (*MUST*)
in order to have a compliant implementation.

As said above, only a subset of features is to be implemented. Here is a list of features that are impacted:
  - Support QoS 0 only. This means that messages like `PUBREC`, `PUBREL` and `PUBCOMP`
    do not have to be handled.
  - None of the functionality given by the `CONNECT` message flags (as per 3.1.2.3 Connect Flags) has to be
    supported. E.g. the RETAIN flag, Will, Username/password, etc.
  - Likewise, the functionality related to the flags in the PUBLISH message (e.g. the RETAIN flag) does not have to be implemented
  - message delivery retry (4.4). Given that QoS > 0 is not to be implemented, this does not have to be implemented.
    Same goes for message ordering (4.6)

If an unsupported message or message with unsupported content is received, the server can close the connection.

The implementation should make every attempt to verify message content
based on the MQTT protocol specification.
There are some exceptions to this rule, though:
- UTF-8 string verification (per MQTT spec section 1.5.3) does not have to be performed

The topics are to be treated as opaque sequences of characters,
A topic containing wildcard characters (such as `#`) should be refused, i.e. the client disconnected.

#### Remaining length bug in the MQTT spec

It seems that the MQTT specificaion contains a bug w.r.t. the Remaining length (2.2.3).
For the SUBSCRIBE and PUBLISH packets the Fixed header example has `byte 2` instead of `byte 2...`
in sections 3.3.1 and 3.8.1, respectively. This might lead some to think that field should be 1 byte only.
The elipsis is signifying that the Remaining length can be encoded as multiple bytes like in the CONNECT packet
fixed header (section 3.1.1) where it is correctly specified with the elipsis.

### Choice of APIs

Stick to standard UNIX APIs (SUSv4) covered in the lecture. For example, avoid
non-standard/non-portable APIs such as epoll(7) or reallocarray(3) etc.

There are some exceptions though, such as err(3) family of functions.

Use `select()`/`poll()` to handle client connections and incoming data.
You may use these APIs for outgoing data as well.
Do not use any other mechanism to handle client connection or data events
(such as epoll etc.).

When in doubt, ask on the mailing list.

### Source code comments

The code should be commented so that the comments aid whoever reads it.
In particular, if there can be a doubt about interaction between pieces
of the program or when the choice of particular solution might not be clear
- it such cases a comment explaining the 'why' is invaluable.

On the other hand, too many trivial comments hurts readability.

### Coding style

As stressed multiple times during the lecture, using a coding style consistently
is good practice and helps in expedited evaluation of your program.

Also, using spaghetti code is reluctantly accepted but unwelcome.

### Error handling

If there is a way how to check for error of a library/system call, a check
should be present in the code with appropriate reaction.

For most of the error cases the server should report the problem to `stderr` and
try to recover/continue. In some cases it might make sense to exit the program.
For example, if `accept()` fails or if there is not enough memory.

Any error reporting should be as helpful as possible. For example for the above cases,
the program should attempt to report why `accept()` failed and how much memory was
being (re)allocated, respectively.

On `SIGINT`/`SIGTERM` the daemon should gracefully exit, i.e. closing active client connections.

## Debugging

Besides using a debugger (such as `gdb` or `lldb`), there are tools that can be
useful for debugging network program:
- system call tracing: `strace` / Dtrace
- program observation: `lsof`, `/proc`
- network traffic capture: Wireshark/Tshark, `tcpdump`, `dsniff`
- custom clients: `nc`, Python (Scapy), various MQTT clients

There are other tools that can help with general troubleshooting and/or problem prevention:
- compiler options
- static analyzers (LGTM)
- dynamic analyzers (Valgrind)

## Testing

Basic set of unit tests is located in the `tests` directory. These tests have only very basic
coverage of the **subset** of the specification. These serve basically as a [smoke test](https://en.wikipedia.org/wiki/Smoke_testing_(software)),
meaning that if the program passes these tests, it can be made subject to more thorough testing
and review. Passing these tests does not imply that the assignment is accepted.

## Scaling

### Client buffers

There can be a cap on maximum message size lower than the message length theoretically
supported by the MQTT spec (section 2.2.3 Remaining Length). If a message is received
that is longer, the client should be disconnected.

Using 1 KiB buffer should be sufficient to pass the tests.

### Number of clients

The design of data structures and associated algorithms is not that important.
For example, the latency of message delivery to the clients subscribed to particular
topic is secondary.

That said, the server should **theoretically** support unlimited number of clients.
What this means in practice is that the data structures holding any client related
data should be scalable, e.g. linked list with items added based on requests/clients;
if there is an array used, there needs to be place in the code where it is reallocated
based on the number of needed items. The implementation should be efficient it terms
of memory usage. For instance, the array used for poll(2) (if this is what was used
for implementation) should be completely filled before it is reallocated.

Generally, there is no need to implement e.g. hash tables or multiprocessing/multithreading,
unless you want to. That said, it is better to focus on the correctness of the basic implementation
before making performance optimizations.

