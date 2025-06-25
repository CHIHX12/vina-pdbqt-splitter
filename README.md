# 🧬 Vina PDBQT Splitter

## 🔬 Description

**Vina PDBQT Splitter** is a high-performance toolkit for post-processing AutoDock Vina docking results. It splits `.pdbqt` output files containing multiple docking poses (`MODEL 1`, `MODEL 2`, ...) into individual `.pdbqt` files per pose, making downstream analysis, rescoring, and visualization more streamlined.

---

## 💡 Use Case

After running AutoDock Vina:

```bash
vina --receptor receptor.pdbqt --ligand ligand.pdbqt --out out1_output.pdbqt
