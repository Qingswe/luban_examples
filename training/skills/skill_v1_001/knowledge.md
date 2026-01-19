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
