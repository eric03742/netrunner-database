# netrunner-database

*《矩阵潜袭》数据库生成工具*

## 简介

`netrunner-database` 是用于生成《矩阵潜袭》中文卡牌数据库并以 SQLite 数据库为载体保存的工具。

## 使用

生成数据库表结构：

```shell
npm run migrate
```

更新数据库数据：

```shell
npm run build:release
npm run start
```

## 数据源

卡牌数据来自 [NetrunnerDB](https://netrunnerdb.com/) API，中文文本数据来自 [NetrunnerCN/netrunner-card-text-Chinese](https://github.com/NetrunnerCN/netrunner-card-text-Chinese)。

本仓库及其开发者与 Fantasy Flight Games、Wizards of the Coast、Null Signal Games、NetrunnerDB 均无关联。

## 许可证

[MIT](./LICENSE)

## 作者

[Eric03742](https://github.com/eric03742)
