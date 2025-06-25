import os
import subprocess
from pathlib import Path
from tqdm import tqdm
import argparse

# === CLI 參數 ===
parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', type=str, required=True, help='原始 pdbqt 檔案資料夾')
parser.add_argument('--output_folder', type=str, required=True, help='輸出分割結果的資料夾')
parser.add_argument('--runner_path', type=str, default='./split_runner', help='C 編譯出的 split_runner 執行檔路徑')
args = parser.parse_args()

# === 建立輸出資料夾（如尚未存在） ===
os.makedirs(args.output_folder, exist_ok=True)

# === 收集所有 pdbqt 檔案（大於 100 bytes） ===
input_files = [p for p in Path(args.input_folder).glob("*.pdbqt") if p.stat().st_size > 100]

# === 找出已分割的 base name（例如 out_12345）===
output_basenames = {
    p.name.split("_")[0] for p in Path(args.output_folder).glob("*.pdbqt")
}

# === 篩選尚未處理的 pdbqt 檔案 ===
to_process = [p for p in input_files if p.stem not in output_basenames]

print(f"📁 原始 pdbqt 檔案總數：{len(input_files)}")
print(f"✅ 已分割 base name 數量：{len(output_basenames)}")
print(f"🔁 尚需分割檔案數量：{len(to_process)}\n")

# === 執行 C 程式進行分割 ===
error_log = []

for pdbqt_path in tqdm(to_process, desc="🔪 C 執行分割中"):
    try:
        result = subprocess.run(
            [args.runner_path, str(pdbqt_path), args.output_folder],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=60
        )
        if result.returncode != 0:
            error_log.append((str(pdbqt_path), result.stderr.decode()))
    except Exception as e:
        error_log.append((str(pdbqt_path), str(e)))

# === 錯誤輸出（如有） ===
if error_log:
    log_path = os.path.join(args.output_folder, "split_error.log")
    with open(log_path, "w") as f:
        for fname, err in error_log:
            f.write(f"[{fname}]\n{err}\n\n")
    print(f"⚠️ 分割過程有 {len(error_log)} 筆錯誤，詳細請見：{log_path}")
else:
    print("✅ 所有 pdbqt 檔案成功分割！")

