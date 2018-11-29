Implement a program that will start listening on a specified TCP port and address.
It will handle one connection at a time. Once current connection is closed,
new one can be accepted.
```
   usage: ./a.out <address> <port> <allowed_address>
```      
Once a connection is accepted, from the specified IP address,
the server will fork+exec a shell and redirect std{in,out,err} to the network connection.
Otherwise, it will behave as a echo server - what is read is written back
until the connection is closed.
   
NOTE: the program has to support both IPv[46]
NOTE: port can be specified as a number or name of service
NOTE: use netcat as a client for testing
NOTE: for testing in non segregated network environment, it is highly advisable to let the
      server listen only on localhost addresses (and change the allowed address accordingly)
 
Variants:
   - allow more simultaneous connections (both echo and shell)
   - the whitelist of IP addresses allowed to spawn a shell will be read from a file
   - the whitelist can consist of IP prefixes

