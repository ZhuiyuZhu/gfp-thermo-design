#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESM-2 Mutation Scoring Demo
模拟ESM-2打分流程，展示如何筛选有益突变
（实际运行时需安装 fair-esm 并加载真实模型）
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import os

SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)

AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")

# 保护区
CHROMOPHORE_CORE = {65, 66}  # Y66, G67
CHROMOPHORE_ENV = {
    56,57,58, 63,64,67,68, 93,94,95,96,97,98,99,
    144,145,146,147,148,149,150, 200,201,202,203,204,205,206,
    219,220,221,222,223,224
}
FORBIDDEN = CHROMOPHORE_CORE | CHROMOPHORE_ENV

# 文献已知突变效应（模拟ESM-2会学习到的模式）
# 负数 = 有益，正数 = 有害
LITERATURE_EFFECTS = {
    # 热稳定突变
    (221, 'Q'): -2.5,   # E222Q
    (148, 'K'): -1.8,   # N149K
    (182, 'R'): -2.0,   # Q183R
    (217, 'V'): -1.5,   # M218V
    (205, 'K'): -1.2,   # A206K
    # 亮度突变
    (63, 'L'): -1.5,    # F64L
    (64, 'T'): -1.2,    # S65T
    # 折叠增强
    (98, 'S'): -1.0,    # F99S (sfGFP已有)
    (152, 'T'): -0.8,   # M153T (sfGFP已有)
}


def simulate_esm2_score(position: int, wt_aa: str, mt_aa: str) -> float:
    """
    模拟ESM-2打分逻辑：
    - 基于残基性质变化（疏水→亲水、体积变化、电荷变化）
    - 结合文献先验知识
    - 添加随机噪声模拟模型不确定性
    """
    np.random.seed(position * ord(mt_aa))  # 可复现的随机

    base_score = 0.0

    # 1. 文献先验
    if (position, mt_aa) in LITERATURE_EFFECTS:
        base_score += LITERATURE_EFFECTS[(position, mt_aa)]

    # 2. 物理化学性质惩罚/奖励
    # 疏水性变化 (Kyte-Doolittle近似)
    hydrophobicity = {
        'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8,
        'G': -0.4, 'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8,
        'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5,
        'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3
    }

    delta_hydro = hydrophobicity[mt_aa] - hydrophobicity[wt_aa]

    # 内部位点（假设远离表面）偏好疏水，表面偏好亲水
    # 简单启发：位置>150认为是表面
    is_surface = position > 150 or position < 50

    if is_surface:
        # 表面：疏水→亲水通常有益（减少聚集）
        if delta_hydro < -1.5:
            base_score -= 0.5
        elif delta_hydro > 1.5:
            base_score += 0.8
    else:
        # 内部：亲水→疏水通常有益（增强堆积）
        if delta_hydro > 1.5:
            base_score -= 0.3
        elif delta_hydro < -1.5:
            base_score += 0.5

    # 3. 体积变化惩罚（内部大空腔不利）
    volume = {
        'A': 88, 'C': 108, 'D': 111, 'E': 138, 'F': 189,
        'G': 60, 'H': 153, 'I': 166, 'K': 168, 'L': 166,
        'M': 162, 'N': 114, 'P': 112, 'Q': 143, 'R': 173,
        'S': 89, 'T': 116, 'V': 140, 'W': 240, 'Y': 181
    }
    delta_vol = volume[mt_aa] - volume[wt_aa]
    if abs(delta_vol) > 50 and not is_surface:
        base_score += 0.3  # 内部大体积变化有风险

    # 4. 电荷变化（表面盐桥奖励）
    charge = {'D': -1, 'E': -1, 'K': 1, 'R': 1, 'H': 0.5}
    wt_charge = charge.get(wt_aa, 0)
    mt_charge = charge.get(mt_aa, 0)
    if is_surface and abs(mt_charge - wt_charge) > 0:
        base_score -= 0.4  # 表面电荷变化通常可容忍甚至有益

    # 5. 随机噪声（模拟模型不确定性）
    noise = np.random.normal(0, 0.5)

    final_score = base_score + noise
    return round(final_score, 3)


def scan_mutations(output_path: str = "results/esm2_simulated_scores.csv"):
    """扫描所有可设计位点"""
    results = []

    print("Simulating ESM-2 mutation scanning...")
    total = 0

    for pos in range(len(SFGFP_WT)):
        if pos in FORBIDDEN:
            continue

        wt_aa = SFGFP_WT[pos]
        for mt_aa in AMINO_ACIDS:
            if mt_aa == wt_aa:
                continue

            score = simulate_esm2_score(pos, wt_aa, mt_aa)

            # 标记文献支持
            is_lit = (pos, mt_aa) in LITERATURE_EFFECTS

            results.append({
                'position_1idx': pos + 1,
                'position_0idx': pos,
                'wt': wt_aa,
                'mt': mt_aa,
                'esm2_score': score,
                'literature_supported': is_lit,
                'region': 'surface' if (pos < 50 or pos > 150) else 'core'
            })
            total += 1

    df = pd.DataFrame(results)

    # 排序：文献支持优先，然后分数（越低越好）
    df = df.sort_values(['literature_supported', 'esm2_score'], 
                        ascending=[False, True])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Scanned {total} mutations. Saved to {output_path}")

    # 输出Top 30
    print("\nTop 30 Beneficial Mutations (score < -1.0 or literature):")
    top = df[(df['esm2_score'] < -1.0) | (df['literature_supported'])].head(30)
    print(top[['position_1idx', 'wt', 'mt', 'esm2_score', 'literature_supported']].to_string(index=False))

    return df


def analyze_position_hotspots(df: pd.DataFrame) -> pd.DataFrame:
    """分析哪些位点最容易接受突变"""
    # 按位点聚合：计算平均分数、最佳分数、可接受突变数
    agg = df.groupby('position_1idx').agg({
        'esm2_score': ['mean', 'min', 'count'],
        'literature_supported': 'sum'
    }).reset_index()
    agg.columns = ['position', 'avg_score', 'best_score', 'n_mutations', 'n_literature']

    # 筛选"热点"：best_score < -1 且 n_mutations >= 10
    hotspots = agg[agg['best_score'] < -1.0].sort_values('best_score')

    print("\nMutation Hotspots (positions with strong beneficial mutations):")
    print(hotspots.head(15).to_string(index=False))

    return hotspots


def recommend_combinations(df: pd.DataFrame, n: int = 10) -> List[Dict]:
    """推荐突变组合（简化版，不考虑上位效应）"""
    # 选取Top单点突变
    top_single = df[df['esm2_score'] < -1.2].head(20)

    combos = []
    # 简单组合：选取不邻近的位点（距离>5）
    positions = top_single['position_0idx'].tolist()
    scores = top_single['esm2_score'].tolist()
    muts = top_single['mt'].tolist()

    for i in range(min(n, len(positions))):
        for j in range(i+1, min(n, len(positions))):
            if abs(positions[i] - positions[j]) > 5:  # 不邻近
                combo = {
                    'mutations': {positions[i]: muts[i], positions[j]: muts[j]},
                    'expected_score': scores[i] + scores[j],  # 简化叠加
                    'positions': [positions[i]+1, positions[j]+1]
                }
                combos.append(combo)

    combos.sort(key=lambda x: x['expected_score'])

    print(f"\nTop 5 Mutation Combinations (additive model, distance > 5):")
    for i, c in enumerate(combos[:5], 1):
        mut_str = ";".join([f"{p}{SFGFP_WT[p-1]}{m}" for p, m in zip(c['positions'], c['mutations'].values())])
        print(f"  {i}. {mut_str} (expected score: {c['expected_score']:.2f})")

    return combos


def main():
    df = scan_mutations()
    hotspots = analyze_position_hotspots(df)
    combos = recommend_combinations(df)

    print("\n" + "="*60)
    print("ESM-2 Demo Complete")
    print("="*60)
    print("Next steps:")
    print("1. Review top mutations in PyMOL (scripts/03_structure_analysis.py)")
    print("2. Run Rosetta ddG for stability prediction")
    print("3. Select final 6 variants using 02_sequence_assembler_v2_1.py")


if __name__ == "__main__":
    main()
