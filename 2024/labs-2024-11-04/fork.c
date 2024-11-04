#include <unistd.h>

int
main(void)
{
	fork();
	fork();
	fork();

	sleep(42);
}
