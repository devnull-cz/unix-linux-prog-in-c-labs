# select

## reader

- convert the code to be AF agnostic
- Finish the _exercise to the reader_ in [`select/select.c`](https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/select.c).
- make all the fds non-blocking
- rewrite to `poll()`
- handle the a case of client that disconnected

## writer to full pipe

What happens if using non-blocking fd for writing into pipe that is full ?

## writer to full socket

Q: what happens if non-blocking socket cannot receive any more writes ? (e.g. if the TCP window is full or reduced by the other side).
Try with a sequence of small or singular large buffer.

You can use the example in 
[`select/write-select.c`](https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/write-select.c).
as a basis.
