#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
  long long N = atoll(argv[1]);
  long long sum = 0;
  for (long long i = 0; i < N; i++)
  {
    sum += i;
  }
  printf("Sum: %lld\n",sum);
  return 0;
}
