#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
	int nums[5] = {0};
	for (int i = 0; i < 5; i++) {
		nums[i] = 113626820;
	}
	nums[4] += 24;

	char arr[20];

	FILE* fp;
	fp = fopen("exploit.txt", "wb");

	for (int i = 0; i < 5; i++) {
		memcpy(&arr[i], &nums[i], 4);
		fprintf(fp, "%c", arr[i]);
		fprintf(fp, "%c", arr[i+1]);
		fprintf(fp, "%c", arr[i+2]);
		fprintf(fp, "%c", arr[i+3]);

	}

	return 0;
}

