# GFP Thermostability & Brightness Engineering Pipeline

## 竞赛背景
本仓库为 [合成生物大设施蛋白质设计竞赛] 的参赛代码，目标为设计兼具高荧光亮度与优良热稳定性（72°C）的GFP变体。

## 设计策略
**母序列**: sfGFP (Superfolder GFP, 238 aa)  
**策略**: 基于已知高性能骨架，通过理性设计与计算预测引入热稳定化突变，兼顾Cell-Free表达体系（CFPS）的折叠效率。

### 6条序列设计逻辑

| Seq_ID | 设计策略 | 核心突变 | 风险等级 | 预期表现 |
|--------|---------|---------|---------|---------|
| 1 | **保守基线** | E222Q | 极低 | 亮度≈WT，稳定性略升 |
| 2 | **双热稳定** | E222Q + N149K | 低 | 亮度接近WT，稳定性提升 |
| 3 | **三热稳定** | + Q183R | 中 | 亮度略降，稳定性显著提升 |
| 4 | **极致热稳定** | + M218V | 中-高 | 亮度可能略降，热稳定性最高 |
| 5 | **CFPS表面优化** | E14K+E47K+E173K+E222Q | 中 | 增强无伴侣体系折叠 |
| 6 | **探索型** | loop区+C端工程 | 高 | 高风险高回报 |

### 关键突变文献依据
- **E222Q**: 消除Glu222在碱性条件下的去质子化，增强热稳定性 [Pedelacq et al., 2006]
- **N149K**: 表面盐桥引入，增强β-barrel刚性 [Kiss et al., 2020]
- **Q183R**: 内部氢键网络优化，填充空腔 [Pavel et al., 2018]
- **M218V**: 减少C端柔性，增强尾部稳定性 [Stepanenko et al., 2013]

## 环境配置

### 依赖安装
```bash
# 基础环境
conda create -n gfp_design python=3.9
conda activate gfp_design

# 核心依赖
pip install torch fair-esm pandas numpy biopython

# 结构分析 (可选)
pip install py3Dmol

# MD模拟 (可选，用于预筛选)
conda install -c conda-forge openmm
```

## 使用流程

### Step 1: ESM-2 突变效应扫描
```bash
python scripts/01_esm2_mutation_scan.py --output results/esm2_scores.csv
```
扫描所有可设计位点的单点突变效应，输出伪对数似然分数。

### Step 2: 序列组装与校验
```bash
python scripts/02_sequence_assembler_v2_1.py
```
自动生成6条设计序列，执行格式校验（长度、字符规范、发色团保护、排除列表比对）。

### Step 3: 提交文件生成
运行后自动生成：
- `results/submission_final.csv` — 符合规范的提交文件
- `results/sequences_for_exclusion_check.txt` — 用于排除列表比对的纯序列

## 目录结构
```
.
├── README.md
├── data/
│   └── sfgfp_wt.fasta          # 母序列
├── scripts/
│   ├── 01_esm2_mutation_scan.py    # ESM-2突变打分
│   └── 02_sequence_assembler.py    # 序列组装
├── results/
│   ├── submission_final.csv       # 最终提交文件
│   └── sequences_for_exclusion_check.txt
└── docs/
    └── design_report.pdf         # 设计思路文档 (需自行补充)
```

## 关键设计原则

### 1. 发色团保护 (绝对禁区)
- **Y66, G67**: 发色团核心，不可突变
- **周围8Å环境**: R96, H148, T203, S205, E222, W57 等谨慎处理

### 2. 亮度与热稳定性的平衡
综合得分 = (Finitial/Finitial_WT) × (Ffinal/Finitial)  
数学上等价于 **Ffinal/Finitial_WT**，但受限于 **Finitial ≥ 0.3×Finitial_WT**

因此策略为：
- 保持sfGFP骨架的高折叠效率（亮度底线）
- 在不破坏发色团微环境的前提下引入稳定化突变

### 3. Cell-Free体系适配
- sfGFP本身为"superfolder"，在无伴侣条件下折叠优异
- 避免引入依赖分子伴侣的突变
- 表面电荷优化（Seq-5）可增强CFPS中的溶解度

## 开源声明
本代码基于以下开源工具：
- [ESM-2](https://github.com/facebookresearch/esm) (Meta AI)
- [fair-esm](https://pypi.org/project/fair-esm/)

## 联系方式
Team: YourTeamName
