import os
import subprocess
from pathlib import Path
from tqdm import tqdm

# === 固定路徑設定 ===
PDB_FOLDER_DOCKING_PATH = './../../cococnut_2025_6_relu_pdbqt_out_8pjk_R_cococunt_L'
OUTPUT_FOLDER = PDB_FOLDER_DOCKING_PATH + '_split1'
RUNNER_PATH = './split_runner'  # 編譯後的 C 程式執行檔

# === 建立輸出資料夾 ===
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === 收集所有 pdbqt 檔案（>100 bytes）===
input_files = [p for p in Path(PDB_FOLDER_DOCKING_PATH).glob("*.pdbqt") if p.stat().st_size > 100]

# === 比對 base name（如 out_XXXX）是否已存在於 output 中 ===
output_basenames = {p.name.split("_")[0] for p in Path(OUTPUT_FOLDER).glob("*.pdbqt")}
to_process = [p for p in input_files if p.stem not in output_basenames]

# === 簡報輸出 ===
print(f"📁 原始 pdbqt 檔案總數：{len(input_files)}")
print(f"✅ 已分割 base name 數量：{len(output_basenames)}")
print(f"🔁 尚需分割檔案數量：{len(to_process)}\n")

# === 執行分割 ===
error_log = []

for pdbqt_path in tqdm(to_process, desc="🔪 C 執行分割中"):
    try:
        result = subprocess.run(
            [RUNNER_PATH, str(pdbqt_path), OUTPUT_FOLDER],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=60
        )
        if result.returncode != 0:
            error_log.append((str(pdbqt_path), result.stderr.decode()))
    except Exception as e:
        error_log.append((str(pdbqt_path), str(e)))

# === 若有錯誤，輸出紀錄 ===
if error_log:
    log_path = os.path.join(OUTPUT_FOLDER, "split_error.log")
    with open(log_path, "w") as f:
        for fname, err in error_log:
            f.write(f"[{fname}]\n{err}\n\n")
    print(f"⚠️ 分割過程有 {len(error_log)} 筆錯誤，詳細請見：{log_path}")
else:
    print("✅ 所有 pdbqt 檔案成功分割完成！")

