# Excel 表头/数据模式库（Luban 4.x）

本文件提供“可复制”的 Markdown 表格片段，用于快速拼出能被 Luban 解析的 Excel。

## 0) 通用硬规则

- `##var / ##type / ##group / ##` 行必须 **列数一致**。
- 紧凑格式写在 **字段名**：`field#format=lite/json/lua`（不是写在 type 上）。
- `*field` 多行结构：续行通常把非 `*` 列留空。
- `sep` 如需用 `#` 或 `&`，要写转义：`\\#`、`\\&`。

## 1) 普通横表（含 group 与注释）

| ##var | id | name | desc | enable |
| --- | --- | --- | --- | --- |
| ##type | int | string | string | bool |
| ##group |  | c,s | c | s |
| ## | 主键 | 名称 | 说明 | 服务端开关 |
|  | 1 | A | hello | true |
|  | 2 | B | world | false |

## 2) 可空字段（`null` vs `\"\"`）

| ##var | id | note | title |
| --- | --- | --- | --- |
| ##type | int | string? | string? |
| ## |  | `null` 与空字符串 |  |
|  | 1 | null | "" |
|  | 2 | "" | null |

## 3) 多态 bean（限定列：`$type`）

假设 `SkillEffect` 是多态基类（子类有不同字段）。

| ##var | id | effect | effect | effect | effect |
| --- | --- | --- | --- | --- | --- |
| ##type | int | SkillEffect | SkillEffect | SkillEffect | SkillEffect |
| ##var |  | $type | element | ratio | fixed |
| ## |  | 具体类型 | 元素 | 系数 | 固定值 |
|  | 1 | DamageEffect | FIRE | 1.2 | 30 |
|  | 2 | HealEffect |  | 0.8 | 200 |

提示：字段不足的子类型，对应列留空即可；如果字段差异非常大，建议拆表或改用 `#format=lite/json`。

## 4) 多行结构 list（`*field`）

假设 `SkillUpgrade` 的 `effects:list,SkillEffect` 需要跨多行续写：

| ##var | id | level | *effects | *effects | *effects | *effects |
| --- | --- | --- | --- | --- | --- | --- |
| ##type | int | int | list,SkillEffect | list,SkillEffect | list,SkillEffect | list,SkillEffect |
| ##var |  |  | $type | element | ratio | fixed |
|  | 1001 | 1 | DamageEffect | FIRE | 1.0 | 0 |
|  |  |  | BuffEffect |  |  |  |

续行规则：同一条记录追加 `*effects` 时，把 `id/level` 留空。

## 5) map 限定列（`$key`）

假设 `EquipSet.bonuses` 是 `map,int,BaseStats`（key=件数，value=属性加成）。

| ##var | id | name | *bonuses | *bonuses | *bonuses | *bonuses |
| --- | --- | --- | --- | --- | --- | --- |
| ##type | int | string | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats | map,int,BaseStats |
| ##var |  |  | $key | hp | attack | defense |
|  | 1 | 火焰套装 | 2 | 100 | 10 | 5 |
|  |  |  | 4 | 250 | 25 | 12 |

## 6) flags 枚举（值模式：`A|B`）

| ##var | id | buff_flags |
| --- | --- | --- |
| ##type | int | EBuffType |
|  | 1 | ATTACK_UP|STUN |
|  | 2 | DEFENSE_UP |

## 7) flags 枚举（列限定模式：每项一列）

| ##var | id | buff | buff | buff |
| --- | --- | --- | --- | --- |
| ##type | int | EBuffType | EBuffType | EBuffType |
| ##var |  | ATTACK_UP | DEFENSE_UP | STUN |
|  | 1 | 1 |  | 1 |
|  | 2 |  | 1 |  |

## 8) 记录 tag（dev/test/##）

启用 tag 时：**数据行第 1 列**填写 tag；字段从第 2 列开始对齐。

| ##var | id | name |
| --- | --- | --- |
| ##type | int | string |
|  | 1 | always_export |
| dev | 2 | dev_only |
| ## | 3 | never_export |

## 9) 单例表纵表（`##column#var`）

| ##column#var | ##type | ## | |
| --- | --- | --- | --- |
| max_level | int | 最大等级 | 100 |
| exp_factor | float | 经验系数 | 1.5 |
| rewards#sep=\\| | (list#sep=,),Reward | 奖励列表 | 1001,10\\|1002,5 |

## 10) 紧凑格式（`stream/lite/json/lua`）

| ##var | id | vec_stream | vec_lite#format=lite | vec_json#format=json | vec_lua#format=lua |
| --- | --- | --- | --- | --- | --- |
| ##type | int | Vec3 | Vec3 | Vec3 | Vec3 |
|  | 1 | 1,2,3 | {1,2,3} | {"x":1,"y":2,"z":3} | {x=1,y=2,z=3} |

