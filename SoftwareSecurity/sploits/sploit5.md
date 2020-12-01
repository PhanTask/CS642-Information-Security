# Bug Identification

For target5, string format vulnerability can be used to "attack" the `snprintf` function to overwrite the contents (e.g., `EIP`) in the buffer.

# Details

1. First, make a buffer with a size of `480` to run target5, and use gdb to find the address of the buffer (`0xbffffab8`) and foo's saved EIP (`0xbffffc9c`).

2. In this case, the string format template to be used is something like `[address][any byte][shellcode][(multiple)%u][%n]`. Here `[address]` is currently set to be foo's saved EIP on the stack and has 4 bytes; `[any byte]` can all be `0x90` with arbitrary size (depend on buffer size, shellcode size, and the length of `[(multiple)%u][%n]`); `[shellcode]` is the shellcode; `[(multiple)%u]` means multiple `%u` connected together. The number of `%u` is based on how many `%u` we need to make the stack pointer point to the address of the buffer. It turned out three `%u` are enough after trying it in gdb mode. Thus, `[(multiple)%u][%n] = %u%u%u%n`; `[%n]` causes a certain number of bytes to be written to the address.

3. To control the number of bytes written by `%n` in order to reach the address of the buffer, zeros can be padded before reaching `%n`. Thus, `%u%u%u%n` is modified as `%u%u%0ku%n`, where `k` controls the number of zeros to be padded. `k` can be determined by the first three bytes of the `EIP` address (which is `bffffc = 12582908`). Considering the buffer size, address size, `%u%u%0ku%n` length, etc., `k` is finally set as `12582442` (`%u%u%0ku%n = %u%u%12582442u%n`).

4. Since only the first three bytes of the `EIP` address is overwritten, the address should be pointed to `1` byte after the `EIP` address. Thus `the address = 0xbffffc9c + 1 = 0xbffffc9d`.