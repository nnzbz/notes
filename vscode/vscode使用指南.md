# vscode使用指南

[TOC]

## 1. 推荐插件列表

| 插件名称                  | 插件说明                      |
| ------------------------- | ----------------------------- |
| Eclipse Keymap            | 让vscode和Eclipse的快捷键     |
| GitLens                   | 增强对GIT的支持               |
| Markdown All in One       | 增强对Markdown的支持          |
| Markdown Preview Enhanced | 可预览Markdown文件            |
| Markdown TOC              | 增强对Markdown中TOC语法的支持 |
| markdownlint              | Markdown语法检查              |

## 2. 插件配置

### 2.1. Markdown Preview Enhanced

- 解决预览的字体问题
编辑 `/home/zbz/.vscode/extensions/shd101wyy.markdown-preview-enhanced-0.5.3/node_modules/@shd101wyy/mume/styles/preview.css` 文件，查找 `.preview-container .mume[for="preview"] {......}`， 在省略号里面的开头添加 `font-family:'Microsoft YaHei';`

### 2.2. Markdown TOC

- 解决生成目录时连文章标题也算是一级的问题
`File` -> `Preferences` - `Settings` -> 选择 `Workspace` Tab标签 -> 在左边的树节点中选择 `Extensions`-`Markdown TOC configuration` 节点 -> `Depth From` 设置 `2`
