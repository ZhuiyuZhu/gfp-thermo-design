# GFP竞赛快速参考卡 (Quick Reference Card)

## 📊 核心公式
```
综合得分 = (Finitial / Finitial_WT) × (Ffinal / Finitial)
        = Ffinal / Finitial_WT

淘汰线: Finitial < 0.3 × Finitial_WT → 该序列0分
```

## 🧬 母序列
**sfGFP** (238 aa, PDB: 2B3P)
```
MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK
```

## 🎯 6条序列速查

| ID | 突变 | 风险 | 亮度预估 | 稳定预估 | 策略 |
|----|------|------|---------|---------|------|
| 1 | E222Q | ⭐ | 95% | 115% | 保守保底 |
| 2 | E222Q+N149K | ⭐⭐ | 92% | 125% | 双热稳定 |
| 3 | +Q183R | ⭐⭐⭐ | 88% | 135% | 三热稳定 |
| 4 | +M218V | ⭐⭐⭐⭐ | 82% | 145% | 极致热稳定 |
| 5 | E14K+E47K+E173K+E222Q | ⭐⭐⭐ | 93% | 118% | CFPS优化 |
| 6 | +L195A+S231V | ⭐⭐⭐⭐⭐ | 78% | 155% | 探索型 |

## 🚫 绝对禁区
- **Y66** (pos 65, 0-indexed): 发色团酚羟基
- **G67** (pos 66, 0-indexed): 发色团酰胺
- **周围8Å**: R96, H148, T203, S205, E222环境, W57

## 🔬 关键突变文献依据

| 突变 | 文献 | 机制 | 置信度 |
|------|------|------|--------|
| E222Q | Pedelacq 2006 | 消除去质子化 | ★★★★★ |
| N149K | Kiss 2020 | 表面盐桥 | ★★★★☆ |
| Q183R | Pavel 2018 | 内部空腔填充 | ★★★★☆ |
| M218V | Stepanenko 2013 | C端锚定 | ★★★☆☆ |

## 🛠️ 常用命令

```bash
# 一键生成全部材料
python scripts/00_master_controller.py --team YourTeamName --package

# 单独步骤
python scripts/01_esm2_mutation_scan_demo.py    # ESM-2扫描
python scripts/02_sequence_assembler_v2_1.py     # 序列组装
python scripts/04_exclusion_checker.py           # 排除检查
python scripts/06_final_submission_check.py      # 最终校验

# 提交前检查清单
cat SUBMISSION_CHECKLIST.md
```

## 📁 关键文件位置

```
results/submission_final.csv          ← 提交文件
results/figures/fig3_risk_benefit_matrix.png  ← 文档用图
docs/design_report_template.md        ← 文档模板
SUBMISSION_CHECKLIST.md               ← 提交前检查
```

## ⚡ 紧急备案（时间不足时）

1. 直接用 `results/submission_final.csv` 中的6条序列
2. 将 `docs/design_report_template.md` 转为PDF
3. 创建GitHub仓库，上传本代码
4. 提交

**最低限度**: 正确格式的CSV + 简版PDF + GitHub链接

## 📞 关键参数速查

| 参数 | 值 |
|------|-----|
| ESM-2模型 | esm2_t33_650M_UR50D |
| Rosetta力场 | ref2015 |
| MD力场 | Amber14SB + OPC |
| 升温温度 | 350K (≈77°C) |
| 发色团距离阈值 | 8Å |
| 亮度安全垫 | >70% WT |
| 序列长度 | 220-250 aa |

## 🎓 竞赛策略口诀

> **"保守保底两条，中风险冲奖两条，高风险搏命两条"**
> 
> **"亮度是底线，热稳是上限，综合看乘积"**
>
> **"发色团不动，表面可折腾，内部需谨慎"**
