#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rosetta ddG Calculation Framework
计算单点突变的稳定性变化 (ΔΔG)
"""

import os
import subprocess
from typing import Dict, List

# Rosetta 路径 (需根据实际安装修改)
ROSETTA_BIN = "/path/to/rosetta/main/source/bin"

# 6条序列的突变（1-indexed用于Rosetta）
MUTATIONS = {
    'E222Q': {'chain': 'A', 'resi': 222, 'wt': 'E', 'mt': 'Q'},
    'N149K': {'chain': 'A', 'resi': 149, 'wt': 'N', 'mt': 'K'},
    'Q183R': {'chain': 'A', 'resi': 183, 'wt': 'Q', 'mt': 'R'},
    'M218V': {'chain': 'A', 'resi': 218, 'wt': 'M', 'mt': 'V'},
    'E14K':  {'chain': 'A', 'resi': 14,  'wt': 'E', 'mt': 'K'},
    'E47K':  {'chain': 'A', 'resi': 47,  'wt': 'E', 'mt': 'K'},
    'E173K': {'chain': 'A', 'resi': 173, 'wt': 'E', 'mt': 'K'},
    'L195A': {'chain': 'A', 'resi': 195, 'wt': 'L', 'mt': 'A'},
    'S231V': {'chain': 'A', 'resi': 231, 'wt': 'S', 'mt': 'V'},
}


def run_cartesian_ddg(pdb_path: str, mutation: Dict, output_dir: str):
    """
    运行Rosetta Cartesian ddG
    参考: https://www.rosettacommons.org/docs/latest/cartesian-ddG
    """
    os.makedirs(output_dir, exist_ok=True)

    mut_name = f"{mutation['wt']}{mutation['resi']}{mutation['mt']}"

    # 生成突变文件
    mutfile = os.path.join(output_dir, f"{mut_name}.mutfile")
    with open(mutfile, 'w') as f:
        f.write("total 1\n")
        f.write(f"1\n")
        f.write(f"{mutation['wt']} {mutation['resi']} {mutation['chain']} {mutation['mt']}\n")

    # Rosetta命令
    cmd = [
        f"{ROSETTA_BIN}/cartesian_ddg.default.linuxgccrelease",
        "-s", pdb_path,
        "-ddg::mut_file", mutfile,
        "-ddg::iterations", "3",
        "-ddg::cartesian",
        "-ddg::dump_pdbs", "true",
        "-bbnbr", "1",
        "-fa_max_dis", "9.0",
        "-out", output_dir,
    ]

    print(f"Running ddG for {mut_name}...")
    print(f"Command: {' '.join(cmd)}")

    # subprocess.run(cmd, check=True)


def run_flex_ddg(pdb_path: str, mutation: Dict, output_dir: str):
    """
    运行Rosetta Flex ddG（更精确但耗时）
    参考: https://github.com/Kortemme-Lab/flex_ddG_tutorial
    """
    os.makedirs(output_dir, exist_ok=True)
    mut_name = f"{mutation['wt']}{mutation['resi']}{mutation['mt']}"

    cmd = [
        "python", "run_flex_ddG.py",
        "--pdb", pdb_path,
        "--chain", mutation['chain'],
        "--resnum", str(mutation['resi']),
        "--wt", mutation['wt'],
        "--mut", mutation['mt'],
        "--output", output_dir,
    ]

    print(f"Running Flex ddG for {mut_name}...")
    print(f"Command: {' '.join(cmd)}")


def parse_ddg_results(output_dir: str) -> Dict[str, float]:
    """解析ddG结果"""
    results = {}

    # 读取Rosetta输出文件
    for fname in os.listdir(output_dir):
        if fname.endswith('.ddg'):
            with open(os.path.join(output_dir, fname)) as f:
                for line in f:
                    if 'ddG' in line:
                        parts = line.split()
                        mut_name = fname.replace('.ddg', '')
                        ddg = float(parts[-1])
                        results[mut_name] = ddg

    return results


def batch_ddg(pdb_path: str = "data/2b3p.pdb"):
    """批量计算所有突变"""
    output_base = "results/rosetta_ddg"

    print("=" * 60)
    print("Rosetta ddG Batch Calculation")
    print("=" * 60)
    print(f"PDB: {pdb_path}")
    print(f"Mutations: {len(MUTATIONS)}")

    for name, mut in MUTATIONS.items():
        out_dir = os.path.join(output_base, name)
        run_cartesian_ddg(pdb_path, mut, out_dir)

    print("\nParsing results...")
    results = parse_ddg_results(output_base)

    print("\nResults Summary:")
    print(f"{'Mutation':<15} {'ddG (kcal/mol)':<20} {'Effect'}")
    print("-" * 50)
    for name, ddg in sorted(results.items(), key=lambda x: x[1]):
        effect = "Stabilizing" if ddg < -0.5 else ("Neutral" if ddg < 0.5 else "Destabilizing")
        print(f"{name:<15} {ddg:<20.2f} {effect}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdb', default='data/2b3p.pdb', help='Input PDB')
    parser.add_argument('--method', choices=['cartesian', 'flex'], default='cartesian')
    args = parser.parse_args()

    batch_ddg(args.pdb)


if __name__ == "__main__":
    main()
