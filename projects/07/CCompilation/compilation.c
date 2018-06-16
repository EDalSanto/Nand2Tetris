/*
 * "Hello, World!": A classic.
 */

// preprocessor inlines code from this header file
// preprocessor output -> cc -E compilation.c
#include <stdio.h>

// compilation output -> cc -S compilation.c
// assembler output -> cc -c compilation.c
// linker output -> cc -o compilation.c
int
main(void)
{
	puts("Hello, World!");
	return 0;
}
