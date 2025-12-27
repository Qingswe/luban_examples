---
name: luban-config-examples
description: Example-focused Luban configuration skill with copy-paste ready templates. Use when: (1) Needing quick Luban table templates, (2) Looking up specific syntax examples, (3) Creating common game configuration patterns, (4) Referencing data fill formats for types.
---

# Luban Quick Reference & Templates

## 5-Minute Quick Start

### Step 1: Create XML Definition

```xml
<!-- Defines/item.xml -->
<module name="item">
  <bean name="Item">
    <var name="id" type="int"/>
    <var name="name" type="string"/>
    <var name="price" type="int"/>
  </bean>
  <table name="TbItem" value="Item" input="item.xlsx"/>
</module>
```

### Step 2: Create Excel Data

| ##var | id | name | price |
|-------|-----|------|-------|
| ##type | int | string | int |
| | 1001 | Sword | 100 |
| | 1002 | Shield | 150 |

### Step 3: Generate

```bash
dotnet Luban.dll -t all -c cs-bin -d bin --conf luban.conf
```

## Syntax Cheatsheet

### Header Rows

| Row | Format | Purpose |
|-----|--------|---------|
| `##var` | `##var, field1, field2, ...` | Define field names |
| `##type` | `##type, int, string, ...` | Define field types |
| `##group` | `##group, , c, s, c,s` | Export groups (empty=all) |
| `##` | `##, Comment1, Comment2, ...` | Comment row |
| `##column` | First cell A1 | Vertical table mode |

### Type Reference

| Type | Example Value | Notes |
|------|---------------|-------|
| `int` | `100`, `-50` | 32-bit integer |
| `long` | `10000000000` | 64-bit integer |
| `float` | `3.14` | Single precision |
| `string` | `hello` | Text, empty = "" |
| `bool` | `true`, `1`, `是` | Case insensitive |
| `datetime` | `2024-01-15 10:30:00` | Auto converts to UTC |
| `int?` | `null`, `100` | Nullable |
| `list,int` | Span columns | Container |
| `map,int,string` | Key-value pairs | Dictionary |

## Ready-to-Use Templates

### Template 1: Character Stats Table

**XML:**
```xml
<enum name="CharacterClass">
  <var name="WARRIOR" alias="战士" value="1"/>
  <var name="MAGE" alias="法师" value="2"/>
  <var name="ARCHER" alias="弓手" value="3"/>
</enum>

<bean name="CharacterStats">
  <var name="id" type="int"/>
  <var name="name" type="string"/>
  <var name="class" type="CharacterClass"/>
  <var name="hp" type="int"/>
  <var name="mp" type="int"/>
  <var name="atk" type="int"/>
  <var name="def" type="int"/>
</bean>

<table name="TbCharacter" value="CharacterStats" input="character.xlsx"/>
```

**Excel:**

| ##var | id | name | class | hp | mp | atk | def |
|-------|-----|------|-------|-----|-----|-----|-----|
| ##type | int | string | CharacterClass | int | int | int | int |
| ##group | | c | c,s | c,s | c,s | c,s | c,s |
| ## | ID | Name | Class | HP | MP | ATK | DEF |
| | 1 | Hero | WARRIOR | 1000 | 100 | 50 | 30 |
| | 2 | Mage | 法师 | 500 | 500 | 80 | 10 |

### Template 2: Item with Quality Enum

**XML:**
```xml
<enum name="Quality">
  <var name="COMMON" alias="普通" value="1"/>
  <var name="RARE" alias="稀有" value="2"/>
  <var name="EPIC" alias="史诗" value="3"/>
  <var name="LEGENDARY" alias="传说" value="4"/>
</enum>

<bean name="Item">
  <var name="id" type="int"/>
  <var name="name" type="text"/>
  <var name="quality" type="Quality"/>
  <var name="stack_limit" type="int"/>
  <var name="sell_price" type="int"/>
</bean>

<table name="TbItem" value="Item" input="item.xlsx"/>
```

**Excel:**

| ##var | id | name | quality | stack_limit | sell_price |
|-------|-----|------|---------|-------------|------------|
| ##type | int | text | Quality | int | int |
| | 1001 | ITEM_SWORD | RARE | 1 | 500 |
| | 1002 | ITEM_POTION | 普通 | 99 | 10 |
| | 1003 | ITEM_RING | 传说 | 1 | 10000 |

### Template 3: Equipment with Polymorphic Modifiers

**XML:**
```xml
<bean name="Modifier"/>
<bean name="FlatModifier" parent="Modifier">
  <var name="stat" type="string"/>
  <var name="value" type="int"/>
</bean>
<bean name="PercentModifier" parent="Modifier">
  <var name="stat" type="string"/>
  <var name="percent" type="float"/>
</bean>

<bean name="Equipment">
  <var name="id" type="int"/>
  <var name="name" type="string"/>
  <var name="modifier" type="Modifier"/>
</bean>

<table name="TbEquipment" value="Equipment" input="equipment.xlsx"/>
```

**Excel:**

| ##var | id | name | modifier | modifier | modifier |
|-------|-----|------|----------|----------|----------|
| ##type | int | string | Modifier | Modifier | Modifier |
| ##var | | | $type | stat | value |
| ##var | | | | | percent |
| | 1 | Iron Sword | FlatModifier | ATK | 10 |
| | 2 | Magic Ring | PercentModifier | MP | 0.15 |

### Template 4: Quest with Localization

**XML:**
```xml
<bean name="Quest">
  <var name="id" type="int"/>
  <var name="title" type="text"/>
  <var name="desc" type="text"/>
  <var name="reward_gold" type="int" variants="zh,en"/>
  <var name="prereq_quest" type="int#ref=quest.TbQuest?"/>
</bean>

<table name="TbQuest" value="Quest" input="quest.xlsx"/>
```

**Excel:**

| ##var | id | title | desc | reward_gold | reward_gold@zh | reward_gold@en | prereq_quest |
|-------|-----|-------|------|-------------|----------------|----------------|--------------|
| ##type | int | text | text | int | | | int |
| | 1 | QUEST_1_TITLE | QUEST_1_DESC | 100 | 150 | 80 | 0 |
| | 2 | QUEST_2_TITLE | QUEST_2_DESC | 200 | 250 | 150 | 1 |

### Template 5: Skill with References

**XML:**
```xml
<bean name="Skill">
  <var name="id" type="int"/>
  <var name="name" type="text"/>
  <var name="damage" type="int#range=[0,9999]"/>
  <var name="cooldown" type="float#range=[0,]"/>
  <var name="prereq_skills" type="list,int#ref=skill.TbSkill?"/>
</bean>

<table name="TbSkill" value="Skill" input="skill.xlsx"/>
```

**Excel:**

| ##var | id | name | damage | cooldown | prereq_skills | prereq_skills | prereq_skills |
|-------|-----|------|--------|----------|---------------|---------------|---------------|
| ##type | int | text | int | float | list,int | list,int | list,int |
| | 1 | SKILL_SLASH | 100 | 1.5 | | | |
| | 2 | SKILL_COMBO | 250 | 3.0 | 1 | | |
| | 3 | SKILL_ULTIMATE | 1000 | 10.0 | 1 | 2 | |

## Common Patterns

### Pattern: Multi-row List

**When**: List elements have multiple fields, horizontal layout too wide

| ## | id | *rewards | *rewards | *rewards |
|----|-----|----------|----------|----------|
| ##type | int | list,Reward | list,Reward | list,Reward |
| ##var | | item_id | count | probability |
| | 1 | 1001 | 10 | 0.5 |
| | | 1002 | 5 | 0.3 |
| | | 1003 | 1 | 0.2 |
| | 2 | 2001 | 20 | 1.0 |

### Pattern: Singleton Table

**When**: Global config with single record

```xml
<table name="TbGlobalConfig" value="GlobalConfig" mode="one" input="global.xlsx"/>
```

| ##column | ##type | ## | |
|----------|--------|-----|---|
| max_level | int | Max Level | 100 |
| init_gold | int | Starting Gold | 1000 |
| vip_enabled | bool | VIP System | true |

### Pattern: Map with Explicit Keys

| ##var | id | *stats | *stats | *stats |
|-------|-----|--------|--------|--------|
| ##type | int | map,string,int | map,string,int | map,string,int |
| ##var | | $key | $value | |
| | 1 | HP | 100 | |
| | | ATK | 50 | |
| | 2 | HP | 200 | |

## Error Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ref check failed` | Invalid reference ID | Ensure ID exists in referenced table |
| `duplicate key` | Same ID twice | Use unique IDs |
| `type parse error` | Wrong value format | Check type (bool: true/false/1/0) |
| `field not found` | Missing ##var column | Add field name to ##var row |
| `empty required field` | Null in non-nullable | Fill value or use nullable type |
