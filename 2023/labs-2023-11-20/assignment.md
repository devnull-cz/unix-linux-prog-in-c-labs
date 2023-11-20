# select

## reader

Finish the _exercise to the reader_ in [`select/select.c`](https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/select.c).

## writer

Q: what happens if non-blocking socket cannot receive any more writes ? (e.g. if the TCP window is full or reduced by the other side).
Try with a sequence of small or singular large buffer.

You can use the example in 
[`select/write-select.c`](https://github.com/devnull-cz/unix-linux-prog-in-c-src/blob/master/select/write-select.c).
as a basis.
