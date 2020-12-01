# Bug Identification

For target4, the pointer `q` is freed twice. To be specific,  the function `tfree(q)` is called twice but `tmalloc` is not called for `q` before the second call of `tfree(q)`. Thus, this is a double free vulnerability, and we can use this bug to overwrite `the saved EIP`.

The key part to use is this code block in `tfree(q)` (note that the variable `p` in the code block is actually `q` since we call `tfree(q)`):
```
if (q != NULL && GET_FREEBIT(q)) /* try to consolidate leftward */
    {
      CLR_FREEBIT(q);
      q->s.r      = p->s.r;
      p->s.r->s.l = q;
      SET_FREEBIT(q);
      p = q;
    }
```
Based on this part, we can set `p`'s (actual `q`'s) right chunk to point to foo's saved EIP (using its left link) and left chunk to point to the start of the buffer (using its right link). By doing so, we can overwrite foo's saved EIP with the start of the buffer. 

The buffer now looks like this:
`[The left link of the left chunk][The right link of the left chunk][(multiple)0x90][shellcode][The left link of the right chunk][The right link of the right chunk][other data]`

Note that between `[the left link of the left chunk]` and the `[(multiple)0x90][shellcode]` part, there is `[the right link of the left chunk]`, which is meaningless and should be skipped so that we can reach `0x90` and finally `shellcode`. To do so, we use `"\xeb\x04"` (jump 4 bytes) to jump over that part.

# Details

1. First, make a buffer with a size of `1024` to run target4, and use gdb to find `the previous p` (`0x8059950`), `the new p` (`0x8059878`), `q` (`0x8059ae8`), and foo's saved EIP (`0xbffffa7c`).

2. The offset between `the previous p` and `the new p` is `0x8059950 - 0x8059878 = d8 = 216`. In addition, after `malloc()`, the next/prev pointers are `8` bytes before the address of the pointers. Thus, the offset between the right chunk and the start of the buffer is `216 - 8 = 208`. 

3. `[The left link of the left chunk]` (4 bytes) should be set as `"\x90\x90\xeb\x04"` (two `0x90` and one `jmp`). Here, jmp (`"\xeb\x04"`, jump 4 bytes) can be used to jump over `[The right link of the left chunk]` to reach `[(multiple)0x90][shellcode]` part.

4. `[The right link of the left chunk]` (4 bytes) should be set as `foo's saved EIP + 1`. This is because, Although `[The right link of the left chunk]` is skipped using jmp `"\xeb\x04"`, but it still needs to be set like this so that the `GET_FREEBIT` function returns true.

5. Finally, `[The left link of the right chunk]` and `[The right link of the right chunk]` are set as `0x8059878` (`the new p`) and foo's saved EIP (`0xbffffa7c`), respectively.