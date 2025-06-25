#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_LEN 2048

void split_pdbqt(const char* input_file, const char* output_dir) {
    FILE *in_fp = fopen(input_file, "r");
    if (!in_fp) {
        fprintf(stderr, "Failed to open input file: %s\n", input_file);
        return;
    }

    char line[LINE_LEN];
    char base_name[256];
    int model_id = 0;
    FILE *out_fp = NULL;

    // 取檔案名稱（去除路徑與副檔名）
    const char *slash = strrchr(input_file, '/');
    if (slash) {
        strncpy(base_name, slash + 1, sizeof(base_name) - 1);
    } else {
        strncpy(base_name, input_file, sizeof(base_name) - 1);
    }
    base_name[strcspn(base_name, ".")] = '\0'; // 去除 .pdbqt

    // 開始分割
    while (fgets(line, LINE_LEN, in_fp)) {
        if (strncmp(line, "MODEL", 5) == 0) {
            model_id++;
            char out_path[512];
            snprintf(out_path, sizeof(out_path), "%s/%s_%d.pdbqt", output_dir, base_name, model_id);
            out_fp = fopen(out_path, "w");
            if (!out_fp) {
                fprintf(stderr, "Failed to open output file: %s\n", out_path);
                continue;
            }
        }

        if (out_fp) fputs(line, out_fp);

        if (strncmp(line, "ENDMDL", 6) == 0 && out_fp) {
            fclose(out_fp);
            out_fp = NULL;
        }
    }

    if (out_fp) fclose(out_fp);
    fclose(in_fp);
}

