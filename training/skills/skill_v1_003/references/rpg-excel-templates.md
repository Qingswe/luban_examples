# RPG Excel 表格模板（Markdown，可复制到 Excel）

这些模板与 `references/rpg-schema-template.xml` 的类型/字段名对应，方便直接落地。

## 1) `item/道具表.xlsx`（独立索引：id 与 key 各自唯一）

| ##var | id | key | name | rarity |
| --- | --- | --- | --- | --- |
| ##type | int | string | string | ERarity |
| ## | 道具ID | 唯一字符串key | 名称 | 稀有度 |
|  | 1001 | gold | 金币 | COMMON |
|  | 2001 | potion_hp | 生命药水 | UNCOMMON |

## 2) `character/角色表.xlsx`（基础类型 + 可空 + enum + group）

| ##var | id | name | class | level | base_stats | base_stats | base_stats | base_stats | base_stats | element | desc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ##type | int | string | ECharacterClass | int | BaseStats | BaseStats | BaseStats | BaseStats | BaseStats | EElementType? | string? |
| ##group |  | c,s | c,s | s | c,s | c,s | c,s | c,s | c,s | c | c |
| ##var |  |  |  |  | hp | mp | attack | defense | speed |  |  |
| ## | 角色ID | 角色名 | 职业 | 初始等级(仅服) | 生命 | 法力 | 攻击 | 防御 | 速度 | 元素(可空) | 描述(可空) |
|  | 1001 | 艾伦 | WARRIOR | 1 | 1000 | 100 | 50 | 30 | 10 | FIRE | 勇敢的战士 |
|  | 1002 | 露娜 | MAGE | 1 | 700 | 300 | 35 | 20 | 12 | null | "" |

## 3) `character/等级配置.xlsx`（单例表 + 纵表）

| ##column#var | ##type | ## | |
| --- | --- | --- | --- |
| max_level | int | 最大等级 | 100 |
| exp_base | int | 经验基数 | 100 |
| exp_factor | float | 经验系数 | 1.5 |
| hp_per_level | int | 每级生命成长 | 50 |
| mp_per_level | int | 每级法力成长 | 20 |

## 4) `skill/技能表.xlsx`（可空 + 多级标题头示例）

| ##var | id | name | cooldown | cost | cast_range | cast_range | desc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ##type | int | string | float | int | FloatRange? | FloatRange? | string? |
| ##var |  |  |  |  | min | max |  |
| ## | 技能ID | 名称 | 冷却 | 消耗 | 最小距离 | 最大距离 | 描述 |
|  | 3001 | 火球术 | 3.5 | 20 | 0.0 | 8.0 | 对目标造成火焰伤害 |
|  | 3002 | 治疗术 | 8.0 | 35 | null | null | "" |

## 5) `skill/技能升级表.xlsx`（多行结构 list + 多态 SkillEffect）

| ##var | id | level | need_gold | *effects | *effects | *effects | *effects | *effects |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ##type | int | int | int | list,SkillEffect | list,SkillEffect | list,SkillEffect | list,SkillEffect | list,SkillEffect |
| ##var |  |  |  | $type | damage_type | damage_ratio | fixed_damage | fixed_heal |
| ## | 技能ID | 等级 | 升级金币 | 效果类型 | 元素 | 系数 | 固定伤害 | 固定治疗 |
|  | 3001 | 1 | 100 | DamageEffect | FIRE | 1.0 | 0 |  |
|  |  |  |  | BuffEffect |  |  |  |  |
|  | 3001 | 2 | 250 | DamageEffect | FIRE | 1.2 | 20 |  |
|  | 3002 | 1 | 120 | HealEffect |  | 0.8 |  | 120 |

## 6) `equip/套装表.xlsx`（map 限定列 + `$key`）

| ##var | id | name | *bonuses | *bonuses | *bonuses | *bonuses | *bonuses | *bonuses |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ##type | int | string | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats |
| ##var |  |  | $key | hp | mp | attack | defense | speed |
| ## | 套装ID | 名称 | 件数 | 生命 | 法力 | 攻击 | 防御 | 速度 |
|  | 1 | 火焰套装 | 2 | 100 | 0 | 10 | 5 | 0 |
|  |  |  | 4 | 250 | 0 | 25 | 12 | 0 |

## 7) `quest/任务表.xlsx`（联合索引 + 多态条件）

| ##var | quest_type | quest_id | name | level_req | conditions | conditions | conditions | conditions | next_quest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ##type | EQuestType | int | string | int | list,QuestCondition | list,QuestCondition | list,QuestCondition | list,QuestCondition | int? |
| ##var |  |  |  |  | $type | monster_id | count | item_id |  |
| ## | 类型 | ID | 名称 | 等级要求 | 条件类型 | 怪物ID | 数量 | 物品ID | 下一任务(可空) |
|  | MAIN | 1001 | 初出茅庐 | 1 | KillMonsterCondition | 9001 | 5 |  | 1002 |
|  | MAIN | 1002 | 收集补给 | 2 | CollectItemCondition |  | 10 | 2001 | null |

## 8) `quest/任务奖励表.xlsx`（紧凑格式：lite + json）

| ##var | quest_id | rewards#format=lite | random_rewards#format=json |
| --- | --- | --- | --- |
| ##type | int | list,Reward | list,RandomReward |
| ## | 任务ID | 固定奖励（lite） | 随机奖励（json） |
|  | 1001 | [{1001,100},{POTION_HP,2}] | [{"item_id":2001,"count_range":{"min":1,"max":3},"weight":100}] |
|  | 1002 | [{1001,150}] | [] |

## 9) `dungeon/副本掉落表.xlsx`（flags：列限定模式）

| ##var | id | need_buffs | need_buffs | need_buffs | rewards#sep=\\| |
| --- | --- | --- | --- | --- | --- |
| ##type | int | EBuffType | EBuffType | EBuffType | (list#sep=,),Reward |
| ##var |  | ATTACK_UP | DEFENSE_UP | STUN |  |
| ## | 掉落ID | 攻击提升 | 防御提升 | 眩晕 | 奖励列表（`|` 分割） |
|  | 5001 | 1 | 1 |  | 1001,10\\|POTION_HP,1 |
|  | 5002 |  |  | 1 | 1001,30 |

## 10) `shop/商店物品表.xlsx`（constalias + tag + datetime）

启用记录 tag：数据行第 1 列填写 tag（如 `dev`/`test`/`##`），字段从第 2 列开始对齐。

| ##var | id | item_id | price | currency_id | stock | refresh_time | available_time | available_time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ##type | int | int | int | int | int? | datetime | DateTimeRange? | DateTimeRange? |
| ##var |  |  |  |  |  |  | start | end |
| ## | 商品ID | 道具ID | 价格 | 货币(道具ID) | 库存(可空) | 刷新时间 | 上架开始 | 上架结束 |
|  | 6001 | POTION_HP | 100 | GOLD | 99 | 2024-01-01 00:00:00 | null | null |
| dev | 6002 | DIAMOND | 1 | GOLD | null | 2024-01-01 00:00:00 | 2024-01-01 00:00:00 | 2024-02-01 00:00:00 |
| ## | 6003 | POTION_MP | 0 | GOLD | null | 2024-01-01 00:00:00 | null | null |

## 11) `config/系统参数.xlsx`（四种紧凑格式）

| ##var | id | vec_stream | vec_lite#format=lite | vec_json#format=json | vec_lua#format=lua |
| --- | --- | --- | --- | --- | --- |
| ##type | int | Vec3 | Vec3 | Vec3 | Vec3 |
| ## | ID | stream | lite | json | lua |
|  | 7001 | 1,2,3 | {1,2,3} | {"x":1,"y":2,"z":3} | {x=1,y=2,z=3} |

