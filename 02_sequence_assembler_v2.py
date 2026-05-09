#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GFP Variant Assembler & Validator (v2)
基于sfGFP骨架设计6条新突变序列
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Set, Tuple
import csv
import os

# sfGFP 野生型序列 (238 aa) - 作为母序列
SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)

AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

# ===== 关键保护区定义 (基于PDB 2B3P和文献) =====
# 发色团核心 (绝对不可动)
CHROMOPHORE_CORE = {65, 66}  # 0-indexed: Y66, G67

# 发色团催化/稳定环境 (8Å内，谨慎突变)
CHROMOPHORE_ENV = {
    56, 57, 58,       # W57 堆叠
    63, 64, 67, 68,   # 发色团邻近
    93, 94, 95, 96, 97, 98, 99,  # R96, F99区域
    144, 145, 146, 147, 148, 149, 150,  # H148区域
    200, 201, 202, 203, 204, 205, 206,  # T203, S205, A206区域
    219, 220, 221, 222, 223, 224,  # E222区域
}

# 已知在sfGFP中已优化的位点 (再突变风险高)
ALREADY_OPTIMIZED = {
    29, 38, 63, 64, 98, 104, 144, 152, 162, 170, 205
    # S30R, Y39N, F64L, S65T, F99S, N105T, Y145F, M153T, V163A, I171V, A206V
}


def apply_mutations(sequence: str, mutations: Dict[int, str]) -> str:
    """应用突变到序列"""
    seq_list = list(sequence)
    for pos, new_aa in mutations.items():
        wt_aa = sequence[pos]
        if new_aa == wt_aa:
            print(f"  [WARN] pos {pos+1}: {wt_aa} -> {new_aa} (no change)")
        else:
            print(f"  pos {pos+1}: {wt_aa} -> {new_aa}")
        seq_list[pos] = new_aa
    return "".join(seq_list)


def validate_sequence(seq: str, wt_seq: str = SFGFP_WT, exclusion_list: Set[str] = None) -> Tuple[bool, str]:
    """校验序列是否符合提交要求"""
    if exclusion_list is None:
        exclusion_list = set()

    checks = []

    # 1. 长度
    if not (220 <= len(seq) <= 250):
        checks.append(f"Length {len(seq)} not in [220,250]")
    else:
        checks.append(f"Length OK ({len(seq)})")

    # 2. M开头
    if not seq.startswith('M'):
        checks.append("Must start with M")
    else:
        checks.append("Starts with M OK")

    # 3. 标准氨基酸
    invalid = set(seq) - AMINO_ACIDS
    if invalid:
        checks.append(f"Invalid chars: {invalid}")
    else:
        checks.append("Standard AAs OK")

    # 4. 无终止符
    if '*' in seq or '.' in seq or '-' in seq:
        checks.append("Forbidden symbols")
    else:
        checks.append("No forbidden symbols")

    # 5. 排除列表
    if seq in exclusion_list:
        checks.append("In exclusion list!")

    # 6. 发色团保护
    if seq[65] != 'Y' or seq[66] != 'G':
        checks.append(f"CHROMOPHORE DAMAGED! pos66={seq[65]}, pos67={seq[66]}")
    else:
        checks.append("Chromophore OK")

    is_valid = all("OK" in c or "WARN" in c for c in checks)
    return is_valid, " | ".join(checks)


class GFPDesigner:
    """基于sfGFP设计6条突变序列"""

    def __init__(self, wt_seq: str = SFGFP_WT):
        self.wt = wt_seq

    def design_seq1_conservative(self) -> Tuple[str, Dict[int, str], str]:
        """
        Seq-1: 保守基线 (低风险)
        仅引入1个文献强支持的热稳定突变
        预期：亮度接近WT，稳定性略升
        """
        muts = {
            221: 'Q',  # E222Q: 经典热稳定突变，不破坏亮度
        }
        desc = "Conservative: E222Q only, minimal risk"
        seq = apply_mutations(self.wt, muts)
        return seq, muts, desc

    def design_seq2_thermo_dual(self) -> Tuple[str, Dict[int, str], str]:
        """
        Seq-2: 双热稳定突变
        E222Q + N149K，两个不冲突的稳定化突变
        """
        muts = {
            221: 'Q',  # E222Q
            148: 'K',  # N149K: 表面盐桥增强
        }
        desc = "Thermo dual: E222Q + N149K"
        seq = apply_mutations(self.wt, muts)
        return seq, muts, desc

    def design_seq3_thermo_triple(self) -> Tuple[str, Dict[int, str], str]:
        """
        Seq-3: 三热稳定突变
        增加Q183R，预期热稳定性显著提升
        """
        muts = {
            221: 'Q',  # E222Q
            148: 'K',  # N149K
            182: 'R',  # Q183R: 内部堆积优化
        }
        desc = "Thermo triple: E222Q + N149K + Q183R"
        seq = apply_mutations(self.wt, muts)
        return seq, muts, desc

    def design_seq4_thermo_max(self) -> Tuple[str, Dict[int, str], str]:
        """
        Seq-4: 极致热稳定
        加入M218V，四个热稳定突变组合
        风险：可能轻微影响折叠
        """
        muts = {
            221: 'Q',  # E222Q
            148: 'K',  # N149K
            182: 'R',  # Q183R
            217: 'V',  # M218V: C端稳定
        }
        desc = "Thermo max: E222Q + N149K + Q183R + M218V"
        seq = apply_mutations(self.wt, muts)
        return seq, muts, desc

    def design_seq5_folding_optimized(self) -> Tuple[str, Dict[int, str], str]:
        """
        Seq-5: CFPS折叠优化
        针对Cell-Free体系优化表面电荷和loop区
        策略：表面负电→正电，增强溶解度
        """
        muts = {
            221: 'Q',  # E222Q (基础稳定)
            13: 'K',   # E14K: N端表面电荷翻转
            46: 'K',   # E47K: loop区盐桥
            172: 'K',  # E173K: C端表面
        }
        desc = "CFPS optimized: surface charge engineering + E222Q"
        seq = apply_mutations(self.wt, muts)
        return seq, muts, desc

    def design_seq6_exploratory(self) -> Tuple[str, Dict[int, str], str]:
        """
        Seq-6: 探索型
        更大胆：loop区缩短+内部疏水优化
        高风险高回报
        """
        muts = {
            221: 'Q',  # E222Q
            148: 'K',  # N149K
            182: 'R',  # Q183R
            194: 'A',  # L195A: loop区疏水→亲水
            230: 'V',  # S231V: C端疏水锚定
        }
        desc = "Exploratory: loop engineering + C-term anchor"
        seq = apply_mutations(self.wt, muts)
        return seq, muts, desc

    def generate_all(self) -> List[Tuple[str, str, Dict[int, str], str]]:
        """生成全部6条序列"""
        methods = [
            self.design_seq1_conservative,
            self.design_seq2_thermo_dual,
            self.design_seq3_thermo_triple,
            self.design_seq4_thermo_max,
            self.design_seq5_folding_optimized,
            self.design_seq6_exploratory,
        ]
        designs = []
        for i, method in enumerate(methods, 1):
            seq, muts, desc = method()
            designs.append((str(i), seq, muts, desc))
        return designs


def generate_submission_csv(designs: List[Tuple], team_name: str, output_path: str):
    """生成提交CSV"""
    rows = []
    for seq_id, seq, muts, desc in designs:
        mut_str = ";".join([f"{k+1}{SFGFP_WT[k]}{v}" for k, v in sorted(muts.items())])
        rows.append({
            'Team_Name': team_name,
            'Seq_ID': seq_id,
            'Sequence': seq,
            'Mutations': mut_str,
            'Design_Strategy': desc,
            'Length': len(seq)
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"\nSubmission saved: {output_path}")
    return df


def main():
    designer = GFPDesigner()

    print("=" * 70)
    print("GFP Variant Design Pipeline v2 - sfGFP Based")
    print("=" * 70)

    designs = designer.generate_all()

    print("\n" + "=" * 70)
    print("Validation & Sequence Details")
    print("=" * 70)

    valid_designs = []
    for seq_id, seq, muts, desc in designs:
        valid, msg = validate_sequence(seq)
        status = "✓ PASS" if valid else "✗ FAIL"
        print(f"\nSeq-{seq_id}: {status}")
        print(f"  Strategy: {desc}")
        print(f"  Length: {len(seq)} | {msg}")
        print(f"  Mutations: {';'.join([f'{k+1}{SFGFP_WT[k]}{v}' for k,v in sorted(muts.items())])}")
        print(f"  Seq: {seq[:50]}...{seq[-20:]}")
        if valid:
            valid_designs.append((seq_id, seq, muts, desc))

    if valid_designs:
        os.makedirs("results", exist_ok=True)
        df = generate_submission_csv(valid_designs, "YourTeamName", "results/submission_final.csv")

        # 生成排除列表检查文件
        with open("results/sequences_for_exclusion_check.txt", "w") as f:
            for _, seq, _, _ in valid_designs:
                f.write(seq + "\n")

        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(df[['Seq_ID', 'Length', 'Mutations', 'Design_Strategy']].to_string(index=False))

    print("\nDone!")


if __name__ == "__main__":
    main()
