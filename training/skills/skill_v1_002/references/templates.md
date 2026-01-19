# 空白模板（直接填字段即可）

## 1) 横表（最小：map/list）

| ##var | [field1] | [field2] |
| --- | --- | --- |
| ##type | [type1] | [type2] |
| ##group | [c/s/c,s/空] | [c/s/c,s/空] |
| ## | [注释] | [注释] |
|  |  |  |

## 2) 横表（启用记录 tag）

说明：数据行第 1 列为 tag（可空），字段值从第 2 列开始对齐（表头不需要额外空列）。

| ##var | [field1] | [field2] |
| --- | --- | --- |
| ##type | [type1] | [type2] |
| ##group | [c/s/c,s/空] | [c/s/c,s/空] |
| ## | [注释] | [注释] |
|  |  |  |
| dev |  |  |

## 3) 多级标题头（限定列）

| ##var | id | obj | obj | obj |
| --- | --- | --- | --- | --- |
| ##type | int | Obj | Obj | Obj |
| ##var |  | $type | [fieldA] | [fieldB] |
|  | 1 | [TypeName] |  |  |

## 4) 多行结构 list（`*field`）

| ##var | id | *items | *items |
| --- | --- | --- | --- |
| ##type | int | list,Item | list,Item |
| ##var |  | [sub1] | [sub2] |
|  | 1 |  |  |
|  |  |  |  |
