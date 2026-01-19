# Schema XML 写法速查（Luban 4.x）

本文件只记录 **容易写错/需要统一风格** 的点；具体字段业务由需求决定。

## 1) 基本结构

```xml
<module name="rpg">
  <!-- enums -->
  <!-- constalias -->
  <!-- beans -->
  <!-- tables -->
</module>
```

建议：同一份 XML 里只写一个 `<module>`；需要拆分时用多个 XML 文件分别写 `common`/`rpg`。

## 2) enum：中文别名 + flags

普通 enum（带中文别名）：

```xml
<enum name="ERarity">
  <var name="COMMON" alias="普通" value="1"/>
  <var name="EPIC" alias="史诗" value="4"/>
</enum>
```

flags enum（位标志）：

```xml
<enum name="EBuffType" flags="1">
  <var name="ATTACK_UP" alias="攻击提升" value="1"/>
  <var name="DEFENSE_UP" alias="防御提升" value="2"/>
  <var name="STUN" alias="眩晕" value="32"/>
</enum>
```

Excel 数据侧常见两种填法：
- 值模式：`ATTACK_UP|STUN`
- 列限定模式：每个枚举项一列，填 `1` 表示包含

## 3) constalias：常量别名

```xml
<constalias name="GOLD" value="1001"/>
<constalias name="POTION_HP" value="2001"/>
```

Excel 数据中可以直接写 `GOLD`、`POTION_HP`（前提：字段类型为数值类型，如 `int/long`）。

## 4) bean：sep、可空、容器

sep（常用在 Vec/Range/Reward）：

```xml
<bean name="Vec3" sep=",">
  <var name="x" type="float"/>
  <var name="y" type="float"/>
  <var name="z" type="float"/>
</bean>
```

可空字段：

```xml
<bean name="DateTimeRange" sep=";">
  <var name="start" type="datetime?"/>
  <var name="end" type="datetime?"/>
</bean>
```

容器：

```xml
<bean name="Reward" sep=",">
  <var name="item_id" type="int"/>
  <var name="count" type="int"/>
</bean>

<bean name="RewardGroup">
  <var name="rewards" type="list,Reward"/>
  <var name="random_rewards" type="list,RandomReward"/>
</bean>
```

## 5) 多态 bean：继承体系 + alias（推荐给策划）

写法 A：子类单独声明并用 `parent="Base"`：

```xml
<bean name="SkillEffect"/>

<bean name="DamageEffect" parent="SkillEffect" alias="伤害">
  <var name="element" type="EElementType"/>
  <var name="ratio" type="float"/>
  <var name="fixed" type="int"/>
</bean>
```

写法 B：在基类 bean 内嵌子 bean（也能表达多态）：

```xml
<bean name="SkillEffect">
  <bean name="DamageEffect" alias="伤害">
    <var name="ratio" type="float"/>
  </bean>
</bean>
```

建议：团队协作时优先写法 A（结构更清晰，便于 grep 与拆模块）。

## 6) table：mode 与 index

普通表（单主键）：

```xml
<table name="TbItem" value="Item" index="id" input="item/道具表.xlsx"/>
```

联合索引（任务：`quest_type+quest_id`）：

```xml
<table name="TbQuest" value="Quest" mode="list" index="quest_type+quest_id" input="quest/任务表.xlsx"/>
```

独立索引（多字段分别唯一：`index="id,key"`）：

```xml
<table name="TbItem" value="Item" index="id,key" input="item/道具表.xlsx"/>
```

无主键表（纯列表）：

```xml
<table name="TbQuestDialog" value="QuestDialog" mode="list" input="quest/任务对话表.xlsx"/>
```

单例表（全局配置）：

```xml
<table name="TbGameConfig" value="GameConfig" mode="one" input="config/游戏配置.xlsx"/>
```

## 7) 约定（避免踩坑）

- `index="a+b"` 表示联合唯一索引；`index="a,b"` 表示独立唯一索引（每个字段都唯一）。
- `mode="one"` 只是“只有一条记录”；Excel 是否用纵表由你的表格设计决定。
- `constalias` 只能替代数值字面量；别名是否可用取决于具体字段类型与解析器实现，输出时要给 1 行实际使用样例。

