# Bug Identification

For target3, Integer Overflow can be used to overwrite `the saved EIP`. The key part is the code:

```
if (count < MAX_WIDGETS)
    memcpy(buf, in, count * sizeof(struct widget_t));
```

Here the only constriction to the value of `count` is `count < MAX_WIDGETS`, which means we can assign an extremely small negative number to `count` to exceed the range of an integer and create overflow. This overflow can turn the result to be a positive number (can be larger than `MAX_WIDGETS`) so that `memcpy` function can be used to overwrite the saved EIP using a buffer with a size larger than `MAX_WIDGETS`.

# Details

1. First, we need to calculate how large our buffer should be. The struct `widget_t` includes `2` integers and `1` double, so the struct size is `4 + 4 + 8 = 16`, and the buffer size is at least `struct_size * MAX_WIDGETS = 16 * 160 = 2560`. We then make a buffer with a size of `2560` to run target3, and use gdb to find the address of the buffer (`0xbfffea48`) and foo's saved EIP (`0xbffff44c`).

2. Try and find the suitable negative number for `count` so that `count * sizeof(struct widget_t) > 2560` (but not too large). It turned out that `-2147483487` (generates `2572`) meets our needs.

3. The final buffer we create is a buffer with a size of `2581` ( = 2572 + 4 stp + 4 ret addr + 1 null terminate). The structure of the buffer is `[string of count][,][(multiple)0x90][shellcode][stp][ret addr][null terminate]`. Here, `[string of count]` = `"-2147483487"`; `[stp]` doesn't matter in this case and it is set as all `0x90`; `[ret addr]` is set as the address of the buffer (`0xbfffea48`); `[null terminate]` = `"\x00"`.