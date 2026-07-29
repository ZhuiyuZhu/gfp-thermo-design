# GFP设计竞赛项目导航

## 📖 快速开始

| 我想... | 查看文件 |
|---------|---------|
| 了解项目概况 | [README.md](README.md) |
| 快速查看关键信息 | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 了解竞赛规则 | [docs/rules_interpretation.md](docs/rules_interpretation.md) |
| 查看操作路线图 | [ROADMAP.md](ROADMAP.md) |
| 提交前检查 | [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) |
| 常见问题解答 | [FAQ.md](FAQ.md) |

## 🧬 序列设计

| 我想... | 查看文件 |
|---------|---------|
| 查看6条设计序列 | [results/submission_final.csv](results/submission_final.csv) |
| 查看序列详细对比 | [docs/sequence_comparison.md](docs/sequence_comparison.md) |
| 查看突变位点结构分析 | [docs/structure_position_analysis.md](docs/structure_position_analysis.md) |
| 查看突变效应详情 | [results/mutation_effect_details.csv](results/mutation_effect_details.csv) |
| 查看备选序列池 | [docs/alternative_pool.md](docs/alternative_pool.md) |

## 💻 代码与计算

| 我想... | 运行脚本 |
|---------|---------|
| 一键生成全部材料 | `python scripts/00_master_controller.py` |
| ESM-2突变扫描 | `python scripts/01_esm2_mutation_scan_demo.py` |
| 序列组装 | `python scripts/02_sequence_assembler_v2_1.py` |
| 结构分析 | `python scripts/03_structure_analysis.py` |
| 排除列表检查 | `python scripts/04_exclusion_checker.py` |
| ProteinMPNN设计 | `python scripts/05_proteinmpnn_design.py` |
| 最终校验 | `python scripts/06_final_submission_check.py` |
| AlphaFold2预测 | `python scripts/07_alphafold_prediction.py` |
| Rosetta ddG计算 | `python scripts/08_rosetta_ddg.py` |
| PDF生成 | `python scripts/09_generate_pdf.py` |
| 自动化测试 | `python scripts/10_run_tests.py` |
| 得分模拟 | `python scripts/11_scoring_simulator.py` |

## 📊 可视化图表

| 图表 | 文件 | 用途 |
|------|------|------|
| ESM-2得分分布 | [fig1_esm2_distribution.png](results/figures/fig1_esm2_distribution.png) | 展示突变扫描结果 |
| 突变位点分布 | [fig2_mutation_distribution.png](results/figures/fig2_mutation_distribution.png) | 展示序列设计位置 |
| 风险-收益矩阵 | [fig3_risk_benefit_matrix.png](results/figures/fig3_risk_benefit_matrix.png) | 展示6条序列策略 |
| 文献vs计算预测 | [fig4_lit_vs_comp.png](results/figures/fig4_lit_vs_comp.png) | 展示预测依据 |
| 序列比对 | [fig5_sequence_alignment.png](results/figures/fig5_sequence_alignment.png) | 展示突变细节 |
| 时间规划 | [fig6_timeline_gantt.png](results/figures/fig6_timeline_gantt.png) | 展示项目计划 |
| 得分模拟 | [fig7_scoring_scenarios.png](results/figures/fig7_scoring_scenarios.png) | 展示得分机制 |

## 📝 文档撰写

| 我想... | 查看文件 |
|---------|---------|
| 撰写设计思路文档 | [docs/design_report_template.md](docs/design_report_template.md) |
| 了解迭代优化策略 | [docs/iteration_guide.md](docs/iteration_guide.md) |
| 了解DNA反向翻译 | [docs/dna_reverse_translation.md](docs/dna_reverse_translation.md) |
| 查看文献引用 | [docs/references.md](docs/references.md) |
| 准备答辩幻灯片 | [docs/presentation_outline.md](docs/presentation_outline.md) |

## 🔧 环境配置

| 我想... | 查看文件 |
|---------|---------|
| 安装依赖 | [requirements.txt](requirements.txt) |
| Docker部署 | [Dockerfile](Dockerfile) |
| 一键运行 | [run_pipeline.sh](run_pipeline.sh) |
| Jupyter演示 | [notebooks/GFP_Design_Demo.ipynb](notebooks/GFP_Design_Demo.ipynb) |
| CI配置 | [.github/workflows/ci.yml](.github/workflows/ci.yml) |

## 📦 提交材料

| 材料 | 文件 | 状态 |
|------|------|------|
| 序列文件 | [results/submission_final.csv](results/submission_final.csv) | ✅ 已生成 |
| 排除检查 | [results/sequences_for_exclusion_check.txt](results/sequences_for_exclusion_check.txt) | ✅ 已生成 |
| ESM-2数据 | [results/esm2_simulated_scores.csv](results/esm2_simulated_scores.csv) | ✅ 已生成 |
| 结构分析 | [results/mutation_structure_analysis.csv](results/mutation_structure_analysis.csv) | ✅ 已生成 |
| 效应详情 | [results/mutation_effect_details.csv](results/mutation_effect_details.csv) | ✅ 已生成 |
| 汇总表 | [results/submission_summary.csv](results/submission_summary.csv) | ✅ 已生成 |

## 🎯 关键决策速查

| 问题 | 答案 |
|------|------|
| 母序列 | sfGFP (238 aa) |
| 保守保底 | Seq-1 (E222Q) |
| 冲金奖 | Seq-4 (E222Q+N149K+Q183R+M218V) |
| 冲亮度奖 | Seq-5 (表面电荷优化) |
| 冲稳定奖 | Seq-6 (loop+C端工程) |
| 绝对禁区 | Y66(pos65), G67(pos66) |
| 长度限制 | 220-250 aa |
| 淘汰线 | Finitial < 0.3×WT |

---

**最后更新**: 2026-05-03  
**版本**: v1.0  
**状态**:  ready for submission
