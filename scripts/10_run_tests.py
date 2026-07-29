#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Test Suite for GFP Design Pipeline
验证所有脚本和输出是否符合预期
"""

import unittest
import os
import pandas as pd
import subprocess
import sys

SFGFP_WT = (
    "MSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTLTYGVQCFSRYPDHMKRHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
)
AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


class TestSequenceAssembly(unittest.TestCase):
    """测试序列组装"""

    def test_submission_file_exists(self):
        """提交文件存在"""
        self.assertTrue(os.path.exists("results/submission_final.csv"))

    def test_csv_format(self):
        """CSV格式正确"""
        df = pd.read_csv("results/submission_final.csv")
        required = ['Team_Name', 'Seq_ID', 'Sequence']
        for col in required:
            self.assertIn(col, df.columns)

    def test_sequence_count(self):
        """序列数量正确"""
        df = pd.read_csv("results/submission_final.csv")
        self.assertLessEqual(len(df), 6)

    def test_sequence_length(self):
        """长度在范围内"""
        df = pd.read_csv("results/submission_final.csv")
        for seq in df['Sequence']:
            self.assertTrue(220 <= len(seq) <= 250)

    def test_start_with_m(self):
        """以M开头"""
        df = pd.read_csv("results/submission_final.csv")
        for seq in df['Sequence']:
            self.assertTrue(seq.startswith('M'))

    def test_standard_amino_acids(self):
        """仅标准氨基酸"""
        df = pd.read_csv("results/submission_final.csv")
        for seq in df['Sequence']:
            self.assertTrue(set(seq).issubset(AMINO_ACIDS))

    def test_chromophore_protected(self):
        """发色团保护"""
        df = pd.read_csv("results/submission_final.csv")
        for seq in df['Sequence']:
            if len(seq) > 66:
                self.assertEqual(seq[65], 'Y')
                self.assertEqual(seq[66], 'G')

    def test_no_duplicates(self):
        """无重复序列"""
        df = pd.read_csv("results/submission_final.csv")
        self.assertEqual(len(df['Sequence'].unique()), len(df))


class TestESM2Scan(unittest.TestCase):
    """测试ESM-2扫描"""

    def test_scores_file_exists(self):
        """得分文件存在"""
        self.assertTrue(os.path.exists("results/esm2_simulated_scores.csv"))

    def test_scores_format(self):
        """得分文件格式正确"""
        df = pd.read_csv("results/esm2_simulated_scores.csv")
        required = ['position_1idx', 'wt', 'mt', 'esm2_score']
        for col in required:
            self.assertIn(col, df.columns)

    def test_literature_mutations_present(self):
        """文献突变在数据中"""
        df = pd.read_csv("results/esm2_simulated_scores.csv")
        lit_muts = df[df['literature_supported'] == True]
        self.assertGreater(len(lit_muts), 0)


class TestDocumentation(unittest.TestCase):
    """测试文档完整性"""

    def test_readme_exists(self):
        """README存在"""
        self.assertTrue(os.path.exists("README.md"))

    def test_design_report_template_exists(self):
        """设计报告模板存在"""
        self.assertTrue(os.path.exists("docs/design_report_template.md"))

    def test_roadmap_exists(self):
        """路线图存在"""
        self.assertTrue(os.path.exists("ROADMAP.md"))

    def test_checklist_exists(self):
        """检查清单存在"""
        self.assertTrue(os.path.exists("SUBMISSION_CHECKLIST.md"))


class TestScripts(unittest.TestCase):
    """测试脚本可执行性"""

    def test_scripts_exist(self):
        """核心脚本存在"""
        scripts = [
            "scripts/01_esm2_mutation_scan_demo.py",
            "scripts/02_sequence_assembler_v2_1.py",
            "scripts/04_exclusion_checker.py",
            "scripts/06_final_submission_check.py",
        ]
        for script in scripts:
            self.assertTrue(os.path.exists(script), f"{script} not found")

    def test_scripts_executable(self):
        """脚本有执行权限"""
        import stat
        scripts = [
            "scripts/01_esm2_mutation_scan_demo.py",
            "scripts/02_sequence_assembler_v2_1.py",
        ]
        for script in scripts:
            if os.path.exists(script):
                mode = os.stat(script).st_mode
                self.assertTrue(mode & stat.S_IXUSR, f"{script} not executable")


def run_all_tests():
    """运行全部测试"""
    print("=" * 60)
    print("GFP Design Pipeline - Automated Test Suite")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestSequenceAssembly))
    suite.addTests(loader.loadTestsFromTestCase(TestESM2Scan))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentation))
    suite.addTests(loader.loadTestsFromTestCase(TestScripts))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("
" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("
✅ ALL TESTS PASSED")
        return 0
    else:
        print("
❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
