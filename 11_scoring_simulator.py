#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Competition Scoring Simulator
模拟不同表现下的得分，帮助理解得分机制
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple


def calculate_scores(finitial: float, ffinal: float, 
                     finitial_wt: float = 1.0) -> Tuple[float, float, float, str]:
    """
    计算单条序列的得分

    Args:
        finitial: 初始亮度
        ffinal: 热后亮度
        finitial_wt: WT初始亮度（归一化为1.0）

    Returns:
        (brightness_score, stability_score, total_score, status)
    """
    brightness_score = finitial / finitial_wt

    # 淘汰检查
    if finitial < 0.3 * finitial_wt:
        return 0.0, 0.0, 0.0, "ELIMINATED"

    stability_score = ffinal / finitial if finitial > 0 else 0
    total_score = brightness_score * stability_score

    status = "PASS"
    return brightness_score, stability_score, total_score, status


def simulate_team_performance(designs: Dict[str, Dict]):
    """
    模拟队伍表现

    designs: {
        'Seq-1': {'finitial': 0.95, 'ffinal': 1.10, 'name': 'Conservative'},
        ...
    }
    """
    results = []

    for seq_id, params in designs.items():
        finitial = params['finitial']
        ffinal = params['ffinal']
        name = params.get('name', seq_id)

        b, s, t, status = calculate_scores(finitial, ffinal)

        results.append({
            'Seq_ID': seq_id,
            'Name': name,
            'Finitial': finitial,
            'Ffinal': ffinal,
            'Brightness_Score': round(b, 3),
            'Stability_Score': round(s, 3),
            'Total_Score': round(t, 3),
            'Status': status,
        })

    df = pd.DataFrame(results)

    # 找出Top-1
    valid = df[df['Status'] == 'PASS']
    if len(valid) > 0:
        top1 = valid.loc[valid['Total_Score'].idxmax()]
        df['Is_Top1'] = df['Seq_ID'] == top1['Seq_ID']
    else:
        df['Is_Top1'] = False

    return df


def run_scenarios():
    """运行多种场景模拟"""

    scenarios = {
        "保守成功": {
            'Seq-1': {'finitial': 0.95, 'ffinal': 1.10, 'name': 'Conservative'},
            'Seq-2': {'finitial': 0.92, 'ffinal': 1.15, 'name': 'Thermo Dual'},
            'Seq-3': {'finitial': 0.88, 'ffinal': 1.20, 'name': 'Thermo Triple'},
            'Seq-4': {'finitial': 0.82, 'ffinal': 1.25, 'name': 'Thermo Max'},
            'Seq-5': {'finitial': 0.93, 'ffinal': 1.12, 'name': 'CFPS Opt'},
            'Seq-6': {'finitial': 0.78, 'ffinal': 1.30, 'name': 'Exploratory'},
        },
        "激进成功": {
            'Seq-1': {'finitial': 0.95, 'ffinal': 1.10, 'name': 'Conservative'},
            'Seq-2': {'finitial': 0.92, 'ffinal': 1.15, 'name': 'Thermo Dual'},
            'Seq-3': {'finitial': 0.85, 'ffinal': 1.25, 'name': 'Thermo Triple'},
            'Seq-4': {'finitial': 0.80, 'ffinal': 1.35, 'name': 'Thermo Max'},
            'Seq-5': {'finitial': 0.93, 'ffinal': 1.12, 'name': 'CFPS Opt'},
            'Seq-6': {'finitial': 0.75, 'ffinal': 1.45, 'name': 'Exploratory'},
        },
        "亮度灾难": {
            'Seq-1': {'finitial': 0.95, 'ffinal': 1.10, 'name': 'Conservative'},
            'Seq-2': {'finitial': 0.92, 'ffinal': 1.15, 'name': 'Thermo Dual'},
            'Seq-3': {'finitial': 0.25, 'ffinal': 0.30, 'name': 'Thermo Triple'},  # 淘汰！
            'Seq-4': {'finitial': 0.20, 'ffinal': 0.25, 'name': 'Thermo Max'},    # 淘汰！
            'Seq-5': {'finitial': 0.93, 'ffinal': 1.12, 'name': 'CFPS Opt'},
            'Seq-6': {'finitial': 0.15, 'ffinal': 0.20, 'name': 'Exploratory'},  # 淘汰！
        },
        "全部中等": {
            'Seq-1': {'finitial': 0.90, 'ffinal': 1.08, 'name': 'Conservative'},
            'Seq-2': {'finitial': 0.88, 'ffinal': 1.10, 'name': 'Thermo Dual'},
            'Seq-3': {'finitial': 0.85, 'ffinal': 1.12, 'name': 'Thermo Triple'},
            'Seq-4': {'finitial': 0.82, 'ffinal': 1.14, 'name': 'Thermo Max'},
            'Seq-5': {'finitial': 0.88, 'ffinal': 1.09, 'name': 'CFPS Opt'},
            'Seq-6': {'finitial': 0.80, 'ffinal': 1.15, 'name': 'Exploratory'},
        },
    }

    all_results = {}
    for scenario_name, designs in scenarios.items():
        df = simulate_team_performance(designs)
        all_results[scenario_name] = df

    return all_results


def visualize_scenarios(results: Dict[str, pd.DataFrame]):
    """可视化多种场景"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, (scenario, df) in enumerate(results.items()):
        ax = axes[idx]

        colors = ['#e74c3c' if s == 'ELIMINATED' else '#2ecc71' for s in df['Status']]

        x = np.arange(len(df))
        width = 0.35

        bars1 = ax.bar(x - width/2, df['Brightness_Score'], width, label='Brightness', color='#3498db', alpha=0.8)
        bars2 = ax.bar(x + width/2, df['Stability_Score'], width, label='Stability', color='#e67e22', alpha=0.8)

        # 标注总分
        for i, (b, s, total, status) in enumerate(zip(df['Brightness_Score'], 
                                                      df['Stability_Score'], 
                                                      df['Total_Score'],
                                                      df['Status'])):
            if status == 'PASS':
                ax.text(i, max(b, s) + 0.05, f'Total: {total:.2f}', ha='center', fontsize=8, fontweight='bold')
            else:
                ax.text(i, 0.1, 'ELIMINATED', ha='center', fontsize=9, color='red', fontweight='bold')

        ax.set_xlabel('Sequence')
        ax.set_ylabel('Score')
        ax.set_title(f'{scenario} Scenario', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Seq_ID'], rotation=45)
        ax.legend()
        ax.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Elimination line')
        ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/figures/fig7_scoring_scenarios.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    print("=" * 60)
    print("Competition Scoring Simulator")
    print("=" * 60)

    results = run_scenarios()

    for scenario, df in results.items():
        print(f"
{'='*60}")
        print(f"Scenario: {scenario}")
        print(f"{'='*60}")
        print(df[['Seq_ID', 'Finitial', 'Ffinal', 'Brightness_Score', 
                  'Stability_Score', 'Total_Score', 'Status']].to_string(index=False))

        valid = df[df['Status'] == 'PASS']
        if len(valid) > 0:
            top1 = valid.loc[valid['Total_Score'].idxmax()]
            print(f"
🏆 Top-1: {top1['Seq_ID']} (Score: {top1['Total_Score']:.3f})")
        else:
            print("
❌ All sequences eliminated!")

    visualize_scenarios(results)
    print("
✅ Scenario visualization saved")


if __name__ == "__main__":
    main()
