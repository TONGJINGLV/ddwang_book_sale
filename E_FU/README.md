# ddwang_book_sale

## version2:

**更新时间**：2019-12-29 20:25:00

**更新内容**：

1. builddb.sql中新增Order_表的address字段。

## version1：

**更新时间**：2019-12-28 13:00:00

**更新内容**：

1. 目前确定的逻辑结构及解释（逻辑结构.md）
2. 关于数据库使用者的角色说明，及各角色对应可能需实现的功能（角色.md）
3. 建表命令（builddb.sql）
4. 建表所需的初始数据（data.zip）
5. 本文件（README）



### 逻辑结构

​	该文件解释了现有哪些表，以及为何如此建表。

### 角色

​	该文件从使用者的角度来看，为前端功能的种类和逻辑提供了一些拟解决方案。

### builddb

​	使用该文件建立数据库。使用方法有：

1. 拷贝文件中命令在mysql的终端执行。
2. 在builddb.sql的目录下进入mysql终端，并执行source('builddb.sql')，或任意目录下，source时使用绝对路径。

### 推荐阅读顺序

​	逻辑结构（5min）-> 角色（10min）-> 执行builddb.sql

## version0：

* 撰写数据库设计文档
* 数据库实施（数据，嵌入django.bookstore.models）
