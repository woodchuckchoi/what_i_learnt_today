# Insertion Sort
	#include <stdio.h>
	
	void insertion_sort(int *arr, int size) {
		for (int i = 0; i < size - 1; i++) {
			for (int j = i + 1; j < size; j++) {
				if (*(arr+i) > *(arr+j)) {
					int tmp = *(arr+i);
					*(arr+i) = *(arr+j);
					*(arr+j) = tmp;
				}
			}
		}
	}
	
	int main() {
		int arr[] = {5,2,7,4,45,7,3,5,8,5,3,8,9,4,10};
		insertion_sort(arr, sizeof(arr)/sizeof(arr[0]));
		
		for (int i = 0; i < sizeof(arr)/sizeof(arr[0]); i++) {
			printf("%d ", arr[i]);
		}
		printf("\n");
		return 0;
	}

---

# Bubble Sort
	#include <stdio.h>
	
	void swap(int *arr, int i, int j) {
		int tmp = *(arr+i);
		*(arr+i) = *(arr+j);
		*(arr+j) = tmp;
	}
	
	void bubble(int *arr, int size) {
		for (int i = 1; i < size; i++) {
			int cur = i;
			while (cur > 0) {
				if (*(arr+cur-1) > *(arr+cur)) {
					swap(arr, cur, cur-1);
				}
				--cur;
			}
		}
	}
	
	int main() {
		int arr[] = {34,46,2,45,754,23,45,42,3,64,24,7,75,53};
		
		int size = sizeof(arr)/sizeof(arr[0]);
		bubble(arr, size);
		for (int i = 0; i < size; i++) {
			printf("%d ", arr[i]);
		}
		printf("\n");
		return 0;
	}

---

# Merge Sort
	#include <stdio.h>
	#include <stdlib.h>
	
	void merge(int arr[], int l, int m, int h) {
		int i, j, k;
		int n1 = m - l + 1;
		int n2 = h - m;
	
		int *left = (int *)malloc(sizeof(int)*n1);
		int *right = (int *)malloc(sizeof(int)*n2);
	
		for (i = 0; i < n1; i++)
			*(left+i) = arr[l+i];
		for (j = 0; j < n2; j++)
			*(right+j) = arr[m+1+j];
	
		i = 0;
		j = 0;
		k = l;
	
		while (i < n1 && j < n2) {
			if (*(left + i) < *(right + j)) {
				*(arr+k) = *(left + i);
				++i;
			} else {
				*(arr+k) = *(right + j);
				++j;
			}
			++k;
		}
	
		while (i < n1) {
			*(arr+k) = *(left+i);
			++i;
			++k;
		}
		while (j < n2) {
			*(arr+k) = *(right+j);
			++j;
			++k;
		}
	}
	
	void merge_sort(int arr[], int l, int h) {
		if (l < h) {
			int mid = (l + h)/2;
			merge_sort(arr, l, mid); // including the right boundary
			merge_sort(arr, mid+1, h);
			merge(arr, l, mid, h);
		}
	}
	
	int main() {
		int arr[] = {1,5,653,23,645,5243,4,65,532,14,346,475,532,8,364,865,5,856,43,524,635};
		int size = sizeof(arr)/sizeof(arr[0]);
	
		merge_sort(arr, 0, size-1);
		for (int i = 0; i < size; i++) {
			printf("%d ", arr[i]);
		}
		printf("\n");
		return 0;
	}

---

# Quick Sort
	#include <stdio.h>
	#include "swap.h"
	
	int partition(int arr[], int l, int h) {
		int pivot = arr[h];
		int cursor = l;
		for (int i = l; i <= h - 1; i++) {
			if (arr[i] < pivot) {
				swap(arr, i, cursor);
				++cursor;
			}
		}
		swap(arr, cursor, h);
		return cursor;
	}
	
	void quick_sort(int arr[], int l, int h) {
		if (l < h) {
		int pivot = partition(arr, l, h);
		
		quick_sort(arr, l, pivot-1);
		quick_sort(arr, pivot+1, h);
		}
	}
	
	int main() {
		int arr[] = {312,634,433,3465,765,253,7,534,645,756,532,856,523,68,623};
		int size = sizeof(arr)/sizeof(arr[0]);
		quick_sort(arr, 0, size-1);
		for (int i = 0; i < size; i++) {
			printf("%d ", arr[i]);
		}
		printf("\n");
		return 0;
	}

---

# Heap Sort

	#include <stdio.h>
	#include <stdlib.h>
	#include "swap.h"
	
	typedef struct Heap {
		int *data;
		int size;
	} Heap;
	
	void heapify(Heap *heap, int i) {
		int left = 2*i+1;
		int right = 2*i+2;
		int smallest = i;
	
		if (left < heap->size && *((heap->data)+left) < *((heap->data)+smallest)) {
			smallest = left;
		}
		if (right < heap->size && *((heap->data)+right) < *((heap->data)+smallest)) {
			smallest = right;
		}
	
		if (smallest != i) {
			swap(heap->data, smallest, i);
			heapify(heap, smallest);
		}
	}
	
	void heap_sort(Heap *heap) {
		for (int i = heap->size/2; i > -1; i--) {
			heapify(heap, i);
		}
	
		for (int i = heap->size-1; i > -1; i--) {
			swap(heap->data, 0, i);
			printf("%d ", *((heap->data)+i));
			heap->size--;
			heapify(heap, 0);
		}
		printf("\n");
	}
	
	int main() {
		Heap h;
		int data[] = {432,5343,634,7,34,756,4,74,534,687,53,68,354,59,523,7};
		h.data = data;
		h.size = sizeof(data)/sizeof(data[0]);
		heap_sort(&h);
		return 0;
	}

---

# Longest Common Subsequence

	//Go
	const (
		LEN_A int = N+1,
		LEN_B int = M+1
	)
	
	var common int[LEN_A][LEN_B]
	
	for int i = 0; i < LEN_A; i++ {
		for int j = 0; j < LEN_B; j++ {
			if i == 0 || j == 0 {
				common[i][j] = 0
			}
			
			if A[i-1] != B[j-1] {
				common[i][j] = Max(common[i-1][j], common[i][j-1])
			} else {
				common[i][j] = common[i-1][j-1] + 1
			}
	
	return common[N][M]

---


