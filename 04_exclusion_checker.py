#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exclusion List Checker
确保提交序列不与官方排除列表冲突
"""

import pandas as pd
import os
from typing import List, Set

SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)


def load_exclusion_list(filepath: str) -> Set[str]:
    """加载排除列表，支持多种格式"""
    if not os.path.exists(filepath):
        print(f"⚠️  Warning: {filepath} not found. Creating dummy exclusion list for testing.")
        # 模拟排除列表：包含WT本身和一些已知变体
        dummy = {
            SFGFP_WT,
            # 模拟一些已知变体
            SFGFP_WT[:221] + 'Q' + SFGFP_WT[222:],  # E222Q alone
        }
        return dummy

    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.csv':
        df = pd.read_csv(filepath)
        # 自动检测序列列
        seq_col = None
        for col in df.columns:
            if 'seq' in col.lower() or 'sequence' in col.lower():
                seq_col = col
                break
        if seq_col is None:
            seq_col = df.columns[0]  # 默认第一列
        return set(df[seq_col].astype(str).tolist())

    elif ext == '.fasta':
        sequences = []
        current_seq = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current_seq:
                        sequences.append(''.join(current_seq))
                        current_seq = []
                else:
                    current_seq.append(line)
            if current_seq:
                sequences.append(''.join(current_seq))
        return set(sequences)

    else:
        # 纯文本，每行一个序列
        with open(filepath, 'r') as f:
            return set(line.strip() for line in f if line.strip())


def check_against_exclusion(sequences: List[str], exclusion_list: Set[str]) -> pd.DataFrame:
    """逐一检查序列是否在排除列表中"""
    results = []

    for i, seq in enumerate(sequences, 1):
        # 完全匹配检查
        exact_match = seq in exclusion_list

        # 子序列检查（如果排除列表包含短片段）
        substring_match = False
        matched_to = None
        for excl_seq in exclusion_list:
            if len(excl_seq) < len(seq) and excl_seq in seq:
                substring_match = True
                matched_to = excl_seq[:20] + "..."
                break
            elif len(seq) < len(excl_seq) and seq in excl_seq:
                substring_match = True
                matched_to = excl_seq[:20] + "..."
                break

        # 相似度检查（Levenshtein距离，可选）
        # 这里简化为：与WT的相似度
        wt_similarity = sum(1 for a, b in zip(seq, SFGFP_WT) if a == b) / len(seq)

        results.append({
            'Seq_ID': i,
            'Length': len(seq),
            'Exact_Match': exact_match,
            'Substring_Match': substring_match,
            'Matched_To': matched_to if (exact_match or substring_match) else None,
            'WT_Similarity': round(wt_similarity, 3),
            'Status': '❌ EXCLUDED' if (exact_match or substring_match) else '✅ PASS',
            'Sequence_Prefix': seq[:30] + "..."
        })

    df = pd.DataFrame(results)
    return df


def generate_exclusion_report(sequences: List[str], 
                              exclusion_path: str = "data/Exclusion_List.csv",
                              output_path: str = "results/exclusion_check_report.csv"):
    """生成完整的排除列表检查报告"""

    print("=" * 60)
    print("Exclusion List Checker")
    print("=" * 60)

    # 加载排除列表
    exclusion_list = load_exclusion_list(exclusion_path)
    print(f"Loaded {len(exclusion_list)} sequences from exclusion list")

    # 检查
    df = check_against_exclusion(sequences, exclusion_list)

    # 保存报告
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    # 打印结果
    print(f"\nCheck Results:")
    print(df[['Seq_ID', 'Status', 'WT_Similarity', 'Exact_Match']].to_string(index=False))

    n_excluded = df['Exact_Match'].sum() + df['Substring_Match'].sum()
    print(f"\n{'='*60}")
    print(f"Summary: {n_excluded}/{len(sequences)} sequences excluded")
    print(f"Report saved: {output_path}")
    print(f"{'='*60}")

    return df


def main():
    # 示例：检查6条设计序列
    # 实际使用时从submission_final.csv读取

    test_sequences = [
        SFGFP_WT,  # 应该被排除（WT在排除列表中）
        SFGFP_WT[:221] + 'Q' + SFGFP_WT[222:],  # E222Q
        "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHKVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLQFVTAAGITHGMDELYK",  # N149K+E222Q
    ]

    generate_exclusion_report(test_sequences)

    print("\nTo check your actual submission:")
    print("  python scripts/04_exclusion_checker.py --input results/submission_final.csv")


if __name__ == "__main__":
    main()
