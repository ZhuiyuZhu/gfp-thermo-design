#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESM-2 GFP Mutation Effect Predictor
用于预测sfGFP单点突变对蛋白质稳定性的影响
"""

import torch
import esm
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
import argparse

# sfGFP 野生型序列 (238 aa)
SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)

# 20种标准氨基酸
AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")

# ===== 关键位点定义 =====
# 发色团形成位点 (绝对不可突变)
CHROMOPHORE_SITES = {65, 66, 67}  # 0-indexed: Y66, G67 (以及附近的Y64)
# 注意：使用0-indexed，即序列中的第66位对应index 65

# 发色团周围 8Å 保护圈 (基于PDB 2B3P结构分析)
# 这些位点突变可能破坏发色团微环境
CHROMOPHORE_ENVIRONMENT = {
    56, 57, 58,  # W57 附近
    64, 65, 66, 67, 68, 69,  # 发色团核心
    93, 94, 95, 96, 97, 98,  # R96 附近
    145, 146, 147, 148, 149,  # H148 附近
    201, 202, 203, 204, 205,  # T203, S205 附近
    219, 220, 221, 222, 223,  # E222 附近
}

# sfGFP已包含的突变 (相对于野生型GFP)
# S30R, Y39N, N105T, Y145F, I171V, A206V
# 以及 cycle3: F99S, M153T, V163A
SFGFP_MUTATIONS = {
    29: 'R',  # S30R
    38: 'N',  # Y39N
    98: 'S',  # F99S
    104: 'T', # N105T
    144: 'F', # Y145F
    152: 'T', # M153T
    162: 'A', # V163A
    170: 'V', # I171V
    205: 'V', # A206V
}

# 已知有益突变库 (基于文献)
BENEFICIAL_MUTATIONS = {
    # 亮度增强
    'brightness': {
        63: ['L', 'W'],   # F64L (经典EGFP突变)
        64: ['T'],        # S65T (经典)
        144: ['F'],       # Y145F (sfGFP已有)
        170: ['V'],       # I171V (sfGFP已有)
    },
    # 热稳定性增强
    'thermostability': {
        205: ['V', 'K'],  # A206V/K
        221: ['Q', 'G'],  # E222Q/G
        148: ['K', 'R'],  # N149K/R
        182: ['R', 'K'],  # Q183R/K
        98:  ['S'],       # F99S (cycle3, sfGFP已有)
        152: ['T'],       # M153T (cycle3, sfGFP已有)
        162: ['A'],       # V163A (cycle3, sfGFP已有)
        217: ['V'],       # M218V
    },
    # 折叠增强 (CFPS友好)
    'folding': {
        29:  ['R'],       # S30R (sfGFP已有)
        38:  ['N'],       # Y39N (sfGFP已有)
        104: ['T'],       # N105T (sfGFP已有)
        98:  ['S'],       # F99S
        152: ['T'],       # M153T
        162: ['A'],       # V163A
    }
}


def load_esm2_model(model_name: str = "esm2_t33_650M_UR50D"):
    """加载ESM-2模型"""
    print(f"Loading {model_name}...")
    model, alphabet = esm.pretrained.load_model_and_alphabet(model_name)
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()
        print("Using CUDA")
    else:
        print("Using CPU")
    return model, alphabet


def compute_mutant_score(model, alphabet, sequence: str, position: int, mutant_aa: str) -> float:
    """
    计算单点突变的伪对数似然分数 (pseudo-log-likelihood)
    分数越低(越负)表示该突变越不被模型偏好
    我们用野生型概率 - 突变型概率 作为效应值
    """
    batch_converter = alphabet.get_batch_converter()

    # 准备数据
    data = [("protein", sequence)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)

    if torch.cuda.is_available():
        batch_tokens = batch_tokens.cuda()

    # 获取模型输出
    with torch.no_grad():
        results = model(batch_tokens, return_contacts=False)

    # 获取指定位置的logits
    # ESM输出是 (batch, seq_len, vocab_size)
    logits = results["logits"][0, position + 1]  # +1 因为ESM有特殊的begin token

    # 计算概率
    probs = torch.softmax(logits, dim=-1)

    wt_aa = sequence[position]
    mt_aa = mutant_aa

    wt_idx = alphabet.get_idx(wt_aa)
    mt_idx = alphabet.get_idx(mt_aa)

    wt_prob = probs[wt_idx].item()
    mt_prob = probs[mt_idx].item()

    # 突变效应 = log(P_wt) - log(P_mt)
    # 正值表示野生型更被偏好(突变有害)，负值表示突变更被偏好(突变有益)
    effect = np.log(wt_prob + 1e-10) - np.log(mt_prob + 1e-10)

    return effect, wt_prob, mt_prob


def scan_all_mutations(model, alphabet, sequence: str, 
                       exclude_positions: set = None) -> pd.DataFrame:
    """
    扫描所有可能的单点突变
    """
    if exclude_positions is None:
        exclude_positions = set()

    results = []

    for pos in range(len(sequence)):
        if pos in exclude_positions:
            continue

        wt_aa = sequence[pos]
        for mt_aa in AMINO_ACIDS:
            if mt_aa == wt_aa:
                continue

            try:
                effect, wt_prob, mt_prob = compute_mutant_score(
                    model, alphabet, sequence, pos, mt_aa
                )

                results.append({
                    'position_1indexed': pos + 1,
                    'position_0indexed': pos,
                    'wt_aa': wt_aa,
                    'mt_aa': mt_aa,
                    'esm2_effect': effect,
                    'wt_prob': wt_prob,
                    'mt_prob': mt_prob,
                    'is_beneficial_lit': False,  # 后面标记
                })
            except Exception as e:
                print(f"Error at pos {pos}, {wt_aa}->{mt_aa}: {e}")
                continue

    df = pd.DataFrame(results)
    return df


def mark_beneficial_mutations(df: pd.DataFrame) -> pd.DataFrame:
    """标记文献中已知的有益突变"""
    def check_beneficial(row):
        pos = row['position_0indexed']
        mt = row['mt_aa']

        for category, muts in BENEFICIAL_MUTATIONS.items():
            if pos in muts and mt in muts[pos]:
                return True
        return False

    df['is_beneficial_lit'] = df.apply(check_beneficial, axis=1)
    return df


def get_designable_positions(sequence: str) -> set:
    """返回允许设计的位点集合"""
    all_positions = set(range(len(sequence)))
    forbidden = CHROMOPHORE_SITES | CHROMOPHORE_ENVIRONMENT
    return all_positions - forbidden


def main():
    parser = argparse.ArgumentParser(description='ESM-2 GFP Mutation Scanner')
    parser.add_argument('--output', default='results/esm2_mutation_scores.csv', 
                        help='Output CSV path')
    parser.add_argument('--model', default='esm2_t33_650M_UR50D',
                        help='ESM-2 model name')
    args = parser.parse_args()

    # 加载模型
    model, alphabet = load_esm2_model(args.model)

    # 获取可设计位点
    designable = get_designable_positions(SFGFP_WT)
    print(f"Designable positions: {len(designable)} / {len(SFGFP_WT)}")
    print(f"Forbidden positions: {len(CHROMOPHORE_SITES | CHROMOPHORE_ENVIRONMENT)}")

    # 扫描所有突变
    print("Scanning all mutations...")
    df = scan_all_mutations(model, alphabet, SFGFP_WT, 
                           exclude_positions=(CHROMOPHORE_SITES | CHROMOPHORE_ENVIRONMENT))

    # 标记文献突变
    df = mark_beneficial_mutations(df)

    # 排序：优先文献验证的，然后ESM2分数低的(负值大=有益)
    df = df.sort_values(['is_beneficial_lit', 'esm2_effect'], 
                        ascending=[False, True])

    # 保存
    df.to_csv(args.output, index=False)
    print(f"Results saved to {args.output}")
    print(f"Total mutations scanned: {len(df)}")

    # 打印Top 20最有益的
    print("\nTop 20 beneficial mutations (ESM2 effect < -1.0 or literature supported):")
    top = df[(df['esm2_effect'] < -1.0) | (df['is_beneficial_lit'] == True)].head(20)
    print(top[['position_1indexed', 'wt_aa', 'mt_aa', 'esm2_effect', 'is_beneficial_lit']].to_string(index=False))


if __name__ == "__main__":
    main()
