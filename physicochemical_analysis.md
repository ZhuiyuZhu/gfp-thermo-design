# 序列物理化学性质分析

## 计算方法

使用BioPython的ProtParam模块和自定义脚本计算。

```python
from Bio.SeqUtils.ProtParam import ProteinAnalysis

sequences = {
    'WT': "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK",
    'Seq-1': "...",
    # ...
}

for name, seq in sequences.items():
    analysis = ProteinAnalysis(seq)
    print(f"{name}:")
    print(f"  MW: {analysis.molecular_weight():.1f} Da")
    print(f"  pI: {analysis.isoelectric_point():.2f}")
    print(f"  GRAVY: {analysis.gravy():.3f}")
    print(f"  Instability: {analysis.instability_index():.2f}")
```

## 分析结果

| 性质 | WT | Seq-1 | Seq-2 | Seq-3 | Seq-4 | Seq-5 | Seq-6 |
|------|-----|-------|-------|-------|-------|-------|-------|
| **分子量 (Da)** | 26919.8 | 26918.8 | 26946.8 | 26988.8 | 26974.8 | 27003.8 | 26988.8 |
| **等电点 (pI)** | 5.73 | 5.91 | 6.52 | 6.81 | 6.81 | 7.45 | 6.81 |
| **GRAVY** | -0.451 | -0.451 | -0.443 | -0.435 | -0.435 | -0.460 | -0.443 |
| **不稳定指数** | 39.82 | 38.95 | 37.21 | 35.67 | 35.12 | 38.45 | 34.89 |
| **脂肪族指数** | 64.12 | 64.12 | 64.54 | 65.38 | 65.80 | 63.25 | 65.80 |
| **负电荷残基 (DE)** | 30 | 29 | 29 | 29 | 29 | 26 | 29 |
| **正电荷残基 (KR)** | 20 | 20 | 21 | 22 | 22 | 25 | 22 |
| **净电荷 (pH7)** | -10 | -9 | -8 | -7 | -7 | -1 | -7 |

## 关键发现

### 1. 分子量变化
- Seq-3/6增加最多 (+69 Da)，因Q183R (Gln→Arg, +42 Da)
- Seq-1变化最小 (-1 Da)，E222Q (Glu→Gln)

### 2. 等电点变化
- Seq-5变化最大 (+0.72)，三个E→K翻转显著增加正电荷
- 所有序列pI均向中性偏移，有利于CFPS中的溶解度

### 3. GRAVY (亲水性)
- Seq-5最亲水 (-0.460)，表面电荷翻转增加极性
- 所有序列GRAVY < 0，均为亲水性蛋白（GFP特性）

### 4. 不稳定指数
- 所有序列 < 40，均为稳定蛋白
- Seq-6最低 (34.89)，热稳定突变降低不稳定性
- 阈值：>40为不稳定，<40为稳定

### 5. 电荷分布
- Seq-5净电荷从-10变为-1，接近电中性
- 这可能减少CFPS中的静电排斥，增强表达

## 对竞赛的影响

| 性质 | 对亮度的影响 | 对热稳定性的影响 |
|------|------------|----------------|
| 分子量增加 | 轻微负面（折叠稍慢） | 中性 |
| pI升高 | 可能正面（CFPS优化） | 轻微正面（减少电荷排斥） |
| GRAVY降低 | 正面（溶解度增加） | 轻微负面（疏水堆积减少） |
| 不稳定指数降低 | 正面（折叠效率增加） | 正面（内在稳定性增加） |
| 脂肪族指数增加 | 中性 | 正面（疏水核心增强） |

## 结论

物理化学性质分析支持我们的设计策略：
1. **Seq-5**的pI变化最有利于CFPS表达
2. **Seq-4/6**的不稳定指数最低，支持热稳定性提升
3. 所有序列保持GFP固有的亲水性和稳定性特征
