#include <stdlib.h>

void* foo() {
	return malloc(1);
}

int main(void) {
	void *ptra = foo();
}
