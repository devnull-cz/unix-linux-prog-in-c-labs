#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <err.h>

int
main(void)
{
	pid_t pid;

	switch (pid = fork()) {
	case 0:
		execl("/usr/bin/wc", "wc", "/etc/shadow", NULL);
		break;
	case -1:
		err(1, "fork");
	default:
		int status;
		waitpid(pid, &status, 0);
	}
}
