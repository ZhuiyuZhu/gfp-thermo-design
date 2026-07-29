#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyMOL Automation Script for GFP Analysis
自动生成结构分析图片和测量数据
"""

# 保存为 pymol_gfp_analysis.pml，在PyMOL中运行：
# run pymol_gfp_analysis.pml

# 或者直接在PyMOL命令行中逐行执行

"""
========================================
PyMOL GFP Structure Analysis Commands
========================================

# 1. 加载结构
fetch 2B3P
remove solvent
remove hydrogens

# 2. 设置显示风格
as cartoon
color gray, all

# 3. 标记发色团
select chromophore, resi 66+67
show sticks, chromophore
color atomic, chromophore
set stick_radius, 0.3, chromophore

# 4. 标记发色团环境（8Å）
select chrom_env, chromophore expand 8.0
show surface, chrom_env
color red, chrom_env
set transparency, 0.7, chrom_env

# 5. 标记我们的突变位点
select our_mutations, resi 149+183+218+14+47+173+195+231
show sticks, our_mutations
color blue, our_mutations
set stick_radius, 0.25, our_mutations

# 6. 标记E222Q（所有序列共有）
select e222q, resi 222
color green, e222q
show sticks, e222q
set stick_radius, 0.35, e222q

# 7. 测量关键距离
# 发色团到E222的距离
distance chrom_to_e222, chromophore, resi 222
# 发色团到Q183的距离
distance chrom_to_q183, chromophore, resi 183
# N149到最近酸性残基的距离（盐桥）
distance n149_bridge, resi 149 and name NZ, resi 145 and name OE1

# 8. 设置视角
orient chromophore
zoom chromophore, 20

# 9. 添加标签
label chromophore and name CA, "Chromophore"
label resi 222 and name CA, "E222Q"
label resi 149 and name CA, "N149K"
label resi 183 and name CA, "Q183R"

# 10. 保存图片
set ray_trace_mode, 1
set ray_shadows, 0
bg_color white
ray 2400, 2400
png results/figures/pymol_gfp_analysis.png, dpi=300

# 11. 保存会话
save results/figures/pymol_gfp_analysis.pse

========================================
关键测量命令
========================================

# 测量溶剂可及性（需要安装APBS或PyMOL插件）
get_area resi 149
get_area resi 183
get_area resi 218

# 测量二级结构
dssp

# 测量B-factor（结构柔性）
# 查看特定残基的B-factor
iterate resi 195, print(name, b)

# 测量电荷分布
# 需要APBS插件
# apbs_draw_charges

========================================
6条序列分别可视化
========================================

# 为每条序列创建单独的图片
# 注意：这里使用WT结构作为近似，实际应使用AlphaFold2预测的结构

# Seq-1: E222Q
select seq1_mut, resi 222
color green, seq1_mut
show sticks, seq1_mut
ray 1600, 1200
png results/figures/seq1_e222q.png, dpi=300

# Seq-2: E222Q + N149K
select seq2_mut, resi 149+222
color blue, seq2_mut
show sticks, seq2_mut
ray 1600, 1200
png results/figures/seq2_mutations.png, dpi=300

# Seq-3: + Q183R
select seq3_mut, resi 149+183+222
color magenta, seq3_mut
show sticks, seq3_mut
ray 1600, 1200
png results/figures/seq3_mutations.png, dpi=300

# Seq-4: + M218V
select seq4_mut, resi 149+183+218+222
color orange, seq4_mut
show sticks, seq4_mut
ray 1600, 1200
png results/figures/seq4_mutations.png, dpi=300

# Seq-5: Surface mutations
color cyan, resi 14+47+173
color green, resi 222
show sticks, resi 14+47+173+222
ray 1600, 1200
png results/figures/seq5_surface_mutations.png, dpi=300

# Seq-6: Loop + C-term
color yellow, resi 195+231
color magenta, resi 149+183
color green, resi 222
show sticks, resi 149+183+195+222+231
ray 1600, 1200
png results/figures/seq6_exploratory.png, dpi=300
