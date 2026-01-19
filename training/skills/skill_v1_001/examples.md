# 示例

## A) 标准横表（含 group 与注释）

| ##var | id | name | desc | count |
| --- | --- | --- | --- | --- |
| ##type | int | string | string | int |
| ##group |  | c | s | c,s |
| ## | id | 名称 | 描述 | 个数 |
|  | 1001 | 奖励1 | 碎片 | 100 |
|  | 1002 | 奖励2 | 金币 | 1000 |

## B) 可空类型（关键点：`null` 与 `""`）

| ##var | id | title | note |
| --- | --- | --- | --- |
| ##type | int | string? | string? |
|  | 1 | null | "" |
|  | 2 | 你好 | null |

## C) 多态 bean（限定列：`$type`）

| ##var | id | shape | shape | shape |
| --- | --- | --- | --- | --- |
| ##type | int | Shape | Shape | Shape |
| ##var |  | $type | radius | width |
|  | 1 | Circle | 10 |  |
|  | 2 | Rectangle |  | 20 |

## D) 多行结构列表（`*field`）

| ## | id | *effects | *effects | *effects |
| --- | --- | --- | --- | --- |
| ##type | int | list,SkillEffect | list,SkillEffect | list,SkillEffect |
| ##var |  | $type | a | b |
|  | 1 | Damage | 100 | 0 |
|  |  | Heal | 50 | 0 |
|  | 2 | Buff | 1 | 10 |

## E) 记录 tag（第一列）

| ##var | id | name |
| --- | --- | --- |
| ##type | int | string |
|  | 1 | normal |
| dev | 2 | dev_only |
| ## | 3 | always_ignored |
