---
name: luban-config-editor
description: Comprehensive Luban configuration table editing skill for game development. Use when: (1) Creating or editing Excel/XML configuration tables with Luban framework, (2) Defining beans/enums/tables for game data, (3) Setting up type systems with polymorphism, (4) Configuring data validators and references, (5) Implementing localization with text types and variants, (6) Organizing multi-module game configurations.
---

# Luban Configuration Table Editor

## Core Concepts

Luban uses Excel/XML to define game configuration data with a complete type system supporting polymorphism.

### Header Row Format

| Row | Purpose | Example |
|-----|---------|---------|
| `##var` | Field names | `##var, id, name, count` |
| `##type` | Field types | `##type, int, string, int` |
| `##group` | Export groups | `##group, , c, s` (c=client, s=server) |
| `##` | Comments | `##, ID, Name, Count` |

### Type System

**Basic Types**: `bool`, `byte`, `short`, `int`, `long`, `float`, `double`, `string`, `text`, `datetime`

**Containers**: `list,<type>`, `set,<type>`, `map,<keyType>,<valueType>`, `array,<type>`

**Nullable**: Add `?` suffix: `int?`, `string?`, `MyBean?`

## Basic Features

### Enum Definition (XML)

```xml
<enum name="Quality" flags="false">
  <var name="WHITE" alias="白" value="1"/>
  <var name="BLUE" alias="蓝" value="2"/>
  <var name="PURPLE" alias="紫" value="3"/>
</enum>
```

### Bean Definition (XML)

```xml
<bean name="Item">
  <var name="id" type="int"/>
  <var name="name" type="string"/>
  <var name="quality" type="Quality"/>
</bean>
```

### Table Definition (XML)

```xml
<table name="TbItem" value="Item" input="item.xlsx"/>
<table name="TbSingleton" value="GlobalConfig" mode="one" input="global.xlsx"/>
<table name="TbList" value="Record" mode="list" input="records.xlsx"/>
```

### Excel Data Example

| ##var | id | name | quality | price |
|-------|-----|------|---------|-------|
| ##type | int | string | Quality | int |
| ##group | | c | c,s | s |
| ## | ID | Name | Quality | Price |
| | 1001 | Sword | BLUE | 100 |
| | 1002 | Shield | 紫 | 200 |

## Advanced Features

### Polymorphic Types

Define inheritance hierarchy:

```xml
<bean name="Shape"/>
<bean name="Circle" parent="Shape">
  <var name="radius" type="float"/>
</bean>
<bean name="Rectangle" parent="Shape">
  <var name="width" type="float"/>
  <var name="height" type="float"/>
</bean>
```

Excel with $type column:

| ##var | id | shape | shape | shape |
|-------|-----|-------|-------|-------|
| ##type | int | Shape | Shape | Shape |
| ##var | | $type | radius | width |
| | 1 | Circle | 10.5 | |
| | 2 | Rectangle | | 20 |

### Data Validators

```xml
<var name="itemId" type="int#ref=item.TbItem"/>
<var name="count" type="int#range=[1,100]"/>
<var name="icon" type="string#path=unity"/>
<var name="items" type="(list#size=[1,10]),int"/>
<var name="tags" type="(list#index=id),Tag"/>
```

### Localization

**Text type** for localized strings:

```xml
<var name="desc" type="text"/>  <!-- equivalent to string#text=1 -->
```

**Field variants** for region-specific data:

```xml
<var name="reward" type="int" variants="zh,en,jp"/>
```

Excel: Use `field@variant` columns:

| ##var | id | reward | reward@zh | reward@en |
|-------|-----|--------|-----------|-----------|
| ##type | int | int | | |
| | 1 | 100 | 150 | 80 |

### Multi-row Lists

Use `*` prefix for multi-row data:

| ## | id | *items | *items | *items |
|----|-----|--------|--------|--------|
| ##type | int | list,Item | list,Item | list,Item |
| ##var | | id | count | name |
| | 1 | 1001 | 10 | Sword |
| | | 1002 | 5 | Shield |
| | 2 | 2001 | 1 | Potion |

### Compact Formats

```xml
<bean name="Vec3" sep=",">
  <var name="x" type="float"/>
  <var name="y" type="float"/>
  <var name="z" type="float"/>
</bean>
```

Fill as: `1.0,2.0,3.0`

## Workflow

1. **Design Schema**: Define enums, beans, tables in XML
2. **Create Excel Files**: Set up header rows, fill data
3. **Configure Groups**: Use ##group for client/server split
4. **Add Validators**: Apply ref, range, path validators
5. **Generate**: Run Luban to generate code and data
6. **Validate**: Check output for errors, fix and regenerate

## Best Practices

- Use `TbXxxYyy` naming for tables
- Use `xx_yy_zz` field naming (auto-converts to language conventions)
- Organize by module: `item.TbItem`, `quest.TbQuest`
- Use polymorphism for complex GamePlay data (skills, AI, quests)
- Use `unchecked` tag for WIP data to skip validation
- Use `##` tag for permanently commented-out records
