#include <unistd.h>
#include <stdlib.h>
#include <err.h>

extern char **environ;

int
main(void)
{
	setenv("EDITOR", "nano", 1);
#ifdef SUDO
	char *args[] = {"sudo", "-E", "vipw", NULL};
	int r = execve("/usr/bin/sudo", args, environ);
#else
	char *args[] = {NULL};
	int r = execve("/usr/bin/env", args, environ);
#endif

	if (r == -1)
		err(1, "exec");
}
