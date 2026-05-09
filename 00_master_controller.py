#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Pipeline Controller
一键生成GFP竞赛全部提交材料
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)


def run_step(step_name: str, script: str, args: list = None):
    """执行单步并检查结果"""
    print(f"\n{'='*60}")
    print(f"STEP: {step_name}")
    print(f"{'='*60}")

    cmd = [sys.executable, script]
    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("WARN:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Step failed with code {e.returncode}")
        print(e.stdout)
        print(e.stderr)
        return False


def generate_all_materials(team_name: str = "YourTeamName"):
    """生成全部竞赛材料"""

    print("=" * 60)
    print("GFP Competition - Full Material Generation")
    print(f"Team: {team_name}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    steps = [
        ("ESM-2 Mutation Scan (Demo)", "scripts/01_esm2_mutation_scan_demo.py", []),
        ("Sequence Assembly", "scripts/02_sequence_assembler_v2_1.py", []),
        ("Exclusion List Check", "scripts/04_exclusion_checker.py", [
            "--input", "results/submission_final.csv"
        ]),
        ("Final Submission Check", "scripts/06_final_submission_check.py", [
            "--input", "results/submission_final.csv",
            "--output", "results/final_check_report.txt"
        ]),
    ]

    results = {}
    for name, script, args in steps:
        success = run_step(name, script, args)
        results[name] = "✅ PASS" if success else "❌ FAIL"

    # 汇总
    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    for name, status in results.items():
        print(f"  {status} {name}")

    all_pass = all(s == "✅ PASS" for s in results.values())

    if all_pass:
        print("\n✅ ALL MATERIALS GENERATED SUCCESSFULLY")
        print("\nGenerated files:")
        print("  📄 results/submission_final.csv")
        print("  📄 results/esm2_simulated_scores.csv")
        print("  📄 results/exclusion_check_report.csv")
        print("  📄 results/final_check_report.txt")
        print("  📄 results/sequences_for_exclusion_check.txt")
        print("\nNext steps:")
        print("  1. Review results/submission_final.csv")
        print("  2. Convert docs/design_report_template.md → PDF")
        print("  3. Push to GitHub")
        print("  4. Submit!")
    else:
        print("\n❌ SOME STEPS FAILED - Check logs above")

    return all_pass


def package_submission(team_name: str, output_zip: str = None):
    """打包提交材料"""
    if output_zip is None:
        output_zip = f"{team_name}_submission.zip"

    print(f"\n{'='*60}")
    print("PACKAGING SUBMISSION")
    print(f"{'='*60}")

    # 创建临时目录
    pkg_dir = f"tmp_{team_name}_pkg"
    os.makedirs(pkg_dir, exist_ok=True)

    # 复制必要文件
    files_to_copy = [
        ("results/submission_final.csv", "submission.csv"),
        ("docs/design_report_template.md", "design_report.md"),
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE"),
    ]

    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(pkg_dir, dst))
            print(f"  ✅ {src} -> {dst}")
        else:
            print(f"  ⚠️  {src} not found")

    # 创建GitHub链接文件
    with open(os.path.join(pkg_dir, "GITHUB_REPO.txt"), 'w') as f:
        f.write(f"https://github.com/YourOrg/{team_name}-gfp-design\n")

    # 打包
    shutil.make_archive(output_zip.replace('.zip', ''), 'zip', pkg_dir)

    # 清理
    shutil.rmtree(pkg_dir)

    print(f"\n📦 Package created: {output_zip}")
    print(f"   Size: {os.path.getsize(output_zip)} bytes")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Master pipeline controller')
    parser.add_argument('--team', default='YourTeamName', help='Team name')
    parser.add_argument('--package', action='store_true', help='Create submission package')
    parser.add_argument('--zip', default=None, help='Output zip path')
    args = parser.parse_args()

    success = generate_all_materials(args.team)

    if success and args.package:
        package_submission(args.team, args.zip)


if __name__ == "__main__":
    main()
