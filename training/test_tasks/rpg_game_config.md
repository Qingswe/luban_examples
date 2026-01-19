# RPG 游戏配置需求文档

## 项目概述

设计一个完整的 RPG 游戏配置系统，使用 Luban 配置工具进行数据管理。该系统需要涵盖游戏的所有核心模块，并使用 Luban 的所有 Excel 格式功能。

## 一、枚举类型定义 (__enums__.xlsx)

### 1.1 角色相关枚举

```
ECharacterClass - 角色职业枚举
  WARRIOR(战士) = 1
  MAGE(法师) = 2
  ARCHER(弓箭手) = 3
  PRIEST(牧师) = 4
  ASSASSIN(刺客) = 5

EElementType - 元素类型枚举
  FIRE(火) = 1
  ICE(冰) = 2
  THUNDER(雷) = 3
  WIND(风) = 4
  EARTH(土) = 5
  LIGHT(光) = 6
  DARK(暗) = 7

ERarity - 稀有度枚举
  COMMON(普通) = 1
  UNCOMMON(优秀) = 2
  RARE(稀有) = 3
  EPIC(史诗) = 4
  LEGENDARY(传说) = 5

EBuffType - Buff类型枚举 (flags=true)
  ATTACK_UP(攻击提升) = 1
  DEFENSE_UP(防御提升) = 2
  SPEED_UP(速度提升) = 4
  HEAL_OVER_TIME(持续治疗) = 8
  INVINCIBLE(无敌) = 16
  STUN(眩晕) = 32
  SILENCE(沉默) = 64
```

### 1.2 装备相关枚举

```
EEquipSlot - 装备槽位枚举
  WEAPON(武器) = 1
  HEAD(头盔) = 2
  CHEST(胸甲) = 3
  LEGS(腿甲) = 4
  BOOTS(鞋子) = 5
  RING(戒指) = 6
  NECKLACE(项链) = 7

EWeaponType - 武器类型枚举
  SWORD(剑) = 1
  BOW(弓) = 2
  STAFF(法杖) = 3
  DAGGER(匕首) = 4
  HAMMER(锤子) = 5
```

### 1.3 任务相关枚举

```
EQuestType - 任务类型枚举
  MAIN(主线) = 1
  SIDE(支线) = 2
  DAILY(日常) = 3
  WEEKLY(周常) = 4
  EVENT(活动) = 5

EQuestStatus - 任务状态枚举
  LOCKED(未解锁) = 0
  AVAILABLE(可接取) = 1
  IN_PROGRESS(进行中) = 2
  COMPLETED(已完成) = 3
```

## 二、Bean类型定义 (__beans__.xlsx)

### 2.1 基础数据结构

```xml
<!-- 向量类型 -->
<bean name="Vec2" sep=",">
  <var name="x" type="float"/>
  <var name="y" type="float"/>
</bean>

<bean name="Vec3" sep=",">
  <var name="x" type="float"/>
  <var name="y" type="float"/>
  <var name="z" type="float"/>
</bean>

<!-- 数值范围 -->
<bean name="IntRange" sep="-">
  <var name="min" type="int"/>
  <var name="max" type="int"/>
</bean>

<bean name="FloatRange" sep="-">
  <var name="min" type="float"/>
  <var name="max" type="float"/>
</bean>

<!-- 日期时间范围 -->
<bean name="DateTimeRange" sep=";">
  <var name="start" type="datetime?"/>
  <var name="end" type="datetime?"/>
</bean>
```

### 2.2 奖励结构

```xml
<!-- 单个奖励 -->
<bean name="Reward" sep=",">
  <var name="item_id" type="int"/>
  <var name="count" type="int"/>
</bean>

<!-- 随机奖励 -->
<bean name="RandomReward">
  <var name="item_id" type="int"/>
  <var name="count_range" type="IntRange"/>
  <var name="weight" type="int"/>
</bean>

<!-- 奖励组 -->
<bean name="RewardGroup">
  <var name="rewards" type="list,Reward"/>
  <var name="random_rewards" type="list,RandomReward"/>
</bean>
```

### 2.3 技能效果 (多态类型)

```xml
<!-- 技能效果基类 -->
<bean name="SkillEffect">
</bean>

<!-- 伤害效果 -->
<bean name="DamageEffect" parent="SkillEffect" alias="伤害">
  <var name="damage_type" type="EElementType"/>
  <var name="damage_ratio" type="float"/>
  <var name="fixed_damage" type="int"/>
</bean>

<!-- 治疗效果 -->
<bean name="HealEffect" parent="SkillEffect" alias="治疗">
  <var name="heal_ratio" type="float"/>
  <var name="fixed_heal" type="int"/>
</bean>

<!-- Buff效果 -->
<bean name="BuffEffect" parent="SkillEffect" alias="增益">
  <var name="buff_type" type="EBuffType"/>
  <var name="duration" type="float"/>
  <var name="value" type="float"/>
</bean>

<!-- 召唤效果 -->
<bean name="SummonEffect" parent="SkillEffect" alias="召唤">
  <var name="summon_id" type="int"/>
  <var name="count" type="int"/>
  <var name="duration" type="float"/>
</bean>

<!-- 传送效果 -->
<bean name="TeleportEffect" parent="SkillEffect" alias="传送">
  <var name="target_position" type="Vec3"/>
  <var name="is_relative" type="bool"/>
</bean>
```

### 2.4 装备属性结构

```xml
<!-- 基础属性 -->
<bean name="BaseStats">
  <var name="hp" type="int"/>
  <var name="mp" type="int"/>
  <var name="attack" type="int"/>
  <var name="defense" type="int"/>
  <var name="speed" type="int"/>
</bean>

<!-- 进阶属性 -->
<bean name="AdvancedStats">
  <var name="crit_rate" type="float"/>
  <var name="crit_damage" type="float"/>
  <var name="hit_rate" type="float"/>
  <var name="dodge_rate" type="float"/>
</bean>

<!-- 装备完整属性 -->
<bean name="EquipStats">
  <var name="base" type="BaseStats"/>
  <var name="advanced" type="AdvancedStats?"/>
  <var name="element_bonus" type="map,EElementType,float"/>
</bean>
```

### 2.5 任务条件 (多态类型)

```xml
<!-- 任务条件基类 -->
<bean name="QuestCondition">
</bean>

<!-- 击杀怪物条件 -->
<bean name="KillMonsterCondition" parent="QuestCondition" alias="击杀">
  <var name="monster_id" type="int"/>
  <var name="count" type="int"/>
</bean>

<!-- 收集物品条件 -->
<bean name="CollectItemCondition" parent="QuestCondition" alias="收集">
  <var name="item_id" type="int"/>
  <var name="count" type="int"/>
</bean>

<!-- 到达地点条件 -->
<bean name="ReachLocationCondition" parent="QuestCondition" alias="到达">
  <var name="location_id" type="int"/>
</bean>

<!-- 对话条件 -->
<bean name="TalkToNpcCondition" parent="QuestCondition" alias="对话">
  <var name="npc_id" type="int"/>
</bean>

<!-- 等级条件 -->
<bean name="LevelCondition" parent="QuestCondition" alias="等级">
  <var name="required_level" type="int"/>
</bean>
```

## 三、数据表定义 (__tables__.xlsx)

### 3.1 角色系统表

```xml
<!-- 角色基础属性表 - 使用基础类型和可空类型 -->
<table name="TbCharacter" value="Character" input="character/角色表.xlsx"/>

<!-- 角色等级成长表 - 单例表纵表 -->
<table name="TbLevelConfig" value="LevelConfig" mode="one" input="character/等级配置.xlsx"/>

<!-- 职业初始属性表 -->
<table name="TbClassConfig" value="ClassConfig" input="character/职业配置.xlsx"/>
```

### 3.2 技能系统表

```xml
<!-- 技能基础表 - 使用bean类型和多级标题头 -->
<table name="TbSkill" value="Skill" input="skill/技能表.xlsx"/>

<!-- 技能效果表 - 使用多态bean和容器类型 -->
<table name="TbSkillEffect" value="SkillEffectConfig" input="skill/技能效果表.xlsx"/>

<!-- 技能升级表 - 多行结构列表 -->
<table name="TbSkillUpgrade" value="SkillUpgrade" input="skill/技能升级表.xlsx"/>
```

### 3.3 装备系统表

```xml
<!-- 装备基础表 - 枚举、bean、可空类型 -->
<table name="TbEquip" value="Equipment" input="equip/装备表.xlsx"/>

<!-- 装备套装表 - map类型、列限定格式 -->
<table name="TbEquipSet" value="EquipSet" input="equip/套装表.xlsx"/>

<!-- 装备强化表 - 多级标题 -->
<table name="TbEquipEnhance" value="EquipEnhance" input="equip/强化表.xlsx"/>
```

### 3.4 任务系统表

```xml
<!-- 任务表 - 联合索引 -->
<table name="TbQuest" value="Quest" index="quest_type+quest_id" input="quest/任务表.xlsx"/>

<!-- 任务奖励表 - 容器类型、紧凑格式 -->
<table name="TbQuestReward" value="QuestReward" input="quest/任务奖励表.xlsx"/>

<!-- 任务对话表 - 多行模式 -->
<table name="TbQuestDialog" value="QuestDialog" input="quest/任务对话表.xlsx"/>
```

### 3.5 副本系统表

```xml
<!-- 副本配置表 - 单例表纵表 -->
<table name="TbDungeonGlobal" value="DungeonGlobalConfig" mode="one" input="dungeon/副本全局配置.xlsx"/>

<!-- 副本关卡表 -->
<table name="TbDungeon" value="Dungeon" input="dungeon/副本表.xlsx"/>

<!-- 副本怪物表 - 多行结构、map列限定 -->
<table name="TbDungeonMonster" value="DungeonMonster" input="dungeon/副本怪物表.xlsx"/>

<!-- 副本掉落表 - flags枚举、列限定模式 -->
<table name="TbDungeonDrop" value="DungeonDrop" input="dungeon/副本掉落表.xlsx"/>
```

### 3.6 商店系统表

```xml
<!-- 商店物品表 - 常量别名、数据标签过滤 -->
<table name="TbShopItem" value="ShopItem" input="shop/商店物品表.xlsx"/>

<!-- 商店刷新表 - datetime、时间范围 -->
<table name="TbShopRefresh" value="ShopRefresh" input="shop/商店刷新表.xlsx"/>
```

### 3.7 全局配置表

```xml
<!-- 游戏全局配置 - 单例表纵表 -->
<table name="TbGameConfig" value="GameConfig" mode="one" input="config/游戏配置.xlsx"/>

<!-- 系统参数配置 - 紧凑格式 -->
<table name="TbSystemParam" value="SystemParam" input="config/系统参数.xlsx"/>
```

## 四、Excel 数据表格式要求

### 4.1 角色表 (character/角色表.xlsx)

**功能要求**: 基础类型、可空类型、枚举类型、导出分组

| ##var | id | name | class | level | hp | mp | attack | defense | speed | element | desc |
|-------|-----|------|-------|-------|-----|-----|--------|---------|-------|---------|------|
| ##type | int | string | ECharacterClass | int | int | int | int | int | int | EElementType? | string |
| ##group | | c,s | c,s | s | c,s | c,s | c,s | c,s | c,s | c | c |
| ## | 角色ID | 角色名称 | 职业 | 等级 | 生命值 | 魔法值 | 攻击力 | 防御力 | 速度 | 元素属性 | 描述 |
| | 1001 | 艾伦 | WARRIOR | 1 | 1000 | 100 | 50 | 30 | 10 | FIRE | 勇敢的战士 |

### 4.2 等级配置 (character/等级配置.xlsx) - 纵表单例表

**功能要求**: 纵表格式(##column)、单例表(mode="one")

| ##column#var | ##type | ## | |
|--------------|--------|-----|--|
| max_level | int | 最大等级 | 100 |
| exp_base | int | 经验基数 | 100 |
| exp_factor | float | 经验系数 | 1.5 |
| hp_per_level | int | 每级生命成长 | 50 |
| mp_per_level | int | 每级魔法成长 | 20 |
| stat_growth | (list#sep=\|),int | 属性成长列表 | 5\|3\|2\|1 |

### 4.3 技能表 (skill/技能表.xlsx)

**功能要求**: Bean类型、多级标题头、可空类型

| ##var | id | name | cooldown | cost | cost | effects | effects | effects | effects |
|-------|-----|------|----------|------|------|---------|---------|---------|---------|
| ##type | int | string | float | BaseStats | BaseStats | list,SkillEffect | list,SkillEffect | list,SkillEffect | list,SkillEffect |
| ##var | | | | hp | mp | | | | |
| ## | 技能ID | 技能名称 | 冷却时间 | 消耗HP | 消耗MP | 效果1 | 效果2 | 效果3 | 效果4 |
| | 2001 | 火球术 | 5.0 | 0 | 30 | DamageEffect | FIRE | 1.5 | 0 |

### 4.4 技能效果表 (skill/技能效果表.xlsx)

**功能要求**: 多态Bean类型、限定列格式、$type列

| ##var | id | effect | effect | effect | effect | effect |
|-------|-----|--------|--------|--------|--------|--------|
| ##type | int | SkillEffect | SkillEffect | SkillEffect | SkillEffect | SkillEffect |
| ##var | | $type | damage_type | damage_ratio | fixed_damage | |
| ## | 效果ID | 类型 | 伤害类型 | 伤害比例 | 固定伤害 | |
| | 3001 | DamageEffect | FIRE | 1.5 | 100 | |
| | 3002 | HealEffect | | 0.3 | 200 | |
| | 3003 | BuffEffect | ATTACK_UP | 10.0 | 0.5 | |

### 4.5 技能升级表 (skill/技能升级表.xlsx)

**功能要求**: 多行结构列表(*field)

| ## | skill_id | *levels | *levels | *levels | *levels |
|----|----------|---------|---------|---------|---------|
| ##type | int | list,SkillLevel | list,SkillLevel | list,SkillLevel | list,SkillLevel |
| ##var | | level | cost | damage_bonus | cooldown_reduce |
| | 2001 | 1 | 100 | 0 | 0 |
| | | 2 | 200 | 10 | 0.5 |
| | | 3 | 400 | 25 | 1.0 |
| | 2002 | 1 | 150 | 0 | 0 |
| | | 2 | 300 | 15 | 0.3 |

### 4.6 装备表 (equip/装备表.xlsx)

**功能要求**: 枚举类型、Bean类型、可空类型、导出分组

| ##var | id | name | slot | weapon_type | rarity | stats | stats | stats | stats | stats | set_id |
|-------|-----|------|------|-------------|--------|-------|-------|-------|-------|-------|--------|
| ##type | int | string | EEquipSlot | EWeaponType? | ERarity | BaseStats | BaseStats | BaseStats | BaseStats | BaseStats | int? |
| ##var | | | | | | hp | mp | attack | defense | speed | |
| ##group | | c,s | c,s | c | c,s | c,s | c,s | c,s | c,s | c,s | s |
| ## | 装备ID | 装备名称 | 槽位 | 武器类型 | 稀有度 | HP | MP | 攻击 | 防御 | 速度 | 套装ID |
| | 4001 | 火焰之剑 | WEAPON | SWORD | EPIC | 0 | 0 | 100 | 0 | 10 | 1 |

### 4.7 套装表 (equip/套装表.xlsx)

**功能要求**: Map类型、列限定格式

| ## | id | name | *bonuses | *bonuses | *bonuses | *bonuses |
|----|-----|------|----------|----------|----------|----------|
| ##type | int | string | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats |
| ##var | | | $key | hp | attack | defense |
| ## | 套装ID | 套装名称 | 件数 | HP加成 | 攻击加成 | 防御加成 |
| | 1 | 火焰套装 | 2 | 100 | 10 | 5 |
| | | | 4 | 300 | 30 | 15 |
| | | | 6 | 600 | 60 | 30 |

### 4.8 任务表 (quest/任务表.xlsx)

**功能要求**: 联合索引(index="quest_type+quest_id")、多态Bean

| ##var | quest_type | quest_id | name | level_req | conditions | conditions | conditions | conditions |
|-------|------------|----------|------|-----------|------------|------------|------------|------------|
| ##type | EQuestType | int | string | int | list,QuestCondition | list,QuestCondition | list,QuestCondition | list,QuestCondition |
| ##var | | | | | $type | $value | $value | |
| ## | 任务类型 | 任务ID | 任务名称 | 等级要求 | 条件类型 | 条件参数1 | 条件参数2 | |
| | MAIN | 1001 | 初出茅庐 | 1 | KillMonsterCondition | 1001 | 5 | |
| | MAIN | 1002 | 勇者之路 | 5 | ReachLocationCondition | 2001 | | |

### 4.9 任务奖励表 (quest/任务奖励表.xlsx)

**功能要求**: 容器类型、紧凑格式(lite/json)

| ##var | quest_id | rewards#format=lite | random_rewards#format=json |
|-------|----------|---------------------|----------------------------|
| ##type | int | list,Reward | list,RandomReward |
| ## | 任务ID | 固定奖励 | 随机奖励 |
| | 1001 | [{1001,10},{1002,5}] | [{"item_id":2001,"count_range":{"min":1,"max":3},"weight":100}] |

### 4.10 副本全局配置 (dungeon/副本全局配置.xlsx) - 纵表单例表

**功能要求**: 纵表格式(##column)、单例表、紧凑格式

| ##column#var | ##type | ## | |
|--------------|--------|-----|--|
| daily_limit | int | 每日次数限制 | 3 |
| energy_cost | int | 体力消耗 | 10 |
| revive_cost | int | 复活消耗 | 50 |
| sweep_unlock_star | int | 扫荡解锁星数 | 3 |
| buff_config#format=lite | list,BuffEffect | Buff配置 | [{ATTACK_UP,300,0.1},{DEFENSE_UP,300,0.1}] |

### 4.11 副本掉落表 (dungeon/副本掉落表.xlsx)

**功能要求**: Flags枚举、列限定模式

| ##var | id | drop_condition | drop_condition | drop_condition | drop_condition | rewards |
|-------|-----|----------------|----------------|----------------|----------------|---------|
| ##type | int | EBuffType | EBuffType | EBuffType | EBuffType | list,Reward |
| ##var | | ATTACK_UP | DEFENSE_UP | SPEED_UP | INVINCIBLE | |
| ## | 掉落ID | 攻击提升 | 防御提升 | 速度提升 | 无敌 | 奖励列表 |
| | 5001 | 1 | 1 | | | 1001,10 |
| | 5002 | | | 1 | 1 | 2001,5 |

### 4.12 商店物品表 (shop/商店物品表.xlsx)

**功能要求**: 常量别名(constalias)、数据标签过滤(tag)

首先在 schema 中定义常量别名:
```xml
<constalias name="GOLD_COIN" value="1001"/>
<constalias name="DIAMOND" value="1002"/>
<constalias name="POTION_HP" value="2001"/>
```

| ##var | id | item_id | price | currency | stock | refresh_time |
|-------|-----|---------|-------|----------|-------|--------------|
| ##type | int | int | int | int | int? | datetime |
| ## | 商品ID | 物品ID | 价格 | 货币类型 | 库存 | 刷新时间 |
| | 6001 | POTION_HP | 100 | GOLD_COIN | 99 | 2024-01-01 00:00:00 |
| dev | 6002 | DIAMOND | 1 | GOLD_COIN | | 2024-01-01 00:00:00 |
| ## | 6003 | 测试物品 | 0 | 0 | | |

### 4.13 系统参数配置 (config/系统参数.xlsx)

**功能要求**: 多种紧凑格式(stream, lite, json, lua)

| ##var | id | vec_stream | vec_lite#format=lite | vec_json#format=json | vec_lua#format=lua |
|-------|-----|------------|---------------------|----------------------|---------------------|
| ##type | int | Vec3 | Vec3 | Vec3 | Vec3 |
| ## | ID | 流式格式 | lite格式 | json格式 | lua格式 |
| | 7001 | 1,2,3 | {1,2,3} | {"x":1,"y":2,"z":3} | {x=1,y=2,z=3} |

### 4.14 Sep分割示例

| ##var | id | rewards#sep=\| | positions#sep=; |
|-------|-----|----------------|-----------------|
| ##type | int | (list#sep=,),Reward | list,Vec3 |
| ## | ID | 奖励列表 | 位置列表 |
| | 8001 | 1001,10\|1002,5\|1003,1 | 0,0,0;1,1,1;2,2,2 |

## 五、功能验证清单

训练完成后，生成的配置需要验证以下功能点:

1. **基础类型**: bool, byte, short, int, long, float, double, string, datetime ✓
2. **枚举类型**: 普通枚举、flags枚举、别名 ✓
3. **Bean类型**: 普通bean、多态bean、继承 ✓
4. **容器类型**: array, list, set, map ✓
5. **可空类型**: int?, string?, Bean? ✓
6. **单例表**: mode="one" ✓
7. **纵表**: ##column ✓
8. **无主键表**: mode="list" (如需要)
9. **多主键表**: 联合索引(+)、独立索引(,) ✓
10. **限定列格式**: $type, $value, $key ✓
11. **多级标题头**: 嵌套##var ✓
12. **多行结构列表**: *field ✓
13. **紧凑格式**: stream, lite, json, lua ✓
14. **常量别名**: constalias ✓
15. **数据标签**: tag过滤、##注释 ✓
16. **sep分割机制**: 各种分割符 ✓
17. **导出分组**: ##group (c, s, c,s) ✓

## 六、输出要求

请生成以下文件:

1. `__enums__.xlsx` - 枚举定义
2. `__beans__.xlsx` - Bean定义
3. `__tables__.xlsx` - 表定义
4. `character/角色表.xlsx` - 角色数据
5. `character/等级配置.xlsx` - 等级配置(纵表)
6. `skill/技能表.xlsx` - 技能数据
7. `skill/技能效果表.xlsx` - 技能效果数据
8. `skill/技能升级表.xlsx` - 技能升级数据
9. `equip/装备表.xlsx` - 装备数据
10. `equip/套装表.xlsx` - 套装数据
11. `quest/任务表.xlsx` - 任务数据
12. `quest/任务奖励表.xlsx` - 任务奖励数据
13. `dungeon/副本全局配置.xlsx` - 副本配置(纵表)
14. `dungeon/副本掉落表.xlsx` - 副本掉落数据
15. `shop/商店物品表.xlsx` - 商店物品数据
16. `config/系统参数.xlsx` - 系统参数配置

每个表格都需要包含正确的标题头格式(##var, ##type, ##group, ##等)和示例数据。

