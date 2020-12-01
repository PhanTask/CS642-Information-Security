# Bug Identification

For target1, the `strcpy` function in target1.c doesn't check the argument size. Thus, we can create a buffer with a size larger than `200` to overflow `the saved EIP`. Unlike target0, the buffer size is large enough, and thus shellcode can be put into the buffer so that we are able to get the user shell.

# Details

1. First, make a buffer with a size of `200` to run target1, and use gdb to find the address of the buffer (`0xbffffce0`) and foo's saved EBP (`0xbffffda8`).

2. The buffer we create is a buffer with a size of `209` (200 buf + 4 stp + 4 ret addr + 1 null terminate). The structure of the buffer is `[(multiple)0x90][shellcode][stp][ret addr][null terminate]`. Here, `[stp]` doesn't matter so it is set as all `0x90`; `[ret addr]` is set as the address of the buffer (`0xbffffce0`); `[null terminate]` = `"\x00"`.