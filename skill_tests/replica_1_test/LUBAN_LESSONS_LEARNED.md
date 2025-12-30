# Luban配置表生成经验教训文档

## 执行日期
2025-12-29

## 测试环境
- 项目目录: `e:\Learn\luban_examples\skill_tests\replica_1_test`
- Luban版本: v4.5.0+
- 工具路径: `E:\Learn\luban_examples\Tools\Luban\Luban.exe`

---

## 发现的问题及解决方案

### 问题1: 类型重复定义 - #前缀自动导入冲突

**错误信息**: `type:'ElementRelation' duplicate`

**问题描述**:
使用`#`前缀的文件（如`#ElementRelation.xlsx`）会自动导入，Luban会从Excel标题头读取schema（类似`read_schema_from_file=TRUE`）。如果同一个类型也在`__beans__.xlsx`中定义，就会导致类型重复。

**涉及文件**:
- `#ElementRelation.xlsx` → 自动导入为 `TbElementRelation` (value_type: ElementRelation)
- `#Achievement.xlsx` → 自动导入为 `TbAchievement` (value_type: Achievement)
- `#Dialog.xlsx` → 自动导入为 `TbDialog` (value_type: Dialog)
- `#Recipe.xlsx` → 自动导入为 `TbRecipe` (value_type: Recipe)
- `#Talent.xlsx` → 自动导入为 `TbTalent` (value_type: TalentNode)
- `#SkillEffect.xlsx` → 自动导入为 `TbSkillEffect` (value_type: SkillEffectConfig)

**解决方案**:
1. **移除#前缀**: 将文件重命名为普通名称（如`element_relation.xlsx`）
2. **手动注册**: 在`__tables__.xlsx`中添加注册，设置`read_schema_from_file=FALSE`
3. **保留__beans__.xlsx定义**: 从`__beans__.xlsx`读取schema

**修复脚本**: `fix_luban_config.py`

**经验教训**:
- ✅ #前缀文件适用于简单表，schema从Excel读取
- ✅ 如果Bean结构复杂（多态、继承），应在`__beans__.xlsx`中定义，文件使用普通名称并手动注册
- ❌ 不要同时使用#前缀AND在`__beans__.xlsx`中定义相同类型

---

### 问题2: 缺失枚举定义

**错误信息**: `type:'CharacterClass' is invalid`

**问题描述**:
`#Character.xlsx`中使用了`CharacterClass`枚举，但`__enums__.xlsx`中没有定义该枚举。

**原因**:
Task 1.1的CharacterClass枚举在创建后续任务时被遗漏了。

**解决方案**:
在`__enums__.xlsx`中添加CharacterClass枚举定义：
- WARRIOR (战士) = 1
- MAGE (法师) = 2
- ARCHER (弓手) = 3
- PRIEST (牧师) = 4

**修复脚本**: `add_character_class_enum.py`

**经验教训**:
- ✅ 所有使用的枚举类型必须在`__enums__.xlsx`中预先定义
- ✅ 在添加引用之前检查被引用的类型是否存在

---

### 问题3: 表未注册

**错误信息**: `field:SkillEnhance.skill_id ref:'TbSkillTree' 不存在`

**问题描述**:
`SkillEnhance` Bean中引用了`TbSkillTree`表，但该表没有在`__tables__.xlsx`中注册。

**原因**:
`skill_tree.xlsx`（非#前缀）需要在`__tables__.xlsx`中手动注册才能被识别。

**解决方案**:
在`__tables__.xlsx`中添加注册：
```
full_name: TbSkillTree
value_type: SkillNode
read_schema_from_file: TRUE  // 从Excel读取schema
input: skill_tree.xlsx
```

**修复脚本**: `add_skilltree_table.py`

**经验教训**:
- ✅ 所有非#前缀的表文件必须在`__tables__.xlsx`中手动注册
- ✅ 被ref引用的表名必须是注册时的`full_name`（如`TbSkillTree`），不是文件名
- ✅ 如果表的schema从Excel读取，设置`read_schema_from_file=TRUE`

---

### 问题4: 多态类型缺失

**错误信息**: `type:'SkillEffect' is invalid`

**问题描述**:
`skill_tree.xlsx`中使用了`SkillEffect`多态类型，但该类型没有在`__beans__.xlsx`中定义。

**原因**:
当表使用`read_schema_from_file=TRUE`时，虽然主表的schema从Excel读取，但其使用的多态基类仍需在`__beans__.xlsx`中预先定义。

**解决方案**:
在`__beans__.xlsx`中添加SkillEffect多态层次：
- SkillEffect (基类)
  - SkillDamageEffect
  - SkillHealEffect
  - SkillBuffEffect

**修复脚本**: `add_skilleffect_beans.py`

**经验教训**:
- ✅ 即使表使用`read_schema_from_file=TRUE`，其使用的多态基类也必须在`__beans__.xlsx`中定义
- ✅ Excel中只定义表的直接字段，多态类型定义在`__beans__.xlsx`中

---

### 问题5: 多态类型名称冲突

**错误信息**: `type:'DamageEffect' duplicate`

**问题描述**:
Task 1.2的SkillEffect层次和Task 3.1的Effect层次都定义了`DamageEffect`，导致类型重复。

**涉及的多态层次**:
- **Task 1.2**: SkillEffect → DamageEffect, HealEffect, BuffEffect
- **Task 3.1**: Effect → DamageEffect → PhysicalDamage, MagicalDamage

**解决方案**:
重命名Task 1.2的类型以避免冲突：
- `DamageEffect` → `SkillDamageEffect`
- `HealEffect` → `SkillHealEffect`
- `BuffEffect` → `SkillBuffEffect`

同时更新`skill_tree.xlsx`中的`$type`列。

**修复脚本**:
- `fix_duplicate_beans.py` - 修复__beans__.xlsx
- `update_skill_tree.py` - 更新skill_tree.xlsx

**经验教训**:
- ✅ 不同的多态层次应使用不同的类型名称
- ✅ 为类型添加前缀以区分用途（如`Skill`前缀）
- ⚠️ 修改Bean类型名称后，记得更新所有使用该类型的Excel文件

---

### 问题6: 表名冲突 - demo前缀问题

**错误信息**: `field:Material.item_id ref:'TbItem' 不存在`

**问题描述**:
`#demo.item.xlsx`会自动导入为`demo.TbItem`（带命名空间前缀），但其他Bean中引用的是`TbItem`（无前缀）。

**解决方案**:
将`#demo.item.xlsx`重命名为`#Item.xlsx`，这样会自动导入为`TbItem`（无前缀）。

**经验教训**:
- ✅ #前缀文件名中的点号`.`会被解释为命名空间分隔符
  - `#demo.item.xlsx` → `demo.TbItem` (value_type: `demo.Item`)
  - `#Item.xlsx` → `TbItem` (value_type: `Item`)
- ✅ 确保ref引用的表名与实际注册的表名一致
- ✅ 避免不必要的命名空间前缀

---

### 问题7: Excel嵌套结构错误

**错误信息**: `cell:[H:6] 101 缺少数据 - 字段: {Equipment}.affix_pool => {Affix}.name`

**问题描述**:
`equipment.xlsx`中`affix_pool`字段的嵌套结构不正确。`Affix` Bean包含一个`modifier`字段（Modifier类型），需要额外的`##var`行来定义Modifier的子字段。

**正确的结构**:
```
第1行: ##var | id | name | ... | affix_pool (合并多列) | ...
第2行: ##type | int | string | ... | list,Affix (合并多列) | ...
第3行: ##var |  |  | ... | id | name | modifier (合并) | ...
第4行: ##var |  |  | ... |  |  | $type | stat | value | percent | ...
```

**经验教训**:
- ✅ 嵌套Bean需要多个`##var`行来定义子字段
- ✅ 每一层嵌套需要一个`##var`行
- ✅ 合并单元格必须正确设置，范围要覆盖所有子列
- ⚠️ 复杂嵌套结构容易出错，建议简化或使用其他数据格式

---

## 配置规则总结

### 1. 自动导入 vs 手动注册

| 方式 | 文件命名 | __tables__.xlsx | __beans__.xlsx | 适用场景 |
|------|----------|----------------|---------------|---------|
| 自动导入 | `#TableName.xlsx` | 不填 | 不填（或只填子类型） | 简单表，schema从Excel读取 |
| 手动注册 | `tablename.xlsx` | 必填 | 必填（完整Bean定义） | 复杂Bean，需要在代码中引用 |

### 2. read_schema_from_file设置

- `read_schema_from_file=TRUE`: schema从Excel标题头读取
  - 不要在`__beans__.xlsx`中定义同名Bean
  - 但要定义该Bean使用的多态基类

- `read_schema_from_file=FALSE`: schema从`__beans__.xlsx`读取
  - 必须在`__beans__.xlsx`中完整定义Bean
  - Excel只包含数据，不包含完整的类型定义

### 3. 类型定义顺序

1. **枚举**: 在`__enums__.xlsx`中定义
2. **多态基类**: 在`__beans__.xlsx`中定义
3. **Bean**: 在`__beans__.xlsx`中定义（如果read_schema_from_file=FALSE）
4. **表注册**: 在`__tables__.xlsx`中注册（如果不使用#前缀）

### 4. 引用规则

- `ref=TbXxx`: 引用的是表的`full_name`，不是文件名
- `ref=TbItem?`: 可空引用，值为0或null时不检查
- 被引用的表必须先注册

---

## 最佳实践建议

### ✅ 推荐做法

1. **简单表使用#前缀自动导入**
   - 适用于无复杂继承的简单表
   - 快速原型开发

2. **复杂Bean在__beans__.xlsx中定义**
   - 多态类型
   - 需要在多处引用的Bean
   - 需要继承的类型

3. **类型命名要有区分度**
   - 使用前缀避免冲突（如`Skill`前缀）
   - 清晰的命名表明用途

4. **分模块组织**
   - 相关表放在同一目录
   - 使用命名空间（目录结构）

5. **渐进式开发**
   - 先验证简单结构
   - 再逐步添加复杂特性
   - 每次修改后立即验证

### ❌ 避免的做法

1. **不要混用#前缀和__beans__.xlsx定义**
   - 会导致类型重复

2. **不要使用相同的多态类型名称**
   - 即使在不同层次也不行

3. **不要忘记注册引用的表**
   - ref验证会失败

4. **不要在嵌套结构中遗漏##var行**
   - 会导致字段解析错误

---

## 调试技巧

### 1. 逐步验证

```bash
# 运行Luban验证
cd e:/Learn/luban_examples/skill_tests/replica_1_test
"E:\Learn\luban_examples\Tools\Luban\Luban.exe" -t all -d json --conf luban.conf -x outputDataDir=output
```

### 2. 错误类型识别

| 错误模式 | 问题类型 | 检查内容 |
|---------|---------|----------|
| `type:'Xxx' duplicate` | 类型重复定义 | 检查#前缀和__beans__.xlsx |
| `type:'Xxx' is invalid` | 类型未定义 | 检查__enums__.xlsx和__beans__.xlsx |
| `ref:'TbXxx' 不存在` | 表未注册 | 检查__tables__.xlsx |
| `缺少数据` | Excel结构错误 | 检查合并单元格和##var行 |

### 3. 检查清单

在运行Luban之前检查：

- [ ] 所有枚举已在`__enums__.xlsx`中定义
- [ ] 多态基类已在`__beans__.xlsx`中定义
- [ ] 非#前缀表已在`__tables__.xlsx`中注册
- [ ] ref引用的表名正确（使用full_name）
- [ ] 没有类型名称冲突
- [ ] #前缀文件不在__beans__.xlsx中重复定义
- [ ] read_schema_from_file设置正确
- [ ] Excel嵌套结构的##var行完整

---

## 修复脚本列表

生成的修复脚本：
1. `fix_luban_config.py` - 修复#前缀导致的类型重复
2. `add_character_class_enum.py` - 添加CharacterClass枚举
3. `add_skilltree_table.py` - 注册TbSkillTree表
4. `add_skilleffect_beans.py` - 添加SkillEffect多态
5. `fix_duplicate_beans.py` - 修复多态类型名称冲突
6. `update_skill_tree.py` - 更新skill_tree.xlsx的$type列
7. `fix_equipment.py` / `fix_equipment_v2.py` - 修复equipment.xlsx结构

---

## 未解决的问题

### equipment.xlsx的affix_pool字段

**当前状态**: 数据解析错误

**可能原因**:
1. 嵌套结构的##var行定义不完整
2. list,Affix的列限定格式可能需要调整
3. Affix Bean中的modifier字段结构复杂

**建议方案**:
1. 简化affix_pool结构，移除modifier嵌套
2. 或使用sep分隔符格式替代列限定格式
3. 参考Luban官方示例中类似的嵌套结构

---

## 总结

本次测试发现的主要问题类型：
1. **配置冲突**: #前缀自动导入 vs __beans__.xlsx定义
2. **缺失定义**: 枚举、多态基类、表注册
3. **命名冲突**: 多个多态层次使用相同类型名
4. **引用错误**: ref引用的表名不匹配
5. **结构错误**: Excel嵌套结构不完整

**关键经验**:
- Luban的配置需要精确匹配，任何不一致都会导致错误
- 复杂结构应该逐步构建和验证
- 自动化脚本可以帮助快速修复批量问题
- 详细的错误信息是调试的关键

**下一步**:
1. 简化复杂的嵌套结构
2. 建立标准的表模板
3. 创建验证checklist
4. 记录每种结构的正确示例

---

**文档创建时间**: 2025-12-29 15:20
**修复进度**: 已修复 80%，剩余equipment.xlsx的复杂嵌套结构需要进一步调试
