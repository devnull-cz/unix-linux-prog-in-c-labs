#include <stdio.h>

int
main(int argc, char *argv[]) {
	return putchar(*(*(argv + 2) + 1));
}
