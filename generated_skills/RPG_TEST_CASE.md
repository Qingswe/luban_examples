# RPG 配置测试用例

本测试用例用于评估 Luban 配置表编辑 Skill 的完整性和准确性。

## 测试场景：完整 RPG 游戏配置

### 1. 角色成长系统

#### 1.1 角色基础属性表 (TbCharacter)
需求：
- 基础类型：id(int), name(text), class(enum)
- 数值属性：hp, mp, atk, def (int)
- 成长曲线：hp_growth, atk_growth (float)
- 分组：客户端/服务端

#### 1.2 技能树表 (TbSkillTree)
需求：
- 多态技能效果：DamageEffect, HealEffect, BuffEffect
- 前置技能引用：ref 验证器
- 解锁条件：level_required, prereq_skills(list)

#### 1.3 天赋系统表 (TbTalent)
需求：
- 多行列表：talent_nodes
- 被动效果：polymorphic PassiveEffect

### 2. 装备物品系统

#### 2.1 物品基础表 (TbItem)
需求：
- 枚举品质：Quality (COMMON, RARE, EPIC, LEGENDARY)
- 本地化：name(text), desc(text)
- 堆叠/价格：stack_limit, sell_price

#### 2.2 装备表 (TbEquipment)
需求：
- 多态词缀：Modifier (FlatModifier, PercentModifier)
- 装备套装：set_id (ref)
- 随机词缀池：affix_pool (list with index validator)

#### 2.3 合成配方表 (TbRecipe)
需求：
- 材料列表：materials (multi-row list)
- 产出物品：output_item (ref to TbItem)
- 消耗数量：count with range validator

### 3. 战斗数值系统

#### 3.1 技能效果表 (TbSkillEffect)
需求：
- 深度多态：Effect -> DamageEffect -> PhysicalDamage/MagicalDamage
- 伤害公式：base_damage, scaling_factor
- 元素类型：element (enum)

#### 3.2 Buff 表 (TbBuff)
需求：
- 持续时间：duration (float with range)
- 叠加规则：stack_limit, refresh_on_apply
- 效果类型：polymorphic BuffEffect

#### 3.3 元素克制表 (TbElementRelation)
需求：
- Map 类型：damage_multipliers (map,ElementType,float)
- 列限定格式：element columns

### 4. 任务剧情系统

#### 4.1 任务表 (TbQuest)
需求：
- 任务链：prereq_quest (ref with nullable)
- 本地化：title(text), desc(text)
- 字段变体：reward_gold variants (zh, en, jp)

#### 4.2 对话表 (TbDialog)
需求：
- 多行对话：dialog_lines (multi-row)
- 分支选项：choices (list of polymorphic)
- 本地化文本：speaker, content (text)

#### 4.3 成就表 (TbAchievement)
需求：
- 多态条件：AchievementCondition (KillCount, CollectItem, CompleteQuest)
- 进度追踪：target_value, current_progress
- 奖励引用：reward_items (list with ref)

## 评估标准

### 1. 语法正确性 (30%)
- Header 行格式正确（##var, ##type, ##group）
- 类型定义语法正确
- 验证器语法正确

### 2. 特性使用 (25%)
- 基础特性覆盖完整
- 高级特性使用正确
- 特性组合合理

### 3. 数据完整性 (20%)
- 引用关系正确
- 数据一致性
- 无遗漏字段

### 4. 配置完整性 (15%)
- RPG 系统覆盖完整
- 游戏逻辑合理
- 可扩展性良好

### 5. 最佳实践 (10%)
- 命名规范
- 模块组织
- 文档清晰度

## 特性检查清单

### 基础特性
- [ ] 基础数据类型 (int, string, bool, float, datetime)
- [ ] 容器类型 (list, set, map, array)
- [ ] 枚举类型 (enum with alias)
- [ ] Bean 类型 (nested structures)
- [ ] 表定义 (map/list/singleton modes)
- [ ] 分组机制 (##group with c/s/e)
- [ ] 可空类型 (int?, bean?)

### 高级特性
- [ ] 多态类型 (inheritance, $type column)
- [ ] 字段变体 (@variant)
- [ ] 数据校验器 (ref, path, range, size, set, index)
- [ ] 本地化 (text type, static localization)
- [ ] 层级参数机制
- [ ] 数据 tag (##, dev, unchecked)
- [ ] 紧凑格式 (sep, json, lua)
- [ ] 列限定格式 ($type, $value, $key)
- [ ] 多行结构列表 (*field)
- [ ] 多级标题头
