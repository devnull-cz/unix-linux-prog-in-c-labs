/*
 * Demonstrate how to use named pipe to avoid busy waiting when lock file
 * already exists.
 *
 * Based on lock-unlock.c.
 *
 * (c) jp@devnull.cz, vlada@kotalovi.cz
 */

#include <stdio.h>
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define	PIPE_PATH	"/tmp/lock_pipe"

int
lock(char *filename)
{
again:
	int pipefd;
	if (open(filename,
	    O_RDONLY | O_TRUNC | O_EXCL | O_CREAT, 0666) != -1) {
		printf("Acquired the lock\n");
		/*
		 * Have to open as read-write. If O_WRONLY was used,
		 * it would wait for the reader to open, blocking itself.
		 */
		if ((pipefd = open(PIPE_PATH, O_RDWR)) == -1)
			err(1, "pipe open write");
		return (pipefd);
	}

	if (errno != EEXIST)
		err(2, "open");

	/* Wait for the unlock. */
	printf("Waiting for unlock\n");
	if ((pipefd = open(PIPE_PATH, O_RDONLY)) == -1)
		err(1, "pipe open read-only");
	char buf[1];
	read(pipefd, buf, sizeof (buf));
	close(pipefd);	// no longer needed
	goto again;

	// Not reached.
	return (-1);
}

int
unlock(char *filename, int pipefd)
{
	printf("Unlocking\n");
	if (unlink(filename) == -1)
		err(2, "unlink");

	if (pipefd != -1)
		close(pipefd);

	return (0);
}

int
main(int argc, char **argv)
{
	if (argc != 2)
		errx(1, "usage: %s <lockfile>", argv[0]);

	// TODO: should check whether this is a pipe
	if (mkfifo(PIPE_PATH, 0666) == -1 && errno != EEXIST)
		err(1, "mkfifo");

	int pipefd = lock(argv[1]);
	printf("Sleeping for a bit\n");
	sleep(10);
	unlock(argv[1], pipefd);
}
