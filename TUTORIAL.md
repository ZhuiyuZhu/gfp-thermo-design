# GFP设计项目使用教程

## 快速开始（5分钟）

### 步骤1: 下载项目
```bash
git clone https://github.com/YourTeamName/gfp-thermo-design.git
cd gfp-thermo-design
```

### 步骤2: 安装依赖
```bash
pip install -r requirements.txt
```

### 步骤3: 生成序列
```bash
python scripts/02_sequence_assembler_v2_1.py
```

输出：`results/submission_final.csv`

### 步骤4: 检查
```bash
python scripts/06_final_submission_check.py
```

## 完整流程（1小时）

### 阶段1: ESM-2扫描
```bash
# 快速演示（无需GPU）
python scripts/01_esm2_mutation_scan_demo.py

# 真实扫描（需要GPU + fair-esm）
python scripts/01_esm2_mutation_scan.py --output results/esm2_real_scores.csv
```

### 阶段2: 结构分析
```bash
# 下载sfGFP结构
# 手动从PDB下载2B3P，或使用PyMOL: fetch 2B3P

# 运行PyMOL分析脚本
pymol scripts/pymol_gfp_analysis.pml
```

### 阶段3: 序列优化
```bash
# 基于ESM-2结果调整突变组合
# 编辑 scripts/02_sequence_assembler_v2_1.py 中的 mutations 字典

# 重新生成
python scripts/02_sequence_assembler_v2_1.py
```

### 阶段4: 排除检查
```bash
# 将官方Exclusion_List.csv放入data/目录
python scripts/04_exclusion_checker.py --input results/submission_final.csv
```

### 阶段5: 最终校验
```bash
python scripts/06_final_submission_check.py --input results/submission_final.csv
```

### 阶段6: 生成文档
```bash
# 生成PDF（需要pandoc + xelatex）
python scripts/09_generate_pdf.py --team YourTeamName

# 或手动转换
pandoc docs/design_report_template.md -o docs/design_report.pdf
```

## 高级用法

### 自定义突变组合
编辑 `scripts/02_sequence_assembler_v2_1.py`:

```python
def design_seq1_conservative(self):
    muts = {
        221: 'Q',   # 修改这里
        # 添加新突变
        100: 'A',   # 示例
    }
    return apply_mutations(self.wt, muts), muts, "Custom"
```

### 运行Rosetta计算
```bash
# 需要学术许可的Rosetta安装
python scripts/08_rosetta_ddg.py --pdb data/2b3p.pdb
```

### 运行MD模拟
```bash
# 需要OpenMM
# 参考 scripts/md_simulation_params.ini 配置参数
```

### 使用ProteinMPNN
```bash
# 克隆ProteinMPNN仓库
git clone https://github.com/dauparas/ProteinMPNN.git

# 运行设计
python scripts/05_proteinmpnn_design.py
# 复制输出的命令并执行
```

## 常见问题

### Q: ESM-2扫描太慢怎么办？
**A**: 使用演示版 `01_esm2_mutation_scan_demo.py`，基于启发式模拟，秒级完成。

### Q: 序列在排除列表中怎么办？
**A**: 微调突变位点，如 E222Q → E222G，或 N149K → N149R。

### Q: 如何验证结构合理性？
**A**: 使用PyMOL运行 `pymol_gfp_analysis.pml`，检查突变位点与发色团距离。

### Q: 可以修改母序列吗？
**A**: 可以，但需确保新母序列长度在220-250 aa，且以M开头。

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| ImportError: No module named 'esm' | ESM-2未安装 | `pip install fair-esm` |
| FileNotFoundError: Exclusion_List.csv | 未下载排除列表 | 从报名系统下载 |
| Validation failed: Length | 序列长度错误 | 检查母序列长度 |
| Pandoc not found | 未安装pandoc | `sudo apt-get install pandoc` |

## 获取帮助

- 查看 [FAQ.md](FAQ.md)
- 查看 [INDEX.md](INDEX.md) 导航
- 提交GitHub Issue
- 联系组委会
