# Datable 文档分类说明

本文档库包含了从 www.datable.cn 爬取的所有文档，已按照以下规则进行分类整理。

## 目录结构

```
datable_docs_organized/
├── zh/          # 中文文档
│   ├── beginner/        # 新手教程
│   ├── basic/           # 使用指南（索引页）
│   ├── manual/          # 使用指南（详细文档）
│   ├── help/            # FAQ
│   ├── intro/           # 介绍
│   ├── other/           # 其他文档
│   ├── 1.x/             # 1.x 版本文档
│   │   ├── beginner/
│   │   ├── basic/
│   │   ├── manual/
│   │   ├── help/
│   │   ├── intro/
│   │   └── other/
│   └── 3.x/             # 3.x 版本文档
│       ├── beginner/
│       ├── basic/
│       ├── manual/
│       ├── help/
│       ├── intro/
│       └── other/
└── en/          # 英文文档
    ├── beginner/        # Beginner Tutorial
    ├── basic/           # User Guide (index)
    ├── manual/          # User Guide (detailed)
    ├── help/            # FAQ
    ├── intro/           # Introduction
    ├── other/           # Other documents
    ├── 1.x/             # 1.x version documents
    └── 3.x/             # 3.x version documents
```

## 分类规则

### 第一层分类：语言
- **zh/** - 中文文档（URL 不包含 `/en/`）
- **en/** - 英文文档（URL 包含 `/en/`）

### 第二层分类：源网站位置
根据文档在源网站中的 URL 路径进行分类：

- **beginner/** - 新手教程 (`/docs/beginner`)
- **basic/** - 使用指南索引页 (`/docs/basic`)
- **manual/** - 使用指南详细文档 (`/docs/manual`)
- **help/** - FAQ (`/docs/help`)
- **intro/** - 介绍 (`/docs/intro`)
- **other/** - 其他文档 (`/docs/other`)
- **1.x/** - 1.x 版本特定文档 (`/docs/1.x/...`)
- **3.x/** - 3.x 版本特定文档 (`/docs/3.x/...`)

## 统计信息

### 中文文档 (zh)
- beginner: 11 个文件
- basic: 1 个文件
- manual: 27 个文件
- help: 1 个文件
- intro: 1 个文件
- other: 3 个文件
- 1.x/*: 25 个文件
- 3.x/*: 42 个文件

### 英文文档 (en)
- beginner: 11 个文件
- basic: 1 个文件
- manual: 27 个文件
- help: 1 个文件
- intro: 1 个文件
- other: 3 个文件
- 1.x/*: 25 个文件
- 3.x/*: 42 个文件

**总计：224 个文档文件**

## 文件命名

每个文件都保留了原始的文件名，已移除所有命名冲突产生的后缀。

每个文件的开头都包含了：
- 文章标题
- 来源 URL（格式：`> 来源: https://www.datable.cn/...`）

所有文档中的文件引用都已更新为不带后缀的文件名，确保链接一致性。

## 注意事项

- 部分文件可能因为文件名编码问题显示为乱码，但文件内容是正确的 UTF-8 编码
- 如果发现文件分类有误，可以根据文件中的来源 URL 手动调整

