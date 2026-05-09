#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GFP Variant Assembler & Validator
组合突变生成最终序列，并进行格式校验
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Set, Tuple
import csv
import os

# sfGFP 野生型序列 (238 aa)
SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)

AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

# 绝对不可突变的位点 (发色团核心)
FORBIDDEN_POSITIONS = {64, 65, 66}  # 0-indexed: Y66, G67, 以及附近的催化残基


def apply_mutations(sequence: str, mutations: Dict[int, str]) -> str:
    """
    应用突变到序列
    mutations: {0-indexed_position: new_aa}
    """
    seq_list = list(sequence)

    for pos, new_aa in mutations.items():
        if pos < 0 or pos >= len(sequence):
            raise ValueError(f"Position {pos} out of range")
        if new_aa not in AMINO_ACIDS:
            raise ValueError(f"Invalid amino acid: {new_aa}")

        wt_aa = sequence[pos]
        seq_list[pos] = new_aa
        print(f"  Mutated pos {pos+1}: {wt_aa} -> {new_aa}")

    return "".join(seq_list)


def validate_sequence(seq: str, exclusion_list: Set[str] = None) -> Tuple[bool, str]:
    """
    校验序列是否符合提交要求
    """
    if exclusion_list is None:
        exclusion_list = set()

    # 1. 长度检查
    if not (220 <= len(seq) <= 250):
        return False, f"Length {len(seq)} not in [220, 250]"

    # 2. 必须以M开头
    if not seq.startswith('M'):
        return False, "Must start with Methionine (M)"

    # 3. 仅允许20种标准氨基酸
    invalid_chars = set(seq) - AMINO_ACIDS
    if invalid_chars:
        return False, f"Invalid characters: {invalid_chars}"

    # 4. 无终止密码子符号
    if '*' in seq or '.' in seq or '-' in seq:
        return False, "Contains forbidden symbols (*, ., -)"

    # 5. 排除列表检查
    if seq in exclusion_list:
        return False, "Sequence in exclusion list"

    # 6. 发色团检查 (Y66, G67必须保留)
    if seq[65] != 'Y' or seq[66] != 'G':
        return False, f"Chromophore damaged: pos66={seq[65]}, pos67={seq[66]}"

    return True, "Valid"


def load_exclusion_list(filepath: str) -> Set[str]:
    """加载排除列表"""
    if not os.path.exists(filepath):
        print(f"Warning: Exclusion list {filepath} not found, using empty set")
        return set()

    df = pd.read_csv(filepath)
    if 'Sequence' in df.columns:
        return set(df['Sequence'].tolist())
    else:
        # 假设第一列是序列
        return set(df.iloc[:, 0].tolist())


def generate_submission_csv(sequences: List[Tuple[str, str, Dict]], 
                           team_name: str,
                           output_path: str):
    """
    生成提交CSV
    sequences: list of (seq_id, sequence, mutations_dict)
    """
    rows = []
    for seq_id, seq, muts in sequences:
        mut_str = ";".join([f"{k+1}{SFGFP_WT[k]}{v}" for k, v in muts.items()]) if muts else "WT"
        rows.append({
            'Team_Name': team_name,
            'Seq_ID': seq_id,
            'Sequence': seq,
            'Mutations': mut_str,
            'Length': len(seq)
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Submission saved to {output_path}")
    return df


# ============================================================
# 6条序列的设计方案
# ============================================================

class GFPDesigner:
    """GFP变体设计师"""

    def __init__(self, wt_seq: str = SFGFP_WT):
        self.wt = wt_seq
        self.exclusion = set()

    def design_seq1_conservative(self) -> Tuple[str, Dict[int, str]]:
        """
        Seq-1: 保守基线
        sfGFP + 文献经典亮度/稳定突变组合
        策略：在sfGFP基础上叠加已知可共存的增益突变
        """
        muts = {
            63: 'L',   # F64L: EGFP经典亮度突变
            64: 'T',   # S65T: 经典亮度突变 (注意：这里会改变发色团前体，但增强亮度)
            221: 'Q',  # E222Q: 热稳定性增强
            148: 'K',  # N149K: 热稳定性增强
        }
        seq = apply_mutations(self.wt, muts)
        return seq, muts

    def design_seq2_thermo_focus(self) -> Tuple[str, Dict[int, str]]:
        """
        Seq-2: 热稳定优先
        在保守基础上增加更多稳定化突变
        """
        muts = {
            63: 'L',   # F64L
            64: 'T',   # S65T
            221: 'Q',  # E222Q
            148: 'K',  # N149K
            182: 'R',  # Q183R: 热稳定性
            217: 'V',  # M218V: 热稳定性
        }
        seq = apply_mutations(self.wt, muts)
        return seq, muts

    def design_seq3_brightness_focus(self) -> Tuple[str, Dict[int, str]]:
        """
        Seq-3: 亮度优先
        追求极致初始亮度
        """
        muts = {
            63: 'L',   # F64L
            64: 'T',   # S65T
            143: 'F',  # Y145F (sfGFP已有，但确认)
            169: 'V',  # I171V (sfGFP已有)
            204: 'V',  # A206V (sfGFP已有)
            37: 'N',   # Y39N (sfGFP已有)
        }
        # 注意：sfGFP已经包含很多这些突变，这里显式列出用于记录
        # 实际序列可能与WT相同或略有不同
        seq = apply_mutations(self.wt, muts)
        return seq, muts

    def design_seq4_balanced(self) -> Tuple[str, Dict[int, str]]:
        """
        Seq-4: 平衡型
        兼顾亮度与热稳定性，引入表面电荷优化
        """
        muts = {
            63: 'L',   # F64L
            64: 'T',   # S65T
            221: 'Q',  # E222Q
            148: 'K',  # N149K
            182: 'R',  # Q183R
            29: 'R',   # S30R (sfGFP已有)
            103: 'T',  # N105T (sfGFP已有)
        }
        seq = apply_mutations(self.wt, muts)
        return seq, muts

    def design_seq5_surface_optimized(self) -> Tuple[str, Dict[int, str]]:
        """
        Seq-5: 表面优化型
        优化表面残基以增强CFPS中的溶解度和折叠效率
        """
        muts = {
            63: 'L',   # F64L
            64: 'T',   # S65T
            221: 'Q',  # E222Q
            0: 'M',    # 确保以M开头 (已经是)
            14: 'E',   # D15E: 表面电荷调整
            46: 'K',   # E47K: 盐桥引入
            80: 'R',   # K81R: 表面正电荷
        }
        seq = apply_mutations(self.wt, muts)
        return seq, muts

    def design_seq6_exploratory(self) -> Tuple[str, Dict[int, str]]:
        """
        Seq-6: 探索型
        更大胆的组合，包含loop区修饰
        """
        muts = {
            63: 'L',   # F64L
            64: 'T',   # S65T
            221: 'Q',  # E222Q
            148: 'K',  # N149K
            182: 'R',  # Q183R
            217: 'V',  # M218V
            194: 'A',  # N195A: loop区疏水化
            230: 'I',  # S231I: C端稳定
        }
        seq = apply_mutations(self.wt, muts)
        return seq, muts

    def generate_all(self) -> List[Tuple[str, str, Dict[int, str]]]:
        """生成全部6条序列"""
        designs = [
            ("1", *self.design_seq1_conservative()),
            ("2", *self.design_seq2_thermo_focus()),
            ("3", *self.design_seq3_brightness_focus()),
            ("4", *self.design_seq4_balanced()),
            ("5", *self.design_seq5_surface_optimized()),
            ("6", *self.design_seq6_exploratory()),
        ]
        return designs


def main():
    designer = GFPDesigner()

    print("=" * 60)
    print("GFP Variant Design Pipeline")
    print("=" * 60)

    # 生成6条序列
    designs = designer.generate_all()

    # 校验
    print("\n" + "=" * 60)
    print("Validation Results")
    print("=" * 60)

    valid_designs = []
    for seq_id, seq, muts in designs:
        valid, msg = validate_sequence(seq)
        status = "✓ PASS" if valid else "✗ FAIL"
        print(f"Seq-{seq_id}: {status} ({msg}), Length={len(seq)}")
        if valid:
            valid_designs.append((seq_id, seq, muts))

    # 生成提交文件
    if valid_designs:
        output_path = "results/submission_sequences.csv"
        os.makedirs("results", exist_ok=True)
        generate_submission_csv(valid_designs, "Team_Example", output_path)

        # 同时生成纯序列文件用于排除列表比对
        with open("results/sequences_for_exclusion_check.txt", "w") as f:
            for _, seq, _ in valid_designs:
                f.write(seq + "\n")

    print("\nDone!")


if __name__ == "__main__":
    main()
