#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Submission Checker
一键检查所有提交要求
"""

import pandas as pd
import os
import sys
from typing import List, Set, Tuple

SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)
AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


class SubmissionValidator:
    """提交文件完整校验器"""

    def __init__(self, exclusion_list_path: str = "data/Exclusion_List.csv"):
        self.exclusion = self._load_exclusion(exclusion_list_path)
        self.errors = []
        self.warnings = []

    def _load_exclusion(self, path: str) -> Set[str]:
        if not os.path.exists(path):
            print(f"⚠️  Exclusion list not found at {path}, using empty set")
            return set()
        df = pd.read_csv(path)
        seq_col = [c for c in df.columns if 'seq' in c.lower()][0]
        return set(df[seq_col].astype(str).tolist())

    def validate_csv_format(self, csv_path: str) -> pd.DataFrame:
        """检查CSV格式"""
        print("\n📋 [1/6] Checking CSV format...")

        if not os.path.exists(csv_path):
            self.errors.append(f"File not found: {csv_path}")
            return None

        df = pd.read_csv(csv_path)

        # 检查必需列
        required = ['Team_Name', 'Seq_ID', 'Sequence']
        missing = [c for c in required if c not in df.columns]
        if missing:
            self.errors.append(f"Missing columns: {missing}")

        # 检查序列数量
        if len(df) > 6:
            self.errors.append(f"Too many sequences: {len(df)} (max 6)")
        elif len(df) < 6:
            self.warnings.append(f"Only {len(df)} sequences submitted (max 6 allowed)")

        print(f"   ✓ Columns: {list(df.columns)}")
        print(f"   ✓ Sequences: {len(df)}")
        return df

    def validate_sequence_content(self, df: pd.DataFrame):
        """检查每条序列内容"""
        print("\n🔬 [2/6] Checking sequence content...")

        for idx, row in df.iterrows():
            seq_id = row.get('Seq_ID', f'Row_{idx}')
            seq = str(row.get('Sequence', ''))

            # 长度
            if not (220 <= len(seq) <= 250):
                self.errors.append(f"Seq-{seq_id}: Length {len(seq)} not in [220,250]")

            # M开头
            if not seq.startswith('M'):
                self.errors.append(f"Seq-{seq_id}: Does not start with M")

            # 标准氨基酸
            invalid = set(seq) - AMINO_ACIDS
            if invalid:
                self.errors.append(f"Seq-{seq_id}: Invalid chars {invalid}")

            # 终止符
            if '*' in seq or '.' in seq or '-' in seq:
                self.errors.append(f"Seq-{seq_id}: Contains forbidden symbols")

            # 发色团
            if len(seq) > 66:
                if seq[65] != 'Y' or seq[66] != 'G':
                    self.errors.append(f"Seq-{seq_id}: Chromophore damaged (pos66={seq[65]}, pos67={seq[66]})")

            # 排除列表
            if seq in self.exclusion:
                self.errors.append(f"Seq-{seq_id}: Found in exclusion list!")

            # 与WT相似度（预警）
            if len(seq) == len(SFGFP_WT):
                sim = sum(a==b for a,b in zip(seq, SFGFP_WT)) / len(seq)
                if sim < 0.85:
                    self.warnings.append(f"Seq-{seq_id}: Low similarity to WT ({sim:.1%}), verify design intent")
                elif sim == 1.0:
                    self.warnings.append(f"Seq-{seq_id}: Identical to WT, may be excluded")

        print(f"   Checked {len(df)} sequences")

    def validate_team_name(self, df: pd.DataFrame):
        """检查队伍名"""
        print("\n👥 [3/6] Checking team name...")

        teams = df['Team_Name'].unique()
        if len(teams) > 1:
            self.errors.append(f"Multiple team names: {teams}")
        elif len(teams) == 0:
            self.errors.append("No team name found")
        else:
            print(f"   Team: {teams[0]}")

    def validate_seq_ids(self, df: pd.DataFrame):
        """检查Seq_ID"""
        print("\n🔢 [4/6] Checking Seq_IDs...")

        ids = df['Seq_ID'].tolist()
        if len(ids) != len(set(ids)):
            self.errors.append("Duplicate Seq_IDs found")

        expected = ['1', '2', '3', '4', '5', '6']
        missing = [i for i in expected if i not in ids]
        if missing:
            self.warnings.append(f"Missing Seq_IDs: {missing}")

        print(f"   IDs: {ids}")

    def validate_no_duplicates(self, df: pd.DataFrame):
        """检查序列间是否有重复"""
        print("\n🔄 [5/6] Checking for duplicate sequences...")

        seqs = df['Sequence'].tolist()
        unique = set(seqs)
        if len(seqs) != len(unique):
            self.errors.append("Duplicate sequences within submission")

        print(f"   Unique: {len(unique)}/{len(seqs)}")

    def validate_exclusion_list(self, df: pd.DataFrame):
        """最终排除列表检查"""
        print("\n🚫 [6/6] Final exclusion list check...")

        if not self.exclusion:
            print("   Skipped (no exclusion list loaded)")
            return

        matches = 0
        for idx, row in df.iterrows():
            seq = str(row['Sequence'])
            if seq in self.exclusion:
                matches += 1
                self.errors.append(f"Seq-{row['Seq_ID']}: EXCLUDED")

        print(f"   Matches found: {matches}")

    def generate_report(self, output_path: str = "results/final_check_report.txt"):
        """生成检查报告"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("GFP Submission Final Check Report\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"ERRORS ({len(self.errors)}):\n")
            for e in self.errors:
                f.write(f"  ❌ {e}\n")

            f.write(f"\nWARNINGS ({len(self.warnings)}):\n")
            for w in self.warnings:
                f.write(f"  ⚠️  {w}\n")

            if not self.errors:
                f.write("\n✅ ALL CHECKS PASSED - Ready for submission!\n")
            else:
                f.write(f"\n❌ {len(self.errors)} ERRORS FOUND - Fix before submission!\n")

        print(f"\n{'='*60}")
        print("FINAL REPORT")
        print(f"{'='*60}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print("\n❌ FAILED - Fix errors before submission:")
            for e in self.errors:
                print(f"   • {e}")
        else:
            print("\n✅ PASSED - Ready to submit!")

        if self.warnings:
            print("\n⚠️  Warnings (non-blocking):")
            for w in self.warnings:
                print(f"   • {w}")

        print(f"\nReport saved: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Final submission checker')
    parser.add_argument('--input', default='results/submission_final.csv', help='Submission CSV')
    parser.add_argument('--exclusion', default='data/Exclusion_List.csv', help='Exclusion list')
    parser.add_argument('--output', default='results/final_check_report.txt', help='Report output')
    args = parser.parse_args()

    validator = SubmissionValidator(args.exclusion)

    print("=" * 60)
    print("GFP Submission Final Check")
    print("=" * 60)

    df = validator.validate_csv_format(args.input)
    if df is not None:
        validator.validate_sequence_content(df)
        validator.validate_team_name(df)
        validator.validate_seq_ids(df)
        validator.validate_no_duplicates(df)
        validator.validate_exclusion_list(df)

    validator.generate_report(args.output)

    # 返回退出码
    sys.exit(0 if not validator.errors else 1)


if __name__ == "__main__":
    main()
