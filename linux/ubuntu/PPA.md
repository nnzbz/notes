# PPA

[TOC]

## 1. PPA 简介

- 含义
个人软件包存档(Personal Package Archive)。
- 为什么使用PPA
  - Ubuntu 不会立即提供该新版本的软件。需要一个步骤来检查此新版本的软件是否与系统兼容，从而可以确保系统的稳定性。假设有人开发了一款软件，并希望 Ubuntu 将该软件包含在官方软件仓库中。在 Ubuntu 做出决定并将其包含在官方存软件仓库之前，还需要几个月的时间。
  - 另一种情况是在 beta 测试阶段。即使官方软件仓库中提供了稳定版本的软件，软件开发人员也可能希望某些终端用户测试他们即将发布的版本。

## 2. PPA 列表文件的位置

`/etc/apt/sources.list`

PPA 创建了单独的 `sources.list` 文件，避免不会和原始的 `sources.list` 文件弄混，也有助于移除 PPA
