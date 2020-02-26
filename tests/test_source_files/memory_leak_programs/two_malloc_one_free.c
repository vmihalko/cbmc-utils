#include <stdlib.h>

int main () {
   char *a = (char *) malloc(1);
   char *b = (char *) malloc(1);
   free(b);
}
