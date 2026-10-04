#include <stdio.h>

int
main(int n, char **a) {
	return putchar(*(*(a + 2) + 1) - 32);
}
