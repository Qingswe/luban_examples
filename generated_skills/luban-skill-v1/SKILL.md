# Luban 配置表编辑 Skill (综合平衡版)

---
name: luban-config-editor
description: Luban 配置表编辑 Skill。用于：(1) 创建/编辑 Excel 配置表，(2) 定义枚举/Bean/多态类型，(3) 配置验证器和本地化，(4) 处理自动导入和手动注册表。适用于游戏配置、数据驱动系统、Excel 数据建模场景。
---

## 概述

Luban 是一个强大的游戏配置解决方案，支持 Excel/JSON/XML 等多种格式。本 Skill 专注于 Excel 配置表的创建和编辑。

**核心能力**：
- Excel 配置表创建（自动导入 vs 手动注册）
- 枚举、Bean、多态类型定义
- 容器类型（list/map/set/array）填写
- 数据校验器（ref/range/index/path）
- 本地化支持（text 类型）

**工作流**：需求分析 → 设计 schema → 创建 Excel → 运行 Luban 验证 → 迭代修复

## 自动导入规则（最重要）

这是最容易出错的规则，必须牢记：

| 文件命名 | 行为 | __tables__.xlsx |
|----------|------|-----------------|
| `#TableName.xlsx` | ✅ 自动导入为 `TbTableName` | **不填** |
| `#module.Table.xlsx` | ✅ 自动导入为 `module.TbTable` | **不填** |
| `tablename.xlsx` | ❌ 不自动导入 | **必须填** |

**示例**：
```
✅ 正确：#Character.xlsx → 自动生成 TbCharacter，不填 __tables__.xlsx
✅ 正确：#demo.Item.xlsx → 自动生成 demo.TbItem，不填 __tables__.xlsx
❌ 错误：在 __tables__.xlsx 中填写 #demo.Item.xlsx
   → 导致 type:'demo.item' 和 type:'demo.Item' 类名小写重复
```

**规则细节**：
- 自动导入时，文件名去掉 `#` 和扩展名后作为 value_type
- 如果文件在子目录，子目录作为命名空间（module）
- 生成的表名：在 value_type 前加 `Tb` 前缀

## __tables__.xlsx 填写规范

对于**非自动导入**的表，必须在 `__tables__.xlsx` 中注册：

| ##var | full_name | value_type | read_schema_from_file | input | index | mode |
|-------|-----------|------------|----------------------|-------|-------|------|
| | TbSkillTree | SkillNode | TRUE | skill_tree.xlsx | | |
| | demo.TbReward | demo.Reward | TRUE | reward.xlsx | | |

**关键字段**：
- `full_name`: 表的完整名称（含命名空间）
- `value_type`: 记录类型名称
- `read_schema_from_file`: TRUE 时从 Excel 标题头读取字段定义
- `input`: 数据文件路径（**不带 # 前缀**）
- `index`: 主键字段，空则自动取 value_type 的第一个字段
- `mode`: map(默认) | list | one

**注意**：
- `read_schema_from_file=TRUE` 时，value_type 会从 Excel 标题头读取定义
- 此时**不要**在 `__beans__.xlsx` 中重复定义该 value_type
- 但被引用的其他 Bean 类型（如多态基类）需要在 `__beans__.xlsx` 中预先定义

## Excel 标题头格式

所有 Excel 配置表必须包含标题头行：

```
第1行: ##var   | id  | name  | hp   | atk  |
第2行: ##type  | int | text  | int  | int  |
第3行: ##group |     | c,s   | c,s  | s    |  (可选)
第4行: ##      | ID  | 名称   | 生命  | 攻击 |  (注释行)
第5行起: 数据行
```

**标题行说明**：
- `##var`: 字段名行，A1 单元格必须以 `##` 开头表示有效数据表
- `##type`: 字段类型行
- `##group`: 分组行（可选），c=客户端，s=服务端，c,s=两端，空=全部
- `##`: 注释行（可选，可有多行）

**重要**：
- 标题头行的顺序可以调整，Luban 根据 `##xxx` 识别行类型
- 列名为空或以 `#` 开头的列会被忽略（注释列）
- 数据行第一列以 `##` 开头的行会被忽略（注释行）

## 枚举定义（__enums__.xlsx）

在 `__enums__.xlsx` 中定义枚举类型：

| ##var | full_name | flags | unique | group | comment | tags | *items | *items | *items | *items |
|-------|-----------|-------|--------|-------|---------|------|--------|--------|--------|--------|
| ##var |           |       |        |       |         |      | name   | alias  | value  | comment|
| | CharacterClass | FALSE | TRUE | | 角色职业 | | WARRIOR | 战士 | 1 | 战士职业 |
| | | | | | | | MAGE | 法师 | 2 | 法师职业 |
| | | | | | | | ARCHER | 弓手 | 3 | 弓手职业 |

**字段说明**：
- `full_name`: 枚举名称（含命名空间）
- `flags`: 是否为位标志枚举（TRUE/FALSE）
- `unique`: 枚举值是否唯一
- `*items`: 多行列表，每行一个枚举项
  - `name`: 枚举项名称
  - `alias`: 别名（填表时可用）
  - `value`: 枚举值
  - `comment`: 注释

**Flags 枚举示例**：
```
| | BuffType | TRUE | TRUE | | Buff类型 | | NONE | 无 | 0 | |
| | | | | | | | POSITIVE | 正面 | 1 | |
| | | | | | | | NEGATIVE | 负面 | 2 | |
| | | | | | | | DISPELLABLE | 可驱散 | 4 | |
```

填写时可用 `|` 分隔：`POSITIVE|DISPELLABLE` 表示值为 5

## Bean 定义（__beans__.xlsx）

在 `__beans__.xlsx` 中定义结构体和多态类型：

### 普通 Bean

| ##var | full_name | parent | *fields | *fields | *fields | *fields |
|-------|-----------|--------|---------|---------|---------|---------|
| ##var |           |        | name    | type    | group   | comment |
| | Item | | id | int | | 物品ID |
| | | | name | text | c,s | 物品名称 |
| | | | count | int | c,s | 数量 |

### 多态类型（继承）

```
| ##var | full_name | parent | *fields | *fields | *fields |
|-------|-----------|--------|---------|---------|---------|
| ##var |           |        | name    | type    | comment |
| | SkillEffect | | | | 技能效果基类 |
| | DamageEffect | SkillEffect | damage | int | 伤害值 |
| | | | element | string | 元素类型 |
| | HealEffect | SkillEffect | heal_amount | int | 治疗量 |
| | | | heal_percent | float | 治疗百分比 |
```

**多态要点**：
- 基类：定义 full_name，parent 为空
- 子类：定义 full_name 和 parent（指向基类）
- 每个字段占一行，Bean 名称行之后的空行（第二列为空）是字段行
- **所有字段都必须定义**，不能遗漏

## 多态数据填写（$type 列）

Excel 中填写多态数据时，需要使用 `$type` 列指定具体类型：

### 方式1：合并单元格 + 子字段列

```
第1行: ##var  | id  | effect        |        |        |        |
第2行: ##type | int | SkillEffect   |        |        |        |
第3行: ##var  |     | $type         | damage | element| heal_amount |
数据:   | 1   | DamageEffect  | 100    | fire   |        |
       | 2   | HealEffect    |        |        | 200    |
```

**在 openpyxl 中**：
```python
# 合并 effect 列（第1-2行，第3-6列）
sheet.merge_cells(start_row=1, start_column=3, end_row=1, end_column=6)
sheet.merge_cells(start_row=2, start_column=3, end_row=2, end_column=6)

# 第3行定义子字段
sheet.cell(3, 3).value = '$type'
sheet.cell(3, 4).value = 'damage'
sheet.cell(3, 5).value = 'element'
sheet.cell(3, 6).value = 'heal_amount'
```

### 方式2：流式格式（不推荐，易错）

按顺序填写，空白单元格会被跳过，容易出错。

## 容器类型填写

### List 类型

**方式1：sep 分隔符**（推荐，简单）
```
| ##var  | id  | tags                |
| ##type | int | (list#sep=,),string |
| 数据   | 1   | tag1,tag2,tag3      |
```

**方式2：合并单元格，多列**
```
| ##var  | id  | tags   | tags   | tags   |
| ##type | int | list,string |    |        |
| 数据   | 1   | tag1   | tag2   | tag3   |
```

需要合并第1-2行的 tags 列。

**方式3：多行列表**（字段名加 `*` 前缀）
```
| ##var  | id  | *tags           |
| ##type | int | list,string     |
| 数据   | 1   | tag1            |
|        |     | tag2            |
|        |     | tag3            |
| 数据   | 2   | tag4            |
```

### Map 类型

**方式1：sep 分隔符**
```
| ##var  | id  | props                      |
| ##type | int | (map#sep=|),string,int     |
| 数据   | 1   | hp,100|atk,50|def,30       |
```

**方式2：非多行列限定**（key 作为子字段名）
```
| ##var  | id  | stats     | stats     | stats     |
| ##type | int | map,string,int |       |           |
| ##var  |     | hp        | atk       | def       |
| 数据   | 1   | 100       | 50        | 30        |
```

**方式3：多行 + $key 列**
```
| ##var  | id  | *props    | *props    |
| ##type | int | map,string,int |       |
| ##var  |     | $key      | value     |
| 数据   | 1   | hp        | 100       |
|        |     | atk       | 50        |
```

## 数据校验器

### ref 引用校验

检查字段值是否为某表的合法 key：

```
类型定义:
item_id (int#ref=TbItem)
skill_id (int#ref=TbSkillTree)

容器中的引用:
items (list,int#ref=TbItem)
或更清晰: items ((list),(int#ref=TbItem))

可空引用:
item_id (int#ref=TbItem?)   → 值为0时忽略检查
item_id (int?#ref=TbItem)   → 值为null时忽略检查

多表引用:
id (int#ref=TbItem,TbEquip)  → id必须在两表之一存在
```

**重要**：ref 引用的表名必须是**完整表名**（full_name），如 `TbItem`，不是文件名。

### range 范围校验

```
level (int#range=[1,100])     → [1, 100] 闭区间
percent (float#range=[0,1])   → [0, 1]
id (int#range=(0,])           → (0, 无穷] 左开右闭
```

### index 唯一性校验

对于 `list,Bean` 类型，要求某字段唯一：

```
类型定义:
items ((list#index=id),Item)  → items 列表中 id 字段唯一

生成代码（C#）:
List<Item> Items;
Dictionary<int, Item> Items_id;  // 自动生成的索引
```

### size 容器大小校验

```
items ((list#size=4),int)            → 必须4个元素
props ((map#size=[5,10]),string,int) → 5-10个元素
```

**注意**：size 作用于容器本身，必须用括号：`(list#size=4),int`，不能写成 `list,int#size=4`

## 本地化（text 类型）

`text` 类型用于需要本地化的字符串：

```
Excel 定义:
name (text)
desc (text)

填写数据:
| id  | name           | desc              |
| 1   | char_warrior   | desc_warrior_001  |
```

Luban 会校验 `char_warrior` 和 `desc_warrior_001` 是否为合法的本地化 key。

## 常见错误防范

| 错误 | 原因 | 正确做法 |
|------|------|----------|
| 类名小写重复 | #文件填入__tables__ | #前缀文件不填__tables__.xlsx |
| 列名重复 | 未合并单元格 | Bean/容器字段需要合并对应列 |
| $type 列缺失 | 多态数据无类型标识 | 多态字段首列必须是$type |
| Bean定义重复 | read_schema_from_file=TRUE但也在__beans__中定义 | 只在一处定义 |
| 多态字段缺失 | __beans__中字段定义不完整 | 检查每个子类的所有字段都已定义 |
| ref 引用失败 | 表名错误 | 使用完整表名（TbXxx）而非文件名 |
| 容器解析错误 | sep分隔符冲突 | map使用两级分隔符，如sep=| |

## 完整工作流程

### 1. 需求分析
- 确定表的用途和字段
- 是否需要多态？是否需要容器？
- 需要哪些校验器？

### 2. 设计 Schema
- **枚举**：在 `__enums__.xlsx` 中定义
- **多态/Bean**：在 `__beans__.xlsx` 中定义
- **表注册**：
  - 自动导入：使用 `#TableName.xlsx`，不填 __tables__
  - 手动注册：普通文件名，填 __tables__.xlsx

### 3. 创建 Excel
使用 openpyxl 创建：
```python
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active

# 标题头
sheet.append(['##var', 'id', 'name', 'level'])
sheet.append(['##type', 'int', 'text', 'int'])
sheet.append(['##group', '', 'c,s', 'c,s'])
sheet.append(['##', 'ID', '名称', '等级'])

# 数据行
sheet.append(['', 1, 'item_sword', 10])
sheet.append(['', 2, 'item_shield', 15])

wb.save('data.xlsx')
```

**多态字段**：使用 `merge_cells()` 合并单元格。

### 4. 运行 Luban 验证
```bash
cd /path/to/project
Luban.exe -t all -f --conf luban.conf
```

### 5. 迭代修复
根据错误信息修正：
- `列:xxx 重复` → 检查是否需要合并单元格
- `bean:'Xxx' 缺失 列:'yyy'` → 检查多态字段定义
- `type:'Xxx' duplicate` → 检查是否重复定义（__beans__ vs Excel标题头）

## 最佳实践

### 命名规范
- 枚举：PascalCase，如 `CharacterClass`
- Bean：PascalCase，如 `SkillNode`
- 表：`Tb` 前缀 + PascalCase，如 `TbCharacter`
- 字段：snake_case，如 `hp_growth`

### 模块组织
- 使用子目录作为命名空间：`item/equipment/` → `item.equipment.TbWeapon`
- 相关表放在同一模块下
- 使用 `#` 前缀简化自动导入流程

### 性能优化
- 大表使用 mode=map，快速查找
- 需要遍历的小表用 mode=list
- 全局配置用 mode=one（单例表）

### 数据组织
- 复杂多态数据建议使用列限定格式（易读易维护）
- 简单列表用 sep 分隔符（节省列空间）
- 多行列表适用于元素字段较多的情况

## 示例：完整的技能树表

### 1. 定义多态 SkillEffect（__beans__.xlsx）

```
| ##var | full_name | parent | *fields | *fields | *fields |
|-------|-----------|--------|---------|---------|---------|
| ##var |           |        | name    | type    | comment |
| | SkillEffect | | | | 效果基类 |
| | DamageEffect | SkillEffect | damage | int | 伤害 |
| | | | element | string | 元素 |
| | HealEffect | SkillEffect | heal_amount | int | 治疗量 |
| | | | heal_percent | float | 治疗% |
```

### 2. 注册表（__tables__.xlsx）

```
| ##var | full_name | value_type | read_schema_from_file | input |
|-------|-----------|------------|----------------------|-------|
| | TbSkillTree | SkillNode | TRUE | skill_tree.xlsx |
```

### 3. 创建数据表（skill_tree.xlsx）

使用 openpyxl：
```python
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active

# 第1行: ##var
sheet.cell(1, 1).value = '##var'
sheet.cell(1, 2).value = 'id'
sheet.cell(1, 3).value = 'name'
sheet.cell(1, 4).value = 'level_required'
sheet.cell(1, 5).value = 'prereq_skills'
sheet.cell(1, 6).value = 'effect'
sheet.merge_cells(start_row=1, start_column=6, end_row=1, end_column=9)

# 第2行: ##type
sheet.cell(2, 1).value = '##type'
sheet.cell(2, 2).value = 'int'
sheet.cell(2, 3).value = 'text'
sheet.cell(2, 4).value = 'int'
sheet.cell(2, 5).value = '(list#sep=,),int'
sheet.cell(2, 6).value = 'SkillEffect'
sheet.merge_cells(start_row=2, start_column=6, end_row=2, end_column=9)

# 第3行: ##var (子字段)
sheet.cell(3, 1).value = '##var'
sheet.cell(3, 6).value = '$type'
sheet.cell(3, 7).value = 'damage'
sheet.cell(3, 8).value = 'element'
sheet.cell(3, 9).value = 'heal_amount'

# 第4行: ##
sheet.cell(4, 1).value = '##'
sheet.cell(4, 2).value = 'ID'
sheet.cell(4, 3).value = '技能名'
sheet.cell(4, 4).value = '等级需求'
sheet.cell(4, 5).value = '前置技能'
sheet.cell(4, 6).value = '类型'
sheet.cell(4, 7).value = '伤害'

# 数据行
data = [
    ['', 2001, 'skill_fire_bolt', 1, '', 'DamageEffect', 100, 'fire', ''],
    ['', 2002, 'skill_heal', 5, '2001', 'HealEffect', '', '', 200]
]

for row_idx, row_data in enumerate(data, start=5):
    for col_idx, value in enumerate(row_data, start=1):
        sheet.cell(row_idx, col_idx).value = value

wb.save('skill_tree.xlsx')
```

### 4. 验证
```bash
Luban.exe -t all -f --conf luban.conf
```

预期输出：
```
load schema. collector: "default"
load datas begin
load datas end
validation begin
validation end
bye~
```

## 快速参考

### 类型定义语法

| 类型 | 语法 | 示例 |
|------|------|------|
| 基础类型 | `int`, `float`, `string`, `bool` | `hp (int)` |
| 枚举 | `EnumName` | `class (CharacterClass)` |
| Bean | `BeanName` | `item (Item)` |
| 可空 | `type?` | `reward_id (int?)` |
| List | `list,type` 或 `(list#sep=x),type` | `tags (list,string)` |
| Map | `map,keyType,valueType` | `props (map,string,int)` |
| 带校验 | `type#validator` | `level (int#range=[1,100])` |

### Excel 单元格操作（openpyxl）

```python
# 设置单元格值
sheet.cell(row, col).value = 'value'
# 或
sheet['A1'] = 'value'

# 合并单元格
sheet.merge_cells(start_row=1, start_column=3, end_row=1, end_column=6)
# 或
sheet.merge_cells('C1:F1')

# 添加行
sheet.append([value1, value2, value3])

# 保存
wb.save('file.xlsx')
```

### Luban 命令

```bash
# 生成所有目标
Luban.exe -t all -f --conf luban.conf

# 生成特定目标
Luban.exe -t client -f --conf luban.conf

# 排除 dev 标签的数据
Luban.exe -t all -f --excludeTag dev --conf luban.conf
```

## 疑难解答

**Q: 为什么会报"type:'Xxx' duplicate"？**

A: 常见原因：
1. 在 `__tables__.xlsx` 中设置了 `read_schema_from_file=TRUE`
2. 同时在 `__beans__.xlsx` 中也定义了同名 Bean

解决：只在一处定义。如果从 Excel 读取 schema，不要在 __beans__ 中定义。

**Q: 多态数据为什么会报"缺失 列:'xxx'"？**

A: 检查：
1. `__beans__.xlsx` 中该多态子类是否定义了所有字段
2. Excel 中 ##var 第3行是否定义了对应的子字段列
3. 数据行的值是否填在了正确的列

**Q: 为什么 list 类型报"列名重复"？**

A: list/map 等容器字段需要合并单元格。或者使用 `(list#sep=,),type` 格式在单个单元格填写。

**Q: ref 校验失败，但表确实存在？**

A: 确认使用的是**表名**（如 `TbItem`），不是文件名（如 `item.xlsx`）。

**Q: Excel 中文乱码？**

A: openpyxl 默认支持 UTF-8，但 Windows Excel 打开可能乱码。解决：
1. 用 LibreOffice 或 WPS 打开
2. 或在 Excel 中选择"数据" → "获取数据" → "导入 Excel"，指定编码

---

**学习路径建议**：
1. 从简单表开始（枚举 + 基础类型）
2. 掌握自动导入规则
3. 学习容器类型（list/map）
4. 学习多态类型
5. 应用数据校验器

通过逐步实践，快速掌握 Luban 配置表编辑！
