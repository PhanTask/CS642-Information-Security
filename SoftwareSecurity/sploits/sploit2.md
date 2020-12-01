# Bug Identification

For target2, there is a Frame Pointer Overwrite bug. The last bit of buffer can be used to overwrite the last byte of `the saved ESP`. The key part is the code:

```
for (i = 0; i <= len; i++)
    out[i] = in[i];
```
Unlike target1, target2.c checks the argument size. But the bug is `i <= len` (should be `i < len`). This gives us a chance to have one more byte (i.e., altering byte) in the buffer while not violating the length check.

# Details

1. First, make a buffer with a size of `162` to run target2, and use gdb to find the address of the buffer (`0xbffffd28`) and bar's saved EBP (`0xbffffdc8`). With 1 altering byte, we can overwrite the last byte of bar's saved EBP, which is `c8`. We modify it to `c0` using altering byte so that it looks like a foo's frame and points to somewhere in the buffer.

2. The buffer we create is a buffer with a size of `162` (156 buf + 4 ret addr + 1 altering byte + 1 null terminate). The structure of the buffer is `[(multiple)0x90][shellcode][ret addr][altering byte][null terminate]`. Here, `[ret addr]` is set as the address of the buffer (`0xbffffd28`); `[altering byte]` = `"\xc0"`; `[null terminate]` = `"\x00"`.