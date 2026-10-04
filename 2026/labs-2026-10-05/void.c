#include <stdio.h>

int
main(void) {
	void *foo = &foo;

	printf("%p\n", foo);
	printf("%p\n", &foo);
}
