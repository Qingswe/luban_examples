# Luban Skill 训练工作流

## 概述

本工作流用于训练、测试和迭代 Luban 配置表编辑 AI Skill。

## 阶段 1: 训练数据准备

### 核心训练文档

从 `datable_docs/zh/manual` 目录获取：

| 文档 | 重要性 | 内容 |
|------|--------|------|
| excel格式（初级）.md | 必需 | 标题头行、基础数据类型、分组 |
| excel格式（高级）.md | 必需 | 多态、多行列表、列限定格式 |
| 类型系统.md | 必需 | 完整类型系统定义 |
| 多态类型.md | 必需 | 多态继承、$type 列 |
| 数据校验器.md | 必需 | ref、range、path 等验证器 |
| 本地化.md | 必需 | text 类型、静态本地化 |
| 配置定义.md | 必需 | 表、枚举、Bean 定义 |
| 最佳实践.md | 推荐 | 命名规范、模块组织 |

### 补充训练文档

从 `datable_docs/zh/beginner` 目录获取：

| 文档 | 重要性 | 内容 |
|------|--------|------|
| 自动导入table.md | **关键** | `#` 前缀自动导入规则 |
| 快速上手.md | 必需 | 基础工作流、__tables__.xlsx |
| 使用容器类型.md | 必需 | list/set/map 填写方式 |
| 使用多态类型.md | 必需 | 多态数据填写示例 |
| 使用数据校验器.md | 必需 | ref 引用实例 |
| 使用列限定与紧凑格式.md | 推荐 | 列限定、sep、json 格式 |

## 阶段 2: Skill 训练与迭代

### 执行方式

使用 `.claude/agents/luban-skill-trainer.md` agent 执行训练：

```bash
# 训练单个通用 Skill
Task(subagent_type="luban-skill-trainer", prompt="Train luban skill...")
```

### 训练流程

`luban-skill-trainer` agent 负责完整的学习、实践和总结流程：

1. **理解阶段**：阅读 Luban 文档，建立基础认知
2. **测试执行阶段**：直接运行测试用例，在实践中学习 Luban 用法
3. **总结与生成阶段**：总结测试中学到的用法，使用 skill-creator 生成 Skill

### 测试任务

测试任务位于 `skill_tests/TEST_TASKS.md`，包含 4 个模块、12 个任务：

| 模块 | 任务数 | 权重 | 核心测试点 |
|------|--------|------|------------|
| 角色成长系统 | 3 | 25% | 枚举、分组、多态效果、多行列表 |
| 装备物品系统 | 3 | 25% | 品质枚举、多态词缀、引用验证 |
| 战斗数值系统 | 3 | 25% | 深度多态、map类型、列限定 |
| 任务剧情系统 | 3 | 25% | 本地化、字段变体、多态条件 |

### 测试环境

```
skill_tests/
└── replica_test/      # 测试目录（MiniTemplate 副本）
```

### 验证方式

每个测试必须通过实际 Luban 验证：

```bash
cd skill_tests/replica_test
"E:\Learn\luban_examples\Tools\Luban\Luban.exe" -t all -f --conf luban.conf
```

### 学习策略

1. **基础理解**：快速阅读文档，建立基础认知框架
2. **实践学习**：直接运行测试用例，遇到问题时查阅文档
3. **记录总结**：记录每个任务的实现方法和学到的用法
4. **强制完成**：**必须完成所有 12 个测试任务**后才能进入生成阶段
5. **生成 Skill**：基于测试中的实际用法，总结并生成完整的 Skill
6. **质量保证**：确保 Skill 覆盖所有测试点，包含常见错误防范

### 强制完成机制

**在进入总结与生成阶段之前，必须：**

1. 完成所有 12 个测试任务：
   - 模块 1：Task 1.1, 1.2, 1.3
   - 模块 2：Task 2.1, 2.2, 2.3
   - 模块 3：Task 3.1, 3.2, 3.3
   - 模块 4：Task 4.1, 4.2, 4.3

2. 每个任务都通过 Luban 验证

3. 在测试报告中明确列出所有任务的完成状态

**如果未完成所有任务，禁止使用 skill-creator 生成 Skill！**

### 上下文限制反馈

如果 subagent 遇到以下情况，必须立即反馈：

- 文件过大无法完整读取
- 任务描述不完整
- 需要更多文档信息但无法加载
- 测试环境访问问题

反馈格式：使用 `⚠️ 上下文限制：` 前缀，说明问题并提供建议。

### 输出结构

```
generated_skills/
└── luban-skill/
    ├── SKILL.md          # 主技能文件
    ├── references/        # 可选：参考文档（如过长内容）
    │   └── examples.md
    └── assets/            # 可选：示例文件
        └── examples/
```

**注意**：如果某些内容（如详细示例、参考文档）过长不适合放在 SKILL.md 中，可以放在同级目录的 `references/` 或 `assets/` 目录中，在 SKILL.md 中引用。

### Skill 必须包含的关键规则

**自动导入规则（关键）**：

```markdown
## 文件命名与表注册

| 文件类型 | 命名规则 | __tables__.xlsx |
|----------|----------|-----------------|
| 自动导入 | `#TableName.xlsx` | **不填** |
| 手动注册 | `tablename.xlsx` | **必须填** |

示例：
- `#Item.xlsx` → 自动生成 TbItem，不需要注册
- `reward.xlsx` → 需要在 __tables__.xlsx 添加 TbReward
```

## 阶段 3: 评估与交付

### 评分标准

| 维度 | 权重 | 评估内容 |
|------|------|----------|
| 语法正确性 | 40% | Luban 验证通过 |
| 完整性 | 30% | 覆盖所有需求点 |
| 最佳实践 | 20% | 命名规范、结构合理 |
| 清晰度 | 10% | 指导说明清晰 |

### 加权总分

```
总分 = 模块1 × 0.25 + 模块2 × 0.25 + 模块3 × 0.25 + 模块4 × 0.25
```

### 必需交付

- [ ] 1 个通用 Skill（SKILL.md）
- [ ] 测试报告（含 Luban 验证日志，由训练 agent 生成）
- [ ] 可选：引用文件（如过长内容放在同级目录）

### 目录结构

```
luban_examples/
├── generated_skills/
│   └── luban-skill/
│       ├── SKILL.md
│       ├── references/        # 可选：过长内容
│       └── assets/            # 可选：示例文件
├── skill_tests/
│   ├── TEST_TASKS.md
│   └── replica_test/          # 测试目录
└── .claude/agents/
    └── luban-skill-trainer.md
```

## 执行命令

```bash
# 启动完整训练流程
@Skill-Trainer.md 执行训练

# 用户确认参数后：
# 1. 启动训练 agent
# 2. agent 完成：理解 → 测试执行（实践学习）→ 总结生成
# 3. 输出最终 Skill 到 generated_skills/luban-skill/
```
