Here’s a simple implementation in C:

```c
#include <stdio.h>

int count_between(const char *a, const char *b) {
    // Remove leading/trailing whitespace from both strings
    size_t len_a = strlen(a);
    size_t len_b = strlen(b);
    if (len_a == 0 || len_b == 0) return 1;

    size_t start = a[0];
    while (start < len_a && a[start] != ' ') start++;

    size_t end = b[0];
    while (end < len_b && b[end] != ' ') end++;

    if (start >= end) return 0; // outside range

    int count = end - start;
    return count + 1; // inclusive of both ends
}

int main() {
    printf("Between %s and %s: ", "192.168.1.1", "192.168.1.5");
    printf("%d\n", count_between("192.168.1.1", "192.168.1.5"));

    return 0;
}
```

If you prefer a pure C (no `#include <string.h>`), the logic remains similar using string manipulation:

```c
#include <stdio.h>

int count_between(const char *a, const char *b) {
    size_t len_a = strlen(a);
    size_t len_b = strlen(b);
    if (len_a == 0 || len_b == 0) return 1;

    size_t start = a[0];
    while (start < len_a && a[start] != ' ') start++;

    size_t end = b[0];
    while (end < len_b && b[end] != ' ') end++;

    if (start >= end) return 0;

    int count = end - start;
    return count + 1;
}
```