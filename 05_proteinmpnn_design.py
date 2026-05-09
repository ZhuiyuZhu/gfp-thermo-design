#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProteinMPNN Sequence Redesign for GFP
固定骨架，重新设计表面残基序列
"""

import os
import json

# ProteinMPNN 运行参数
MPNN_CONFIG = {
    "pdb_path": "data/2b3p.pdb",
    "output_dir": "results/mpnn_designs",
    "num_seq_per_target": 10,
    "sampling_temp": 0.1,  # 低温度 = 更保守
    "batch_size": 1,

    # 固定位置（不可设计）
    "fixed_positions": "56,57,58,63,64,65,66,67,68,93,94,95,96,97,98,99,144,145,146,147,148,149,150,200,201,202,203,204,205,206,219,220,221,222,223,224",

    # 设计链
    "chains_to_design": "A",

    # 其他参数
    "omit_AAs": "CX",  # 省略Cys（避免非预期二硫键）和特殊氨基酸
    "bias_AA_dict": {
        "K": 0.5,   # 偏好Lys（表面正电荷）
        "R": 0.5,   # 偏好Arg
        "E": -0.3,  # 减少Glu（表面负电荷过多）
        "D": -0.3   # 减少Asp
    }
}


def generate_mpnn_command(config: dict) -> str:
    """生成ProteinMPNN运行命令"""
    cmd = f"""python ProteinMPNN/protein_mpnn_run.py \
        --pdb_path {config['pdb_path']} \
        --out_folder {config['output_dir']} \
        --num_seq_per_target {config['num_seq_per_target']} \
        --sampling_temp {config['sampling_temp']} \
        --batch_size {config['batch_size']} \
        --fixed_positions {config['fixed_positions']} \
        --chains_to_design {config['chains_to_design']} \
        --omit_AAs {config['omit_AAs']}
    """

    # 如果有AA bias，需要额外处理（ProteinMPNN的bias通过json传入）
    if 'bias_AA_dict' in config:
        bias_path = os.path.join(config['output_dir'], 'aa_bias.json')
        os.makedirs(config['output_dir'], exist_ok=True)
        with open(bias_path, 'w') as f:
            json.dump(config['bias_AA_dict'], f)
        cmd += f"\n        --bias_by_res_jsonl {bias_path}"

    return cmd


def parse_mpnn_results(output_dir: str) -> list:
    """解析ProteinMPNN输出，提取序列"""
    import glob

    fasta_files = glob.glob(f"{output_dir}/*.fa")
    sequences = []

    for fa_file in fasta_files:
        with open(fa_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith('>'):
                    header = line.strip()
                    seq = lines[i+1].strip() if i+1 < len(lines) else ""
                    sequences.append({
                        'source': fa_file,
                        'header': header,
                        'sequence': seq,
                        'length': len(seq)
                    })

    return sequences


def main():
    print("=" * 60)
    print("ProteinMPNN Design Setup for GFP")
    print("=" * 60)

    print("\nConfiguration:")
    for k, v in MPNN_CONFIG.items():
        print(f"  {k}: {v}")

    print("\nGenerated Command:")
    cmd = generate_mpnn_command(MPNN_CONFIG)
    print(cmd)

    print("\nDesign Strategy:")
    print("  1. Fix chromophore environment (36 positions)")
    print("  2. Redesign surface loops and termini")
    print("  3. Bias toward Lys/Arg (positive surface charge)")
    print("  4. Omit Cys to avoid spurious disulfides")
    print("  5. Low sampling temp (0.1) for conservative designs")

    print("\nAfter running, use parse_mpnn_results() to extract sequences")
    print("Then run ESM-2 scoring and Rosetta ddG on MPNN outputs")


if __name__ == "__main__":
    main()
