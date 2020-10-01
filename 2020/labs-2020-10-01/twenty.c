/*
 * The program is supposed to print twenty '-' characters.
 * It fails to do that.
 *
 * Change one character to fix it.
 */

#include <stdio.h>

int
main(void)
{
	int i, n = 20;

	for (i = 0; i < n; i--) {
		printf("-");
		putchar('\n');
	}
}
