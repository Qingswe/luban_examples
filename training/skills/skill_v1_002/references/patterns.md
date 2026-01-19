# 模式库：Luban Excel 高级结构

## A) 最常见横表（含 group 与注释）

| ##var | id | name | desc | count |
| --- | --- | --- | --- | --- |
| ##type | int | string | string | int |
| ##group |  | c | s | c,s |
| ## | 主键 | 名称 | 描述 | 数量 |
|  | 1001 | Reward1 | 碎片 | 100 |
|  | 1002 | Reward2 | 金币 | 1000 |

## B) 可空字段（`null` vs `""`）

| ##var | id | title | note |
| --- | --- | --- | --- |
| ##type | int | string? | string? |
|  | 1 | null | "" |
|  | 2 | 你好 | null |

## C) Bean（流式：同名字段重复多列）

假设 `Item` 有字段：`id:int`、`num:int`。

| ##var | rewardId | item | item |
| --- | --- | --- | --- |
| ##type | int | Item | Item |
|  | 1 | 101 | 5 |
|  | 2 | 102 | 10 |

提示：这种写法依赖 bean 字段顺序；字段多或多态时更推荐“限定列”。

## D) 多态 bean（限定列：`$type`）

| ##var | id | shape | shape | shape |
| --- | --- | --- | --- | --- |
| ##type | int | Shape | Shape | Shape |
| ##var |  | $type | radius | width |
|  | 1 | Circle | 10 |  |
|  | 2 | Rectangle |  | 20 |

## E) 多行结构 list（`*field` 跨行续写）

| ##var | id | *effects | *effects | *effects |
| --- | --- | --- | --- | --- |
| ##type | int | list,Effect | list,Effect | list,Effect |
| ##var |  | $type | a | b |
|  | 1 | Damage | 100 | 0 |
|  |  | Heal | 50 | 0 |
|  | 2 | Buff | 1 | 10 |

提示：同一条记录的续行通常把非 `*effects` 的列留空（例如 id 留空）。

## F) flags 枚举（值模式：`A|B`）

| ##var | id | perm |
| --- | --- | --- |
| ##type | int | PermFlags |
|  | 1 | READ|WRITE |
|  | 2 | READ |

## G) flags 枚举（列限定模式：每项一列）

| ##var | id | perm | perm | perm |
| --- | --- | --- | --- | --- |
| ##type | int | PermFlags | PermFlags | PermFlags |
| ##var |  | READ | WRITE | ADMIN |
|  | 1 | 1 | 1 |  |
|  | 2 | 1 |  |  |

## H) 记录 tag（第一列）

| ##var | id | name |
| --- | --- | --- |
| ##type | int | string |
|  | 1 | normal |
| dev | 2 | dev_only |
| ## | 3 | always_ignored |

## I) 纵表（示意）

当用户明确需要纵表时，先确认 Luban 的纵表约定与项目读表器是否一致；常见写法如下：

| ##column#var | value |
| --- | --- |
| ##type | string |
| id | 1001 |
| name | Reward1 |
| desc | 碎片 |

