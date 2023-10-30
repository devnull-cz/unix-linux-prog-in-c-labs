#include <sys/types.h>
#include <unistd.h>

int
main(void)
{
	fork();
	fork();
	fork();

	sleep(42);
}
