# GFP竞赛操作路线图

## 阶段一：环境搭建（第1天）

```bash
# 1. 克隆/下载本仓库
cd gfp_design_pipeline

# 2. 创建conda环境
conda create -n gfp python=3.9
conda activate gfp

# 3. 安装基础依赖
pip install -r requirements.txt

# 4. 安装ESM-2（需要GPU，可选）
pip install fair-esm

# 5. 验证安装
python -c "import torch; import pandas; import esm; print('OK')"
```

## 阶段二：基线建立（第1-2天）

### 2.1 获取官方资料
- 从报名系统下载：GFP序列、结构、Exclusion_List.csv
- 将Exclusion_List.csv放入 `data/` 目录

### 2.2 结构分析
```bash
# 下载sfGFP结构
python scripts/03_structure_analysis.py

# 用PyMOL可视化（手动执行PyMOL命令）
# 确认禁区范围，标记我们的突变位点
```

## 阶段三：计算设计（第3-7天，核心）

### 3.1 ESM-2突变扫描
```bash
# 方式A: 快速演示（无需GPU，基于启发式模拟）
python scripts/01_esm2_mutation_scan_demo.py

# 方式B: 真实ESM-2扫描（需要GPU，更准）
python scripts/01_esm2_mutation_scan.py --output results/esm2_real_scores.csv
```

**关键决策**: 对比演示结果与真实ESM-2结果，调整突变优先级。

### 3.2 Rosetta ddG计算（如有学术许可）
```bash
# 对Top 20突变进行能量计算
# 筛选标准: ΔΔG < -0.5 kcal/mol
```

### 3.3 ProteinMPNN表面优化（可选）
```bash
# 需先克隆ProteinMPNN仓库
python scripts/05_proteinmpnn_design.py
# 运行生成的命令
```

### 3.4 MD预筛选（如有GPU资源）
```bash
# 对最有希望的10个变体进行50ns升温模拟
# 使用scripts/md_simulation_params.ini参数
```

## 阶段四：序列确定（第8-10天）

### 4.1 运行序列组装
```bash
python scripts/02_sequence_assembler_v2_1.py
```

### 4.2 排除列表检查
```bash
python scripts/04_exclusion_checker.py --input results/submission_final.csv
```

### 4.3 迭代优化
参考 `docs/iteration_guide.md` 进行2-3轮优化：
1. 若某序列Rosetta/MD表现差，从备选池替换
2. 若发现新的强有益突变，叠加到保守序列上
3. 保持风险梯度（2保守 + 2中等 + 2激进）

## 阶段五：文档与提交（第11-14天）

### 5.1 撰写设计思路文档
```bash
# 基于模板填写
cp docs/design_report_template.md docs/design_report.md
# 用Typora/Markdown转PDF
```

**必须包含**:
- 算法管线图
- 6条序列的逐条设计逻辑
- LLM Agent使用说明（如适用）
- 可复现性声明

### 5.2 开源仓库准备
```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial design pipeline"

# 创建GitHub仓库并推送
gh repo create YourTeamName/gfp-thermo-design --public
git push origin main
```

### 5.3 最终提交文件
确认提交包包含：
- [ ] `submission_final.csv`（6条序列）
- [ ] `design_report.pdf`
- [ ] GitHub仓库链接

---

## 关键决策点FAQ

### Q1: 为什么当前6条序列主要用文献突变，而非纯ESM-2预测？

**A**: 蛋白质工程的第一原则是**"站在巨人肩膀上"**。ESM-2学习的是进化统计规律，而文献突变已经过实验验证：
- E222Q在多篇文献中被证实增强热稳定性
- N149K、Q183R等有明确的机制解释
- 纯计算预测的新突变（如位点167I→D）虽然ESM2分数低，但缺乏实验验证，风险未知

**策略**: 以文献突变为主体（80%），计算预测为辅助（20%）。

### Q2: 如果ESM-2真实扫描结果与演示版差异很大怎么办？

**A**: 
1. 若文献突变ESM2分数反而高（有害），**相信文献**（实验数据 > 计算预测）
2. 若发现新的强有益突变（ESM2分数低且无文献），**小步验证**：
   - 先添加到Seq-1（保守序列）中测试
   - 若MD/Rosetta支持，再推广到其他序列

### Q3: 6条序列的风险梯度是否合理？

**A**: 当前分布：
- **低风险**（Seq-1, Seq-2）: 2条，保底
- **中风险**（Seq-3, Seq-5）: 2条，主力
- **高风险**（Seq-4, Seq-6）: 2条，冲奖

**建议**: 若时间允许，将Seq-6改为中风险（移除L195A，保留其他），因为：
- 比赛以Top-1成绩排名，一条高风险序列失败不影响其他
- 但若有独立的最佳热稳定奖，高风险序列值得一搏

### Q4: 是否需要做实验验证？

**A**: 竞赛由大设施统一合成表达，**参赛队伍不需要自己做实验**。但如果有条件：
- 可用大肠杆菌表达1-2条序列验证亮度
- 可用PCR仪做简易热稳定性测试（37°C→95°C梯度）
- 这些预实验数据可写入设计文档，增加说服力

### Q5: 如果Exclusion_List包含我们的序列怎么办？

**A**: 
1. 运行 `04_exclusion_checker.py` 自动检测
2. 若冲突，微调突变：
   - E222Q → E222G（同样稳定，序列不同）
   - N149K → N149R（Arg替代Lys）
   - Q183R → Q183K（Lys替代Arg）
3. 重新校验后再次比对

---

## 时间规划表（假设4周准备期）

| 周次 | 任务 | 产出 |
|------|------|------|
| **Week 1** | 环境搭建、结构分析、ESM-2扫描 | 候选突变池、禁区图谱 |
| **Week 2** | Rosetta计算、MD预筛选、组合优化 | Top 12突变组合 |
| **Week 3** | 确定6条序列、迭代优化、排除列表检查 | submission_final.csv |
| **Week 4** | 撰写文档、整理代码、开源仓库、提交 | 完整提交包 |

---

## 紧急备案（如果时间不足）

若只剩1周：
1. **跳过** Rosetta和MD，直接用文献突变
2. 使用本仓库现成的 `02_sequence_assembler_v2_1.py` 生成6条序列
3. 手动检查排除列表
4. 基于 `design_report_template.md` 快速填写文档
5. 提交

**最低限度提交包**：
- 6条序列CSV（格式正确）
- 简版设计文档（说明母序列和突变依据）
- GitHub仓库（包含本代码）
