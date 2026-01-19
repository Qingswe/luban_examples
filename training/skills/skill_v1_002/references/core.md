# Luban Excel 核心速查（v2）

## 1) 标题头关键行

- `##var`：字段定义行（可以有多行表示多级标题头/嵌套字段）。
- `##type`：类型定义行（必须与 `##var` 每列对齐）。
- `##group`：导出分组行：`c`(客户端) `s`(服务器) `c,s`(双端)，留空表示所有分组都导出。
- `##`：注释行（不导出）。常用来放中文列名/说明。
- 纵表：A1 可为 `##column#var` 或 `##vertical#var`（一行一个字段/记录）。

## 2) 类型系统（Excel 里写法）

- 基础类型：`bool byte short int long float double string datetime`
- 容器类型（注意逗号）：`array,T` `list,T` `set,T` `map,K,V`
  - 例：`list,int`、`set,string`、`map,int,string`
- 可空：`T?`（例：`int?`、`string?`、`Item?`），空值用 `null`
  - `""` 是空字符串，不等同于 `null`
- 自定义：`enum`、`bean`（可继承/多态）

## 3) 记录 tag（常见约定）

当启用记录级 tag 时：
- 数据行第 1 列写 tag（如 `dev/test`）；字段值从第 2 列开始对齐
- `##` 作为 tag：永久注释记录（永不导出）
- 常见导出过滤：命令行 `--excludeTag dev` / `--includeTag xxx`

## 4) 高级特性速记

- 多级标题头：多行 `##var`，用子字段名限定列范围（适合多态/限定列）。
- 多行结构：字段名写 `*field`，表示该字段可以跨多行填写（常见于 list 的追加行）。
- 多态 bean：
  - 流式：bean 的第一个格填具体类型名/别名，后面按字段顺序填
  - 限定列：用 `$type` 子列明确类型
- `sep`：在单元格内用分隔符填写复合数据；通常写在类型 tag：`list#sep=|,int`
- `format`：紧凑格式（`stream/lite/json/lua`）通常写在字段/类型 tag 中

