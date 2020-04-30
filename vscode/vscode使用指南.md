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
| Prettier                  |                               |

## 2. 配置

### 2.1. Markdown

- 对齐表格
  默认中英文混合是对不齐表格的，需设置Mono字体(推荐更纱字体<https://github.com/be5invis/Sarasa-Gothic>，下载release和ttf文件并解压到/usr/share/fonts/sarasa目录下)
  `Settings` > `Editor: Font Family` > 开头加上 `'Sarasa Mono SC', ...`

## 3. 插件配置

### 3.1. GitLens

- 解决每次 `push` 都要输入用户名和密码的问题

```sh
git config --global credential.helper store
```

不要忘记重启VsCode

### 3.2. Markdown Preview Enhanced

- 解决预览的字体问题
编辑 `/home/zbz/.vscode/extensions/shd101wyy.markdown-preview-enhanced-0.5.3/node_modules/@shd101wyy/mume/styles/preview.css` 文件，查找 `.preview-container .mume[for="preview"] {......}`， 在省略号里面的开头添加 `font-family:'Microsoft YaHei';`

### 3.3. Markdown TOC

- 解决生成目录时连文章标题也算是一级的问题
`File` -> `Preferences` - `Settings` -> 选择 `Workspace` Tab标签 -> 在左边的树节点中选择 `Extensions`-`Markdown TOC configuration` 节点 -> `Depth From` 设置 `2`
