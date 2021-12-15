#ifndef MY_UTIL
#define MY_UTIL

/* Functions */

int binarySearchAsc(double *arr, unsigned int lo, unsigned int up, double value);
int binarySearchDesc(double *arr, unsigned int lo, unsigned int up, double value);
char interpolateFromTable(double *arrX, double *arrY, unsigned int arrSize, double* result, double value);

#endif
