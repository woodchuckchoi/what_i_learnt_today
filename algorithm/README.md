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

# External Merge Sort

For sorting 900 megabytes of data using only 100 megabytes of RAM:

1. Read 100 MB of the data in main memory and sort by some conventional method, like quicksort.
2. Write the sorted data to disk.
3. Repeat steps 1 and 2 until all of the data is in sorted 100 MB chunks (there are 900MB / 100MB = 9 chunks), which now need to be merged into one single output file.
4. Read the first 10 MB (= 100MB / (9 chunks + 1)) of each sorted chunk into input buffers in main memory and allocate the remaining 10 MB for an output buffer. (In practice, it might provide better performance to make the output buffer larger and the input buffers slightly smaller.)
5. Perform a 9-way merge and store the result in the output buffer. Whenever the output buffer fills, write it to the final sorted file and empty it. Whenever any of the 9 input buffers empties, fill it with the next 10 MB of its associated 100 MB sorted chunk until no more data from the chunk is available. This is the key step that makes external merge sort work externally -- because the merge algorithm only makes one pass sequentially through each of the chunks, each chunk does not have to be loaded completely; rather, sequential parts of the chunk can be loaded as needed.

---

# Sort Analysis
Quick Sort와 Merge Sort는 n log의 시간복잡도를 갖는다. 그런데 왜 Quick Sort implementation을 더 많이 사용할까?\
심지어 Quick Sort에서 최악의 케이스는 시간복잡도가 n^2인데도. (배열이 이미 정렬되어 있거나, 모두 같은 값일 경우)
0. Merge Sort는 왼쪽과 오른쪽을 분리(메모리에 적재)해서 사용하므로 메모리를 더 많이 사용하게 된다. 반면 Quick Sort는 In-place로 작동한다.
1. Quick Sort는 pivot과 포인터를 사용하므로 같은 메모리에 위치한 값에 접근하는 경우가 더 잦다. 따라서 Cache에 저장된 값을 재사용해서 효율을 높일 수 있다.(지역성)
2. Merge Sort에서 일반적으로 더 많은 Swap이 이루어진다.
3. (내 생각) Merge Sort에서 변수를 생성하고 관리하는데서 GC overhead가 발생한다. 또한 Quick Sort는 큰 집단에서 작은 집단으로, Merge Sort는 작은 집단에서 큰 집단으로 재귀하므로 Quick Sort에서는 Tail Call Recursion 최적화가 이루어질 수 있다.

---
