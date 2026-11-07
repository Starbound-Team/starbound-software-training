#include <stdio.h>

int main(void) {
    // Python: a = [1, 2, 3, 4]
    int a[] = {1, 2, 3, 4};

    // Python: b = a
    int *b = a;   // b points at the same memory, nothing is copied

    // Python: b[0] = 99
    b[0] = 99;

    // Python: print(a)  ->  [99, 2, 3, 4]
    printf("a = [%d, %d, %d, %d]\n", a[0], a[1], a[2], a[3]);

    // Python: a is b  ->  True
    printf("a is at %p\n", (void *)a);
    printf("b is at %p\n", (void *)b);

    return 0;
}
