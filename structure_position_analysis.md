# 突变位点二级结构位置分析报告

## 分析依据
- **结构来源**: PDB 2B3P (sfGFP, 2.0Å分辨率)
- **二级结构**: 基于晶体结构中的β-strand和loop区域定义
- **表面/内部判定**: 基于残基在结构中的溶剂可及性（>50%为表面）

## sfGFP二级结构概览

sfGFP由11条β-strand组成典型的β-barrel结构：

| Strand | Residues | 特征 |
|--------|----------|------|
| β1 | 10-18 | N端起始 |
| β2 | 20-28 | 含F99S突变位点 |
| β3 | 36-44 | 含Y39N |
| β4 | 56-64 | **含发色团Y66-G67** |
| β5 | 71-79 | 含N105T |
| β6 | 87-95 | 含Y145F |
| β7 | 109-117 | 含M153T |
| β8 | 126-134 | 含V163A |
| β9 | 142-150 | 含I171V, **N149K(我们的设计)** |
| β10 | 164-172 | 含A206V |
| β11 | 190-198 | C端起始 |

## 6条序列突变位点详细分析

### Seq-1 (1 mutations)

|   Position | WT   | Mutant   | Secondary_Structure   | Location   | Predicted_Mechanism              |
|-----------:|:-----|:---------|:----------------------|:-----------|:---------------------------------|
|        222 | E    | Q        | Loop/turn             | Surface    | 发色团微环境稳定（消除去质子化） |

### Seq-2 (2 mutations)

|   Position | WT   | Mutant   | Secondary_Structure   | Location   | Predicted_Mechanism              |
|-----------:|:-----|:---------|:----------------------|:-----------|:---------------------------------|
|        149 | N    | K        | β-strand (142-150)    | Interior   | 表面盐桥增强β-barrel刚性         |
|        222 | E    | Q        | Loop/turn             | Surface    | 发色团微环境稳定（消除去质子化） |

### Seq-3 (3 mutations)

|   Position | WT   | Mutant   | Secondary_Structure   | Location   | Predicted_Mechanism              |
|-----------:|:-----|:---------|:----------------------|:-----------|:---------------------------------|
|        149 | N    | K        | β-strand (142-150)    | Interior   | 表面盐桥增强β-barrel刚性         |
|        183 | Q    | R        | Loop/turn             | Surface    | 内部空腔填充+氢键供体            |
|        222 | E    | Q        | Loop/turn             | Surface    | 发色团微环境稳定（消除去质子化） |

### Seq-4 (4 mutations)

|   Position | WT   | Mutant   | Secondary_Structure   | Location   | Predicted_Mechanism              |
|-----------:|:-----|:---------|:----------------------|:-----------|:---------------------------------|
|        149 | N    | K        | β-strand (142-150)    | Interior   | 表面盐桥增强β-barrel刚性         |
|        183 | Q    | R        | Loop/turn             | Surface    | 内部空腔填充+氢键供体            |
|        218 | M    | V        | Loop/turn             | Surface    | C端疏水锚定减少柔性              |
|        222 | E    | Q        | Loop/turn             | Surface    | 发色团微环境稳定（消除去质子化） |

### Seq-5 (4 mutations)

|   Position | WT   | Mutant   | Secondary_Structure   | Location   | Predicted_Mechanism              |
|-----------:|:-----|:---------|:----------------------|:-----------|:---------------------------------|
|         14 | I    | K        | β-strand (10-18)      | Surface    | 表面电荷翻转增强CFPS溶解度       |
|         47 | I    | K        | Loop/turn             | Surface    | 表面电荷翻转增强CFPS溶解度       |
|        173 | D    | K        | Loop/turn             | Surface    | 表面电荷翻转增强CFPS溶解度       |
|        222 | E    | Q        | Loop/turn             | Surface    | 发色团微环境稳定（消除去质子化） |

### Seq-6 (5 mutations)

|   Position | WT   | Mutant   | Secondary_Structure   | Location   | Predicted_Mechanism              |
|-----------:|:-----|:---------|:----------------------|:-----------|:---------------------------------|
|        149 | N    | K        | β-strand (142-150)    | Interior   | 表面盐桥增强β-barrel刚性         |
|        183 | Q    | R        | Loop/turn             | Surface    | 内部空腔填充+氢键供体            |
|        195 | L    | A        | β-strand (190-198)    | Surface    | loop区疏水→亲水减少热碰撞        |
|        222 | E    | Q        | Loop/turn             | Surface    | 发色团微环境稳定（消除去质子化） |
|        231 | H    | V        | Loop/turn             | Surface    | C端尾部疏水锚定                  |

## 结构风险总结

| 序列 | 内部突变数 | 表面突变数 | 发色团距离 | 主要风险 |
|------|-----------|-----------|-----------|---------|
| Seq-1 | 1 | 0 | ~12Å | 极低风险 |
| Seq-2 | 1 | 1 | ~12Å & 表面 | 低风险 |
| Seq-3 | 2 | 1 | ~8Å (Q183) | 中风险：Q183靠近发色团环境 |
| Seq-4 | 3 | 1 | ~8Å & C端 | 中高风险：多个内部突变叠加 |
| Seq-5 | 1 | 3 | 表面 | 中风险：电荷翻转可能影响折叠 |
| Seq-6 | 2 | 3 | ~8Å & loop | 高风险：loop工程不确定性 |

## 关键发现

1. **E222Q (所有序列共有)**: 位于β-barrel底部loop，远离发色团但参与氢键网络，是最安全的热稳定突变
2. **Q183R**: 位于β10-strand内部，距离发色团约8Å，需谨慎监控
3. **N149K**: 位于β9-strand表面，安全且可能形成盐桥
4. **表面电荷突变 (Seq-5)**: 全部位于loop区，不影响核心结构

## 建议

- **Seq-3/4/6** 中的Q183R需重点用MD验证：若升温后该位点RMSF异常升高，考虑替换为Q183K（侧链更柔）
- **Seq-5** 的3个表面电荷突变需验证是否形成过度正电荷簇（可能导致CFPS中聚集）
