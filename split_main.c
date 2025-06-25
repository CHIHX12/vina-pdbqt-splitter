#include <stdio.h>

// split_pdbqt 原型宣告（定義於 split_pdbqt.c）
void split_pdbqt(const char* input_file, const char* output_dir);

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("Usage: %s input.pdbqt output_folder/\n", argv[0]);
        return 1;
    }

    split_pdbqt(argv[1], argv[2]);
    return 0;
}

