

#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <time.h>


#define MAX_NUM_ELEMENTS 50

int main() {
  int count;
  int arr1[MAX_NUM_ELEMENTS];
  int arr2[MAX_NUM_ELEMENTS];
  int arr_result[MAX_NUM_ELEMENTS];
  
  clock_t start, end;
  double cpu_time_used;
  start = clock();
	
  memset(arr1, 10, MAX_NUM_ELEMENTS * sizeof(int));
  memset(arr2, 10, MAX_NUM_ELEMENTS * sizeof(int));
  
  for (int row_1 = 0; row_1 < MAX_NUM_ELEMENTS; row_1++) {
  	for (int row_2 = 0; row_2 < MAX_NUM_ELEMENTS; row_2++){
  		  	arr_result[count] = arr1[row_1] * arr2[row_2];
  	}
  }

  end = clock();
  cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
  printf("CPU computation time was: %f\n", cpu_time_used);
  return 0;
}