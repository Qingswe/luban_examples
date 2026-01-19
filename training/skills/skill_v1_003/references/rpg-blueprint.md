# RPG 配置系统默认蓝图（覆盖 Luban Excel 高级特性）

当用户说“给我一套完整 RPG 配置系统”但没给更多细节时，默认按本蓝图生成并输出：
- 1 份 schema XML（enum/bean/table/constalias）
- 多张 Excel（Markdown 表格，可复制到 Excel）

## 目录与命名（默认）

- XML：`Defines/rpg.xml`（单模块 `rpg`，需要拆分时再按 `common/rpg` 分开）
- Excel 输入目录（schema 的 `input="..."`）：`character/` `skill/` `equip/` `quest/` `dungeon/` `shop/` `config/`

## 需要生成的核心表（建议最少 10 张）

### 角色系统

- `TbCharacter`（普通表）
  - 覆盖点：基础类型、可空类型、enum 别名、`##group`（c/s）
- `TbLevelConfig`（`mode="one"` + 纵表 `##column`）
  - 覆盖点：单例表、纵表、`sep`、（可选）`#format=lite`
- `TbClassConfig`（普通表）
  - 覆盖点：map/bean（可选）、职业初始属性

### 技能系统

- `TbSkill`（普通表）
  - 覆盖点：bean、可空、限定列（多级 `##var`）
- `TbSkillUpgrade`（普通表或 list 表）
  - 覆盖点：多行结构列表 `*field`（同一记录跨多行续写）
- `TbSkillEffect`（可选拆表）
  - 覆盖点：多态 bean（`$type`），至少 2 个子类型

### 装备系统

- `TbEquip`（普通表）
  - 覆盖点：enum、bean、可空类型
- `TbEquipSet`（普通表）
  - 覆盖点：`map,K,V` 的限定列（`$key` + 子字段列）
- `TbEquipEnhance`（普通表）
  - 覆盖点：多级标题头 / 列限定 / 成长曲线（可用 `IntRange/FloatRange`）

### 任务系统

- `TbQuest`（`mode="list"` + `index="quest_type+quest_id"`）
  - 覆盖点：联合索引、条件多态（`QuestCondition`）
- `TbQuestReward`（普通表）
  - 覆盖点：紧凑格式（`#format=lite/json`）、容器类型
- `TbQuestDialog`（`mode="list"`）
  - 覆盖点：无主键表（list），（可选）tag（dev/test）

### 副本系统

- `TbDungeonGlobal`（`mode="one"` + 纵表 `##column`）
  - 覆盖点：单例+纵表、flags 枚举、紧凑格式
- `TbDungeonDrop`（普通表）
  - 覆盖点：flags 枚举（推荐演示“列限定模式”：每个 flag 一列）

### 商店系统

- `TbShopItem`（普通表）
  - 覆盖点：`constalias`（货币/道具）、记录 tag（dev/test/##）、datetime
- `TbSystemParam`（普通表或 list 表）
  - 覆盖点：同一类型的四种紧凑格式 `stream/lite/json/lua`（用 `#format=...`）

## 额外必覆盖点（全系统至少出现一次）

- 独立索引：例如 `TbItem` 使用 `index="id,key"`（`id` 与 `key` 各自唯一）
- `sep`：至少 1 个字段使用 `#sep=|` 或 type tag `#sep=|`
- `null` vs `""`：至少 1 个 `string?` / `bean?` / `int?` 的对比样例

## 输出建议结构（对用户的最终交付物）

1) `rpg.xml`：完整 XML 定义（可直接放入项目 Defines）
2) 按 Excel 文件逐个输出 Markdown 表格（建议按目录分段）
3) 最后一段列出“功能点覆盖清单”逐条打勾

