# thread-splitter-lite

零依赖的**长文转帖子串工具**：把一篇长文按段落和字数自动切成多条适合 X / 微博 / Threads 发布的短帖，首帖带钩子，每条带 `n/total` 编号尾注。无需任何 API。

## 功能简介

- 按段落聚合，控制每条帖子不超过设定字符上限。
- 超长段落自动在句号处断句，实在不行按字符硬切。
- 首帖自动加钩子开头（可关闭）。
- 每条帖子自动追加 `(n/total)` 编号，读者一看就知道还有几条。

## 快速开始

```bash
# 从文件读取
python3 cli.py --file long_article.txt

# 直接传文本，收紧到每条 120 字
python3 cli.py --text "第一段。第二段。" --max-len 120

# 不加钩子
python3 cli.py --file long_article.txt --no-hook
```

## 无 API key 如何运行

本项目**完全不需要 API key**，纯本地规则拆分。

## 目录说明

```
thread-splitter-lite/
├── thread_splitter.py   # 段落切分 + 聚合 + 编号钩子
├── cli.py             # 命令行入口
├── tests/
│   └── test_thread.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
