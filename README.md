# netrunner-database

*《矩阵潜袭》数据库生成工具*

## 简介

`netrunner-database` 是用于生成《矩阵潜袭》中文卡牌数据库并以 SQLite 数据库为载体保存的工具。

## 使用

在使用前请确保拉取所有子仓库：

```shell
git submodule update --init
```

准备使用的目录：

```shell
npm run prepare
```

生成数据库表结构：

```shell
npm run migrate
```

更新数据库数据：

```shell
npm run build:release
npm run start
```

## 下载

你可以在 [这里](https://github.com/eric03742/netrunner-database/releases/latest/download/netrunner.sqlite) 下载最新的SQLite数据库文件。

## 数据源

卡牌数据来自 [NetrunnerDB](https://netrunnerdb.com/) API，中文文本数据来自 [netrunner-card-text-Chinese](https://github.com/eric03742/netrunner-card-text-Chinese)。

本仓库及其开发者与 Fantasy Flight Games、Wizards of the Coast、Null Signal Games、NetrunnerDB 均无关联。

## 许可证

[MIT](./LICENSE)

## 作者

[Eric03742](https://github.com/eric03742)
