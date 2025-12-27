---
name: luban-advanced-patterns
description: Advanced Luban patterns for complex game configurations with enterprise architecture. Use when: (1) Designing complex polymorphic type hierarchies, (2) Implementing multi-table reference chains, (3) Building enterprise-level module organization, (4) Optimizing data layout for performance, (5) Integrating Luban with C#/TypeScript codebases.
---

# Luban Advanced Configuration Patterns

## Enterprise Architecture

### Module Organization

```
Defines/
├── common/           # Shared types
│   ├── types.xml     # Common beans (Vec3, Range, etc.)
│   └── enums.xml     # Global enums
├── item/
│   ├── __module__.xml
│   ├── item.xml      # Item beans
│   └── equipment.xml # Equipment beans
├── character/
│   ├── __module__.xml
│   ├── stats.xml
│   └── skills.xml
└── quest/
    └── quest.xml
```

### Naming Conventions

```xml
<!-- Tables: TbModuleName -->
<table name="TbItem" .../>
<table name="TbCharacterStats" .../>

<!-- Beans: ModuleEntity -->
<bean name="Item"/>
<bean name="CharacterStats"/>

<!-- Fields: snake_case (auto-converts) -->
<var name="max_stack_count" type="int"/>
<!-- Generates: MaxStackCount (C#), maxStackCount (TypeScript) -->
```

## Advanced Polymorphism

### Deep Type Hierarchies

```xml
<!-- 3-level hierarchy -->
<bean name="Effect"/>

<bean name="DamageEffect" parent="Effect">
  <var name="base_damage" type="int"/>
</bean>

<bean name="PhysicalDamage" parent="DamageEffect">
  <var name="armor_penetration" type="float"/>
</bean>

<bean name="MagicalDamage" parent="DamageEffect">
  <var name="element" type="ElementType"/>
  <var name="ignore_resistance" type="bool"/>
</bean>

<bean name="BuffEffect" parent="Effect">
  <var name="duration" type="float"/>
  <var name="stackable" type="bool"/>
</bean>

<bean name="StatBuff" parent="BuffEffect">
  <var name="stat" type="StatType"/>
  <var name="value" type="int"/>
  <var name="is_percent" type="bool"/>
</bean>
```

### Column-Restricted Polymorphism

| ##var | id | effect | effect | effect | effect | effect |
|-------|-----|--------|--------|--------|--------|--------|
| ##type | int | Effect | Effect | Effect | Effect | Effect |
| ##var | | $type | base_damage | armor_penetration | element | duration |
| ##var | | | | | ignore_resistance | stackable |
| ##var | | | | | | stat |
| ##var | | | | | | value |
| | 1 | PhysicalDamage | 100 | 0.2 | | |
| | 2 | MagicalDamage | 150 | | FIRE | |
| | | | | | true | |
| | 3 | StatBuff | | | | 10.0 |
| | | | | | | true |
| | | | | | | ATK |
| | | | | | | 50 |

## Advanced Validation

### Multi-Table Reference Chain

```xml
<!-- Reference groups for reuse -->
<refgroup name="AllItems" ref="item.TbItem,item.TbEquipment,item.TbConsumable"/>

<bean name="Reward">
  <var name="item_id" type="int#ref=AllItems"/>
  <var name="count" type="int#range=[1,9999]"/>
</bean>

<bean name="Recipe">
  <var name="id" type="int"/>
  <var name="output_item" type="int#ref=item.TbItem"/>
  <var name="materials" type="(list#size=[1,5]),Material"/>
</bean>

<bean name="Material">
  <var name="item_id" type="int#ref=AllItems"/>
  <var name="count" type="int#range=[1,]"/>
</bean>
```

### Path Validators by Engine

```xml
<!-- Unity: Addressable paths -->
<var name="prefab" type="string#path=unity"/>
<!-- Validates: ${pathValidator.rootDir}/{value} exists -->

<!-- Unreal: Asset references -->
<var name="mesh" type="string#path=ue"/>
<!-- Validates: ${value}.uasset or ${value}.umap exists -->

<!-- Godot: res:// paths -->
<var name="scene" type="string#path=godot"/>
<!-- Validates: res:// prefix removed, checks relative path -->

<!-- Custom pattern -->
<var name="icon" type="string#path=normal;Assets/Icons/*.png"/>
<!-- Validates: Assets/Icons/{value}.png exists -->
```

### Composite Validators

```xml
<!-- Multiple validators on same field -->
<var name="target_id" type="int#ref=character.TbCharacter#range=[1,9999]"/>

<!-- Container with validated elements -->
<var name="skill_chain" type="(list#size=[2,5]),(int#ref=skill.TbSkill)"/>

<!-- Map with validated key and value -->
<var name="drop_table" type="map,(int#ref=item.TbItem),(float#range=[0,1])"/>

<!-- Index validator for list uniqueness -->
<bean name="AffixPool">
  <var name="affixes" type="(list#index=id),Affix"/>
</bean>
```

## Complex Excel Patterns

### Nested Multi-row with Column Restrictions

| ## | id | *skill_stages | *skill_stages | *skill_stages | *skill_stages | *skill_stages |
|----|-----|---------------|---------------|---------------|---------------|---------------|
| ##type | int | list,SkillStage | ... | ... | ... | ... |
| ##var | | level | *effects | *effects | *effects | cooldown |
| ##var | | | $type | damage | duration | |
| | 1 | 1 | PhysicalDamage | 100 | | 5.0 |
| | | | | | | |
| | | 2 | PhysicalDamage | 150 | | 4.5 |
| | | | StatBuff | | 10.0 | |
| | | 3 | PhysicalDamage | 200 | | 4.0 |
| | | | StatBuff | | 15.0 | |
| | | | StatBuff | | 15.0 | |

### Flags Enum with Column Mode

```xml
<enum name="DamageFlags" flags="true">
  <var name="NONE" value="0"/>
  <var name="CRITICAL" value="1"/>
  <var name="IGNORE_ARMOR" value="2"/>
  <var name="LIFESTEAL" value="4"/>
  <var name="AOE" value="8"/>
</enum>
```

| ##var | id | flags | flags | flags | flags |
|-------|-----|-------|-------|-------|-------|
| ##type | int | DamageFlags | DamageFlags | DamageFlags | DamageFlags |
| ##var | | CRITICAL | IGNORE_ARMOR | LIFESTEAL | AOE |
| | 1 | 1 | | 1 | |
| | 2 | 1 | 1 | | 1 |

Result: id=1 has CRITICAL|LIFESTEAL, id=2 has CRITICAL|IGNORE_ARMOR|AOE

### Compact Format Selection

| Format | Syntax | Use Case |
|--------|--------|----------|
| `sep` | `sep=","` | Simple structs: `1,2,3` for Vec3 |
| `json` | `#format=json` | Complex nested: `{"x":1,"y":2}` |
| `lua` | `#format=lua` | Lua projects: `{x=1,y=2}` |
| `lite` | `#format=lite` | Minimal: `{1,2,3}` |

## Code Integration

### C# Loading Pattern

```csharp
// Load tables
var tables = new cfg.Tables(
    file => File.ReadAllBytes($"GameData/{file}.bytes")
);

// Access with strong typing
var item = tables.TbItem.Get(1001);
var weapon = tables.TbEquipment[2001];

// Polymorphic handling
foreach (var skill in tables.TbSkill.DataList)
{
    switch (skill.Effect)
    {
        case cfg.PhysicalDamage pd:
            ApplyPhysical(pd.BaseDamage, pd.ArmorPenetration);
            break;
        case cfg.MagicalDamage md:
            ApplyMagical(md.BaseDamage, md.Element);
            break;
    }
}

// Reference navigation
var questItem = quest.RewardItem_Ref; // Auto-resolved reference
```

### TypeScript Loading Pattern

```typescript
import { Tables } from './gen/Types';

const tables = new Tables(
    (file) => fetch(`/data/${file}.json`).then(r => r.json())
);

await tables.load();

// Type-safe access
const item = tables.TbItem.get(1001);
const allItems = tables.TbItem.dataList;

// Filter with type guards
const weapons = tables.TbEquipment.dataList.filter(
    (e): e is Weapon => e.type === EquipType.WEAPON
);
```

## Performance Optimization

### Group Strategy

```xml
<!-- Split by consumer -->
<table name="TbMonsterAI" value="MonsterAI" group="s" input="ai.xlsx"/>
<table name="TbUIConfig" value="UIConfig" group="c" input="ui.xlsx"/>
<table name="TbEditorTools" value="EditorTool" group="e" input="tools.xlsx"/>

<!-- Field-level groups -->
<bean name="Item">
  <var name="id" type="int"/>
  <var name="name" type="string" group="c"/>
  <var name="server_data" type="string" group="s"/>
</bean>
```

### Data Layout

- **Vertical tables** for singleton configs (fewer parse operations)
- **Multi-row lists** when elements have many fields (reduce column count)
- **Compact formats** for small structs (reduce cell count)
- **Separate files** per module (parallel loading)

### Tag-Based Filtering

```bash
# Exclude dev/test data in production
dotnet Luban.dll --excludeTag dev,test

# Include only specific tags
dotnet Luban.dll --includeTag release
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Circular ref error | A refs B refs A | Break cycle with nullable ref (`ref=Table?`) |
| Type resolution fail | Missing parent bean | Ensure parent defined before child |
| Deep nesting errors | Too many ##var levels | Simplify with compact format or separate table |
| Large file performance | Single massive Excel | Split into multiple files, use directory input |
| Polymorphic parse fail | Wrong $type value | Use exact type name or alias |
