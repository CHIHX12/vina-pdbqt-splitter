# 🧬 PDBQT Splitter — Multi-Model `.pdbqt` 分割工具

## 🔬 工具簡介

本工具可將 `.pdbqt` 結果檔中包含的多個 `MODEL` 自動分割為獨立檔案。該格式通常來自分子對接流程，包含多個預測構象（例如 `MODEL 1` 至 `MODEL 9`）。本工具支援單一檔案處理、批次處理與多核心平行處理，可應用於大規模虛擬篩選後的後處理流程。

---

## 🎯 功能特色

- ✅ 自動解析 `.pdbqt` 中的 `MODEL` 區段並分割
- ✅ 支援單一檔案或資料夾整批處理
- ✅ 已處理檔案自動跳過，避免重複執行
- ✅ 多核心加速（multiprocessing）
- ✅ 分割失敗會自動產生錯誤日誌

---

## 📦 檔案組成

```text
split_main.c                 # 分割主邏輯 (C)
split_pdbqt.c                # 解析 .pdbqt 檔案內容
split_runner                 # 編譯後執行檔 (C → binary)
split_all.py                # 固定路徑單核版本
split_all_not_path.py       # CLI 參數版本（可自訂路徑）
split_all_multiproc.py      # 固定路徑多核心版本
```

---

## ⚙️ 安裝與編譯

請使用以下指令編譯分割程式：

```bash
gcc -O3 -o split_runner split_pdbqt.c split_main.c
```

成功後會產生 `split_runner` 可執行檔。

---

## 🚀 使用教學

### 🧪 單一 `.pdbqt` 分割

```bash
./split_runner input.pdbqt ./output_folder/
```

---

### 📁 批次處理方式

| 腳本名稱                  | 功能說明                            | 可自訂路徑 | 支援多核心 |
|---------------------------|-------------------------------------|------------|------------|
| `split_all_not_path.py`   | 指定輸入與輸出資料夾               | ✅ 是      | ❌ 否       |
| `split_all.py`            | 固定路徑處理（直接執行）           | ❌ 否      | ❌ 否       |
| `split_all_multiproc.py`  | 固定路徑 + 多核心加速               | ❌ 否      | ✅ 是       |

---

### 🧩 自訂路徑範例（推薦）

```bash
python3 split_all_not_path.py \
  --input_folder ./vina_outputs \
  --output_folder ./vina_outputs_split \
  --runner_path ./split_runner
```

---

### ⚡ 固定路徑多核心處理（可在腳本內改輸入路徑）

```bash
python3 split_all_multiproc.py
```

---

## 📂 輸出結果說明

每個多構象 `.pdbqt` 檔案（如 `lig1_out.pdbqt`）將會被分割為：

```
lig1_out_1.pdbqt
lig1_out_2.pdbqt
...
lig1_out_N.pdbqt
```

失敗檔案將記錄於：

```
split_outputs/split_error.log
```

---

## 🧼 `.gitignore` 建議

```gitignore
split_runner
__pycache__/
*.log
```

---

## 📜 授權 License

本專案使用 MIT License，詳見 [LICENSE](./LICENSE)。

---

## 👨‍💻 作者說明

本工具由研究者開發，專為大規模分子對接後處理流程設計，支援高效且穩定的 `.pdbqt` 多構象檔分割。歡迎提出建議與貢獻改進。
