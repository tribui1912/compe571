#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
  if (argc != 2)
  {
    fprintf(stderr, "Usage %s <N>\n", argv[0]);
    return 1;
  }
  int N = atoi(argv[1]);
  long long sum = 0;
  for (int i = 0; i < N; i++)
  {
    sum += i;
  }
  printf("Sum: %lld\n",sum);
  return 0;
}

