/*
 * There was a change in GCC-9
 * The compound literal is considered an anonymous variable in the current scope.
 * 'j' takes the address of it and then the scope ends 'j' access it afterwards.
 *
 * In previous versions of GCC, the compound literal was put in the function level
 * scope rather than in the current scope. Which is why it worked previously.
 * But the code was undefined. This was added to the GCC-9 changes page.
 * 
 * Bugs to reference
 * https://gcc.gnu.org/bugzilla/show_bug.cgi?id=91031
 * https://gcc.gnu.org/bugzilla/show_bug.cgi?id=94979
 * 
 * Reproducible in gcc-9.3.1
 * It segfaults systemd-239.
 * 
 * Hope it will be fixes (reverted back) in newer version.
 */
#include <string.h>

int chararray(char **j) {
        if (!j) {
                j = (char *[]){"a", "test"};
	}

        return (strlen(j[0]) == 1) & (strlen(j[1]) == 4);
}

int main(void) {
	return chararray(0) == 0;
}
