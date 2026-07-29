# 贡献指南

## 团队分工建议

### 角色1: 计算设计师
**职责**:
- ESM-2/Rosetta计算
- 突变筛选和组合优化
- MD模拟设置和分析

**所需技能**:
- Python编程
- PyTorch/ESM-2
- 分子动力学基础

### 角色2: 生物分析师
**职责**:
- 文献调研
- 结构分析（PyMOL）
- 突变机制解释

**所需技能**:
- 蛋白质结构知识
- PyMOL操作
- 文献检索

### 角色3: 工程师
**职责**:
- 代码整理和文档
- GitHub仓库维护
- CI/CD配置

**所需技能**:
- Git/GitHub
- 软件工程
- Markdown/LaTeX

### 角色4: 项目经理
**职责**:
- 时间规划
- 提交材料整合
- 沟通协调

**所需技能**:
- 项目管理
- 学术写作
- 演示准备

## Git工作流

```bash
# 1. 克隆仓库
git clone https://github.com/YourTeamName/gfp-thermo-design.git

# 2. 创建功能分支
git checkout -b feature/esm2-scan

# 3. 开发和提交
git add .
git commit -m "Add ESM-2 mutation scanning"

# 4. 推送到远程
git push origin feature/esm2-scan

# 5. 创建Pull Request
# 在GitHub上合并到main分支

# 6. 更新本地
git checkout main
git pull origin main
```

## 代码规范

### Python代码风格
- 遵循PEP 8
- 使用类型提示
- 编写docstring

### 提交信息规范
```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
refactor: 重构代码
test: 添加测试
chore: 维护性工作
```

### 文件命名
- 脚本: `XX_descriptive_name.py`
- 文档: `descriptive_name.md`
- 结果: `descriptive_name.csv`

## 审查清单

### 代码审查
- [ ] 代码可运行
- [ ] 有适当注释
- [ ] 错误处理完善
- [ ] 输出格式正确

### 文档审查
- [ ] 无拼写错误
- [ ] 图表清晰
- [ ] 引用完整
- [ ] 逻辑连贯

### 序列审查
- [ ] 长度正确
- [ ] 字符规范
- [ ] 发色团保护
- [ ] 排除列表检查

## 沟通渠道

| 目的 | 工具 |
|------|------|
| 日常沟通 | 微信/Slack |
| 代码协作 | GitHub |
| 文档协作 | Google Docs/Notion |
| 文件共享 | Google Drive |
| 会议 | Zoom/腾讯会议 |

## 时间规划

| 周次 | 计算设计师 | 生物分析师 | 工程师 | 项目经理 |
|------|----------|----------|--------|---------|
| 1 | ESM-2扫描 | 文献调研 | 环境搭建 | 团队组建 |
| 2 | Rosetta/MD | 结构分析 | 代码框架 | 进度跟踪 |
| 3 | 组合优化 | 机制解释 | 文档撰写 | 材料整合 |
| 4 | 最终验证 | 结构验证 | 仓库整理 | 提交 |
