#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

static void
print_args(int argc, char *argv[])
{
	for (int i = 0; i < argc; argv++, i++)
		printf("%d:%s\n", i, *argv);
}

static int
getopt_invalid_arg(void)
{
	// TODO: move argv construction to a function (using elipsis)
	int argc = 2;
	char **argv = calloc(3, sizeof (char *));
	assert(argv);
	argv[0] = strdup("prog");
	assert(argv[0]);
	argv[1] = strdup("-x");
	argv[2] = NULL;
	assert(argv[1]);

	char opt;
	print_args(argc, argv);
	opterr = 0; // suppress error prints from getopt()
	while ((opt = getopt(argc, argv, "c")) != -1) {
		switch (opt) {
		case 'c':
			break;
		case '?':
			fprintf(stderr, "unknown option: %c\n", optopt);
			return (0);
		default:
			fprintf(stderr, "got %c\n", opt);
			break;
		}
	}

	return (-1);
}

int
main(void)
{
	assert(getopt_invalid_arg() != -1);

	// TODO: add more tests here
}
