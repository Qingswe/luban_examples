# Luban Skill 完整测试任务集

基于 MiniTemplate 设计的渐进式测试任务，完整覆盖 RPG 游戏配置场景。

## 测试概览

| 模块 | 任务数 | 权重 | 核心测试点 |
|------|--------|------|------------|
| 角色成长系统 | 3 | 25% | 枚举、分组、多态效果、多行列表 |
| 装备物品系统 | 3 | 25% | 品质枚举、多态词缀、引用验证 |
| 战斗数值系统 | 3 | 25% | 深度多态、map类型、列限定 |
| 任务剧情系统 | 3 | 25% | 本地化、字段变体、多态条件 |

---

## 模块 1：角色成长系统 (25%)

### Task 1.1：角色基础属性表 (TbCharacter)

**难度**：初级
**权重**：8%

**需求**：
1. 定义 CharacterClass 枚举：
   - WARRIOR(战士)=1, MAGE(法师)=2, ARCHER(弓手)=3, PRIEST(牧师)=4
2. 创建 Character bean：
   - id (int), name (text), class (CharacterClass)
   - hp, mp, atk, def (int) - 分组 c,s
   - hp_growth, atk_growth (float) - 仅服务端 s
3. 创建 `#Character.xlsx` 数据表（自动导入）
4. 填写至少 4 条角色数据

**预期输出**：
```
__enums__.xlsx: 添加 CharacterClass
#Character.xlsx: 新建，包含标题头和数据
```

**评估点**：
- [ ] 枚举定义正确，含别名
- [ ] 分组机制正确（c/s/c,s）
- [ ] 自动导入规则正确（不填 __tables__.xlsx）
- [ ] float 类型成长曲线

---

### Task 1.2：技能树表 (TbSkillTree)

**难度**：中级
**权重**：8%

**需求**：
1. 定义多态 SkillEffect 层次（在 __beans__.xlsx）：
   ```
   SkillEffect (基类)
   ├── DamageEffect: damage(int), element(string)
   ├── HealEffect: heal_amount(int), heal_percent(float)
   └── BuffEffect: buff_id(int), duration(float)
   ```
2. 创建 SkillNode bean：
   - id (int), name (text)
   - level_required (int#range=[1,100])
   - prereq_skills (list,int) - 前置技能ID列表
   - effect (SkillEffect) - 多态效果
3. 创建 `skill_tree.xlsx`（手动注册）
4. 使用 $type 列填写多态数据

**预期输出**：
```
__beans__.xlsx: 添加 SkillEffect 多态层次
__tables__.xlsx: 添加 TbSkillTree
skill_tree.xlsx: 新建，使用 $type 列
```

**评估点**：
- [ ] 多态继承定义正确
- [ ] $type 列使用正确
- [ ] range 验证器语法
- [ ] 手动注册流程正确

---

### Task 1.3：天赋系统表 (TbTalent)

**难度**：高级
**权重**：9%

**需求**：
1. 定义多态 PassiveEffect：
   ```
   PassiveEffect (基类)
   ├── StatBonus: stat(string), value(int), is_percent(bool)
   └── SkillEnhance: skill_id(int#ref=TbSkillTree), bonus_damage(int)
   ```
2. 创建 TalentNode bean：
   - id, name, tier (int)
   - *effects (多行列表，list,PassiveEffect)
3. 创建 `#Talent.xlsx`
4. 使用多行 + 多态组合填写数据

**预期输出**：
```
__beans__.xlsx: 添加 PassiveEffect 多态层次
#Talent.xlsx: 多行列表 + 多态组合
```

**评估点**：
- [ ] 多行列表 (*field) 语法
- [ ] 多态 + 多行组合
- [ ] ref 跨表引用验证器
- [ ] 嵌套结构填写

---

## 模块 2：装备物品系统 (25%)

### Task 2.1：物品基础表 (TbItem)

**难度**：初级
**权重**：8%

**需求**：
1. 定义 Quality 枚举：
   - COMMON(普通)=1, RARE(稀有)=2, EPIC(史诗)=3, LEGENDARY(传说)=4
2. 定义 ItemType 枚举：
   - CONSUMABLE(消耗品)=1, MATERIAL(材料)=2, EQUIPMENT(装备)=3
3. 扩展现有 Item bean（或新建）：
   - id (int), name (text), desc (text)
   - quality (Quality), item_type (ItemType)
   - stack_limit (int#range=[1,9999]), sell_price (int)
4. 更新 `#demo.item.xlsx`

**预期输出**：
```
__enums__.xlsx: 添加 Quality, ItemType
#demo.item.xlsx: 添加 quality, item_type, desc 列
```

**评估点**：
- [ ] 多个枚举定义
- [ ] text 类型本地化字段
- [ ] range 验证器
- [ ] 枚举别名填写

---

### Task 2.2：装备表 (TbEquipment)

**难度**：中级
**权重**：8%

**需求**：
1. 定义 EquipSlot 枚举：
   - WEAPON=1, ARMOR=2, HELMET=3, BOOTS=4, ACCESSORY=5
2. 定义多态 Modifier：
   ```
   Modifier (基类)
   ├── FlatModifier: stat(string), value(int)
   └── PercentModifier: stat(string), percent(float)
   ```
3. 定义 Affix bean：id(int), name(string), modifier(Modifier)
4. 创建 Equipment bean：
   - id (int), name (string), slot (EquipSlot)
   - base_stats (map,string,int) - 基础属性
   - affix_pool ((list#index=id),Affix) - 词缀池，带 index 验证
   - set_id (int?) - 可空套装ID
5. 创建 `equipment.xlsx`（手动注册）

**预期输出**：
```
__enums__.xlsx: 添加 EquipSlot
__beans__.xlsx: 添加 Modifier 多态, Affix, Equipment
__tables__.xlsx: 添加 TbEquipment
equipment.xlsx: 多态 + map + list 组合
```

**评估点**：
- [ ] map 类型填写
- [ ] index 验证器
- [ ] 可空类型 (int?)
- [ ] 复杂嵌套结构

---

### Task 2.3：合成配方表 (TbRecipe)

**难度**：高级
**权重**：9%

**需求**：
1. 定义 Material bean：
   - item_id (int#ref=TbItem), count (int#range=[1,999])
2. 创建 Recipe bean：
   - id (int), name (string)
   - output_item (int#ref=TbItem)
   - output_count (int#range=[1,99])
   - *materials (多行列表，list,Material)
   - unlock_level (int#range=[1,100])
3. 创建 `#Recipe.xlsx`

**预期输出**：
```
__beans__.xlsx: 添加 Material, Recipe
#Recipe.xlsx: 多行材料列表 + 多重引用验证
```

**评估点**：
- [ ] 多行列表填写
- [ ] 多重 ref 验证器
- [ ] range 验证器组合
- [ ] 自动导入规则

---

## 模块 3：战斗数值系统 (25%)

### Task 3.1：技能效果表 (TbSkillEffect)

**难度**：中级
**权重**：8%

**需求**：
1. 定义 Element 枚举：
   - PHYSICAL=0, FIRE=1, ICE=2, LIGHTNING=3, HOLY=4, DARK=5
2. 定义深度多态 Effect：
   ```
   Effect (基类)
   ├── DamageEffect
   │   ├── PhysicalDamage: base_damage(int), armor_pen(float)
   │   └── MagicalDamage: base_damage(int), element(Element), ignore_resist(bool)
   └── HealEffect: heal_base(int), heal_scale(float)
   ```
3. 创建 SkillEffectConfig bean：
   - id (int), name (string)
   - effect (Effect)
   - scaling_stat (string), scaling_factor (float)
4. 创建 `#SkillEffect.xlsx`，使用列限定格式

**预期输出**：
```
__enums__.xlsx: 添加 Element
__beans__.xlsx: 3层多态层次
#SkillEffect.xlsx: 列限定 + 深度多态
```

**评估点**：
- [ ] 3层多态继承
- [ ] 列限定格式 (##var 子行)
- [ ] 多态类型在不同层级的字段对齐

---

### Task 3.2：Buff 表 (TbBuff)

**难度**：中级
**权重**：8%

**需求**：
1. 定义 BuffType 枚举（flags=true）：
   - NONE=0, POSITIVE=1, NEGATIVE=2, DISPELLABLE=4, STACKABLE=8
2. 定义多态 BuffEffect：
   ```
   BuffEffect (基类)
   ├── StatModifier: stat(string), value(int), is_percent(bool)
   ├── DotEffect: damage_per_tick(int), tick_interval(float)
   └── ControlEffect: control_type(string)
   ```
3. 创建 Buff bean：
   - id (int), name (text)
   - buff_type (BuffType) - flags 枚举
   - duration (float#range=[0,3600])
   - stack_limit (int#range=[1,99])
   - refresh_on_apply (bool)
   - effect (BuffEffect)
4. 创建 `buff.xlsx`（手动注册）

**预期输出**：
```
__enums__.xlsx: 添加 BuffType (flags=true)
__beans__.xlsx: 添加 BuffEffect 多态
__tables__.xlsx: 添加 TbBuff
buff.xlsx: flags枚举 + 多态效果
```

**评估点**：
- [ ] flags 枚举定义和填写
- [ ] float range 验证器
- [ ] bool 类型填写
- [ ] 手动注册流程

---

### Task 3.3：元素克制表 (TbElementRelation)

**难度**：高级
**权重**：9%

**需求**：
1. 创建 ElementRelation bean：
   - source_element (Element)
   - damage_multipliers (map,Element,float) - 对各元素的伤害倍率
2. 创建 `#ElementRelation.xlsx`
3. 使用列限定格式填写 map：$key, $value 列

**预期输出**：
```
#ElementRelation.xlsx: map类型 + 列限定 ($key, $value)
```

**评估点**：
- [ ] map 类型列限定格式
- [ ] $key, $value 列使用
- [ ] 枚举作为 map key
- [ ] 多行 map 填写

---

## 模块 4：任务剧情系统 (25%)

### Task 4.1：任务表 (TbQuest)

**难度**：中级
**权重**：8%

**需求**：
1. 定义 QuestType 枚举：
   - MAIN(主线)=1, SIDE(支线)=2, DAILY(日常)=3, EVENT(活动)=4
2. 创建 Quest bean：
   - id (int), title (text), desc (text)
   - quest_type (QuestType)
   - prereq_quest (int#ref=TbQuest?) - 可空引用
   - reward_gold (int) 带变体 variants="zh,en,jp"
   - reward_exp (int)
3. 创建 `quest.xlsx`（手动注册）
4. 使用 @variant 列填写地区差异数据

**预期输出**：
```
__enums__.xlsx: 添加 QuestType
__beans__.xlsx: 添加 Quest (含 variants)
__tables__.xlsx: 添加 TbQuest
quest.xlsx: 本地化 + 字段变体
```

**评估点**：
- [ ] text 类型本地化
- [ ] 字段变体 (@zh, @en, @jp)
- [ ] 可空引用 (ref=Table?)
- [ ] 自引用表

---

### Task 4.2：对话表 (TbDialog)

**难度**：高级
**权重**：8%

**需求**：
1. 定义多态 DialogChoice：
   ```
   DialogChoice (基类)
   ├── SimpleChoice: text(text), next_dialog(int#ref=TbDialog?)
   ├── ConditionChoice: text(text), condition(string), next_dialog(int#ref=TbDialog?)
   └── ActionChoice: text(text), action(string), params(string)
   ```
2. 定义 DialogLine bean：
   - speaker (text), content (text)
3. 创建 Dialog bean：
   - id (int), name (string)
   - *lines (多行，list,DialogLine)
   - choices (list,DialogChoice) - 分支选项
4. 创建 `#Dialog.xlsx`

**预期输出**：
```
__beans__.xlsx: 添加 DialogChoice 多态, DialogLine, Dialog
#Dialog.xlsx: 多行对话 + 多态选项
```

**评估点**：
- [ ] 多行列表嵌套本地化
- [ ] 多态 list 填写
- [ ] 复杂引用链
- [ ] 自引用验证

---

### Task 4.3：成就表 (TbAchievement)

**难度**：高级
**权重**：9%

**需求**：
1. 定义多态 AchievementCondition：
   ```
   AchievementCondition (基类)
   ├── KillCount: monster_type(string), count(int)
   ├── CollectItem: item_id(int#ref=TbItem), count(int)
   ├── CompleteQuest: quest_id(int#ref=TbQuest)
   └── ReachLevel: level(int#range=[1,100])
   ```
2. 定义 AchievementReward bean：
   - item_id (int#ref=TbItem), count (int#range=[1,999])
3. 创建 Achievement bean：
   - id (int), name (text), desc (text)
   - condition (AchievementCondition)
   - *rewards (多行，list,AchievementReward)
   - points (int) - 成就点数
4. 创建 `#Achievement.xlsx`

**预期输出**：
```
__beans__.xlsx: 添加 AchievementCondition 多态, AchievementReward, Achievement
#Achievement.xlsx: 多态条件 + 多行奖励
```

**评估点**：
- [ ] 多态条件类型
- [ ] 多重 ref 跨表引用
- [ ] 多行奖励列表
- [ ] 综合特性组合

---

## 评分标准

### 单任务评分 (100分)

| 维度 | 权重 | 评估内容 |
|------|------|----------|
| 语法正确性 | 40% | Luban 验证通过，无错误 |
| 完整性 | 30% | 覆盖任务所有需求点 |
| 最佳实践 | 20% | 命名规范、结构合理、无冗余 |
| 清晰度 | 10% | 配置易于理解和维护 |

### 模块加权

```
模块总分 = Σ(任务分数 × 任务权重)
最终总分 = 模块1×0.25 + 模块2×0.25 + 模块3×0.25 + 模块4×0.25
```

---

## 特性覆盖检查清单

### 基础特性

- [ ] 基础数据类型 (int, string, bool, float, datetime)
- [ ] 容器类型 (list, set, map, array)
- [ ] 枚举类型 (enum with alias)
- [ ] Flags 枚举 (flags=true)
- [ ] Bean 类型 (nested structures)
- [ ] 表定义 (map/list/singleton modes)
- [ ] 分组机制 (##group with c/s/e)
- [ ] 可空类型 (int?, bean?)
- [ ] 自动导入 (#前缀文件)
- [ ] 手动注册 (__tables__.xlsx)

### 高级特性

- [ ] 多态类型 (inheritance, $type column)
- [ ] 深度多态 (3层继承)
- [ ] 字段变体 (@variant)
- [ ] 数据校验器 - ref
- [ ] 数据校验器 - range
- [ ] 数据校验器 - size
- [ ] 数据校验器 - index
- [ ] 本地化 (text type)
- [ ] 紧凑格式 (sep)
- [ ] 列限定格式 ($type, $value, $key)
- [ ] 多行结构列表 (*field)
- [ ] 多行 + 多态组合
- [ ] 可空引用 (ref=Table?)
- [ ] 自引用表
