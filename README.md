# Tieba Spider - 百度贴吧爬虫

## 项目简介

本项目是一个简单的百度贴吧爬虫，可以爬取指定贴吧的帖子信息，包括帖子标题、帖子链接、帖子作者、帖子内容等信息。

出于个人需求，目前只实现了爬取图片。其他内容的爬取可以参考代码自行实现。

## 使用方法

先运行`GetTIDs.py`获取指定贴吧内的帖子ID；帖子ID保存在`output/ThreadInfos.json`和`output/tid_list.json`中。

再运行`GetPosts.py`获取帖子内容。输出将保存在`output/images/`目录下。

## 项目结构

```
.
├── README.md
├── LICENSE
├── .gitignore
├── output
    └── images/
└── src
    ├── GetPosts.py
    └── GetTIDs.py
    
```
## 项目流程

由于百度贴吧电脑网页端的反爬虫机制，本项目使用手机网页端的方式进行爬取。访问频率有所限制，使用时还请自行斟酌。

## 参考

[从百度贴吧爬取数据](https://www.cnblogs.com/hair-is-decreasing/p/18191432)