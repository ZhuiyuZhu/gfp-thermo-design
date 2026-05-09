# DNA反向翻译说明

## 竞赛规则要点

> "本次由大设施统一合成DNA模板（已含启动子、RBS及终止子，且浓度标准化），因此参赛队伍只需提供氨基酸序列，本赛事使用开源DNAChisel算法执行反向翻译"

## 这意味着什么？

1. **你只需提交氨基酸序列**（.csv文件中的Sequence列）
2. **不需要自己设计DNA序列**
3. **不需要考虑密码子优化**（DNAChisel会自动处理）
4. **不需要考虑启动子/RBS/终止子**（大设施已统一添加）

## DNAChisel简介

DNAChisel是一个开源的Python库，用于DNA序列的约束设计和优化：
- **GitHub**: https://github.com/Edinburgh-Genome-Foundry/DnaChisel
- **功能**: 反向翻译、密码子优化、GC含量控制、避免重复序列等

### 反向翻译流程（大设施将执行）

```
氨基酸序列 (你的输入)
    │
    ├─→ [DNAChisel] 反向翻译
    │       ├─→ 选择最优密码子（基于宿主表达系统）
    │       ├─→ 避免稀有密码子
    │       ├─→ 控制GC含量在40-60%
    │       ├─→ 避免内部重复/发夹结构
    │       └─→ 避免限制性酶切位点
    │
    ├─→ [大设施] 添加标准调控元件
    │       ├─→ 启动子 (T7/lac等)
    │       ├─→ RBS (核糖体结合位点)
    │       └─→ 终止子
    │
    └─→ [合成] 标准化浓度DNA模板
            └─→ 用于Cell-Free表达
```

## 你需要关注什么？

### 1. 氨基酸序列的绝对正确性
- 任何氨基酸错误都会直接导致蛋白质功能丧失
- 建议用多种工具交叉验证序列

### 2. 长度控制
- 220-250 aa严格限制
- DNAChisel反向翻译后DNA长度约为 660-750 bp
- 加上启动子/RBS/终止子，总DNA长度约 1000-1200 bp

### 3. 特殊氨基酸考虑
- **Cys (C)**: 若你的序列含Cys，DNAChisel会正常翻译
  - 但注意：无二硫键形成环境（CFPS中氧化还原电位不可控）
  - 建议避免Cys或确保其不参与关键结构
- **Met (M)**: 必须以M开头（起始密码子ATG）
- **Pro (P)**: 在β-turn中常见，Proline的密码子CC_系列

### 4. 如果你想自己验证反向翻译

```python
# 可选：自己用DNAChisel验证
from dnachisel import DnaOptimizationProblem, Location, CodonUsageTable

# 你的氨基酸序列
aa_seq = "MSKGEELFTGVVPILVELDGDVNGHK..."

# 创建反向翻译问题
problem = DnaOptimizationProblem(
    sequence=aa_seq,  # DNAChisel支持直接从AA翻译
    constraints=[
        CodonUsageTable("e_coli", location=Location(0, len(aa_seq)*3)),
    ]
)

# 求解
dna_seq = problem.optimize()
print(f"Optimized DNA: {dna_seq}")
```

**注意**: 这仅用于自我验证，提交时仍只需氨基酸序列。

## 常见误区

| 误区 | 正确理解 |
|------|---------|
| "我需要提交DNA序列" | ❌ 只需氨基酸序列 |
| "我需要做密码子优化" | ❌ DNAChisel自动处理 |
| "我需要考虑启动子强度" | ❌ 大设施统一标准化 |
| "我的序列会被直接合成" | ✅ 是的，但由大设施执行 |
| "我可以提交DNA序列替代AA" | ❌ 必须按格式提交AA序列 |

## 验证清单

- [ ] 氨基酸序列仅含20种标准大写字母
- [ ] 以M开头
- [ ] 长度220-250
- [ ] 无终止密码子符号
- [ ] 序列已在Exclusion_List中检查
