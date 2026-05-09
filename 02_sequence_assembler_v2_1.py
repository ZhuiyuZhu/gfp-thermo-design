#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GFP Variant Assembler & Validator (v2.1 - Fixed)
"""

import pandas as pd
import os

SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)
AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def apply_mutations(sequence, mutations):
    seq_list = list(sequence)
    for pos, new_aa in mutations.items():
        wt_aa = sequence[pos]
        if new_aa != wt_aa:
            print(f"  pos {pos+1}: {wt_aa} -> {new_aa}")
        seq_list[pos] = new_aa
    return "".join(seq_list)


def validate_sequence(seq, wt_seq=SFGFP_WT, exclusion_list=None):
    if exclusion_list is None:
        exclusion_list = set()

    errors = []

    if not (220 <= len(seq) <= 250):
        errors.append(f"Length {len(seq)} not in [220,250]")

    if not seq.startswith('M'):
        errors.append("Must start with M")

    invalid = set(seq) - AMINO_ACIDS
    if invalid:
        errors.append(f"Invalid chars: {invalid}")

    if '*' in seq or '.' in seq or '-' in seq:
        errors.append("Forbidden symbols")

    if seq in exclusion_list:
        errors.append("In exclusion list")

    if seq[65] != 'Y' or seq[66] != 'G':
        errors.append(f"Chromophore damaged: pos66={seq[65]}, pos67={seq[66]}")

    is_valid = len(errors) == 0
    msg = "Valid" if is_valid else " | ".join(errors)
    return is_valid, msg


class GFPDesigner:
    def __init__(self, wt_seq=SFGFP_WT):
        self.wt = wt_seq

    def design_seq1(self):
        muts = {221: 'Q'}
        desc = "Conservative: E222Q only"
        return apply_mutations(self.wt, muts), muts, desc

    def design_seq2(self):
        muts = {221: 'Q', 148: 'K'}
        desc = "Thermo dual: E222Q + N149K"
        return apply_mutations(self.wt, muts), muts, desc

    def design_seq3(self):
        muts = {221: 'Q', 148: 'K', 182: 'R'}
        desc = "Thermo triple: +Q183R"
        return apply_mutations(self.wt, muts), muts, desc

    def design_seq4(self):
        muts = {221: 'Q', 148: 'K', 182: 'R', 217: 'V'}
        desc = "Thermo max: +M218V"
        return apply_mutations(self.wt, muts), muts, desc

    def design_seq5(self):
        muts = {221: 'Q', 13: 'K', 46: 'K', 172: 'K'}
        desc = "CFPS surface: E14K+E47K+E173K+E222Q"
        return apply_mutations(self.wt, muts), muts, desc

    def design_seq6(self):
        muts = {221: 'Q', 148: 'K', 182: 'R', 194: 'A', 230: 'V'}
        desc = "Exploratory: loop+C-term"
        return apply_mutations(self.wt, muts), muts, desc

    def generate_all(self):
        methods = [self.design_seq1, self.design_seq2, self.design_seq3,
                   self.design_seq4, self.design_seq5, self.design_seq6]
        designs = []
        for i, method in enumerate(methods, 1):
            seq, muts, desc = method()
            designs.append((str(i), seq, muts, desc))
        return designs


def main():
    designer = GFPDesigner()
    designs = designer.generate_all()

    print("=" * 70)
    print("GFP Variant Design Results")
    print("=" * 70)

    valid_designs = []
    for seq_id, seq, muts, desc in designs:
        valid, msg = validate_sequence(seq)
        status = "✓ PASS" if valid else "✗ FAIL"
        mut_str = ";".join([f"{k+1}{SFGFP_WT[k]}{v}" for k, v in sorted(muts.items())])
        print(f"\nSeq-{seq_id}: {status} | {msg}")
        print(f"  Strategy: {desc}")
        print(f"  Mutations: {mut_str}")
        print(f"  Full Seq: {seq}")
        if valid:
            valid_designs.append((seq_id, seq, muts, desc))

    if valid_designs:
        os.makedirs("results", exist_ok=True)
        rows = []
        for seq_id, seq, muts, desc in valid_designs:
            mut_str = ";".join([f"{k+1}{SFGFP_WT[k]}{v}" for k, v in sorted(muts.items())])
            rows.append({
                'Team_Name': 'YourTeamName',
                'Seq_ID': seq_id,
                'Sequence': seq,
                'Mutations': mut_str,
                'Strategy': desc,
                'Length': len(seq)
            })
        df = pd.DataFrame(rows)
        df.to_csv("results/submission_final.csv", index=False)

        with open("results/sequences_for_exclusion_check.txt", "w") as f:
            for _, seq, _, _ in valid_designs:
                f.write(seq + "\n")

        print("\n" + "=" * 70)
        print("SUBMISSION SUMMARY")
        print("=" * 70)
        print(df.to_string(index=False))
        print("\nFiles saved to results/")

if __name__ == "__main__":
    main()
