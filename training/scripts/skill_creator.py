#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class SkillFiles:
    system_md: str
    knowledge_md: str
    examples_md: str
    readme_md: str


def _write_text(path: Path, content: str, *, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, obj: object, *, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_luban_excel_editor_files() -> SkillFiles:
    system_md = """\
你是一个「Luban Excel 配置表编辑器」。

你的目标：根据用户需求，生成/修改符合 Luban 4.x Excel 读表规则的表头与数据填写方案（必要时给出可直接复制到 Excel 的 Markdown 表格）。

工作方式：
1) 先问清楚缺失信息：表用途（客户端/服务器/双端）、是否需要 tag 过滤、是否需要多态/多行结构列表/纵表、字段是否可空、容器分隔符 sep、是否需要紧凑格式 format（json/lua/lite/stream）。
2) 输出时优先给出：`##var`、`##type`、`##group`（可选）、`##` 注释行，以及示例数据行。
3) 严格使用 Luban 类型字符串（如 `list,int`、`map,int,string`、`int?`、`string#escape=1`、`(list#sep=|),int` 等）。
4) 对多态 bean：在流式格式下先填具体类型名/别名；在限定列格式下使用 `$type`（必要时配合 `$value`）。
5) 对多行结构列表：用 `*field` 标记，按 Luban 多行读入规则给出示例。
6) 若用户只给了业务含义但没给 schema（enum/bean/table 定义），先提出你需要的最小 schema 信息，再给出可落地的 Excel 方案。
"""

    knowledge_md = """\
# luban-excel-editor 知识库（摘要版）

## 1) 类型系统
- 基础类型：`bool, byte, short, int, long, float, double, string, datetime, text`
- 容器类型：`array,T` `list,T` `set,T` `map,K,V`（例：`list,string`、`map,int,string`）
- 可空类型：`T?`（除容器外的类型通常可空；用 `null` 表示空值）
- 自定义类型：`enum`、`bean`（支持继承/多态）

## 2) Excel 标题头
- `##var`：字段名行（支持多行 `##var` 表示多级标题头/嵌套字段）
- `##type`：类型行
- `##group`：导出分组（`c` 客户端，`s` 服务器，`c,s` 双端；留空表示对所有分组导出）
- `##` 或任意 `##xxx`：注释行（不参与导出；通常首个注释行用作字段注释）
- 纵表：A1 为 `##column#var` 或 `##vertical#var`
- 注释列：字段名为空或以 `#` 开头的列会被忽略

## 3) 表模式（来自 schema 的 table 定义）
- `mode="map"`：普通表（默认，通常带主键/索引）
- `mode="list"`：无主键表（仅记录列表）
- `mode="one"`：单例表（全局一份配置）
- `index="k1+k2"`：联合索引；`index="k1,k2"`：独立索引
注：这些通常写在 schema 的 `<table .../>` 上；Excel 侧主要负责字段与数据填写。

## 4) 高级格式
- 多级标题头：新增多行 `##var`，逐层填写子字段名以限定子数据列范围
- 多行结构列表：字段名写 `*field`，表示该字段跨多行读入（可嵌套）
- 限定列格式：用子标题精确限定；多态/可空 bean 常用 `$type`；map 多行常用 `$key`
- 紧凑格式：对非原子数据可用 `#format=json/lua/lite/stream` 指定解析格式
- `sep` 分割：在单元格内用分隔符填写复合数据（可在类型 tag 中指定，如 `list#sep=|`）

## 5) 枚举（enum）
- 普通 enum：可填枚举项名/别名/整数值
- `flags=true`（或等价配置）：支持位标志组合（如 `A|B`）；分隔符可由 enum 的 `sep` 指定
- 列限定 flags：以枚举项作为子标题列名，非 0/非空表示包含该标志位

## 6) Bean（结构体）
- `parent`：继承父类（多态）；`alias`：类型别名；`sep`：默认分隔符
- 非多态 bean：在字段列范围内按顺序填子字段
- 多态 bean：流式格式下先填具体类型名/别名，再填其字段；限定列格式下用 `$type`
- 可空 bean：空值用 `null`；非空可用 `{}` 作为“非空起始标记”（随后按顺序填写）

## 7) 数据 tag（记录级）
- Excel：在**数据行第 1 列**填写 tag（例如 `dev`、`test`）；字段值从第 2 列开始对齐
- 特殊 tag：
  - `##`：永久注释（永不导出）
  - `unchecked`：校验器不检查该记录
- 命令行可用 `--excludeTag dev` / `--includeTag xxx` 过滤导出
"""

    examples_md = """\
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
"""

    readme_md = """\
# Skill: luban-excel-editor

描述：专门用于编辑 Luban Excel 格式配置表的 Skill

文件说明：
- system.md：对助手的工作指令
- knowledge.md：Luban Excel 关键规则与易错点摘要
- examples.md：可复制的 Markdown 表格示例
"""

    return SkillFiles(system_md=system_md, knowledge_md=knowledge_md, examples_md=examples_md, readme_md=readme_md)


def main() -> None:
    parser = argparse.ArgumentParser(prog="skill-creator", description="Create a local Skill folder (simple format).")
    parser.add_argument("--out", required=True, help="Output directory for the skill.")
    parser.add_argument("--name", required=True, help="Skill name.")
    parser.add_argument("--description", required=True, help="Skill description.")
    parser.add_argument("--language", default="zh-CN", help="Skill language tag (default: zh-CN).")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument(
        "--template",
        default="luban-excel-editor",
        help="Built-in template to use (default: luban-excel-editor).",
    )
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.template != "luban-excel-editor":
        raise SystemExit(f"Unknown template: {args.template}")

    files = build_luban_excel_editor_files()

    meta = {
        "schema_version": 1,
        "name": args.name,
        "description": args.description,
        "language": args.language,
        "created_at": date.today().isoformat(),
        "files": {
            "system": "system.md",
            "knowledge": "knowledge.md",
            "examples": "examples.md",
            "readme": "README.md",
        },
    }

    _write_json(out_dir / "skill.json", meta, force=args.force)
    _write_text(out_dir / "system.md", files.system_md, force=args.force)
    _write_text(out_dir / "knowledge.md", files.knowledge_md, force=args.force)
    _write_text(out_dir / "examples.md", files.examples_md, force=args.force)
    _write_text(out_dir / "README.md", files.readme_md, force=args.force)

    print(f"OK: wrote skill to {out_dir}")


if __name__ == "__main__":
    main()

