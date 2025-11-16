# vscode 使用指南

[TOC]

## 1. 推荐插件列表

| 插件名称                  | 插件说明                               |
| ------------------------- | -------------------------------------- |
| Eclipse Keymap            | 让 vscode 和 Eclipse 的快捷键          |
| GitLens                   | 增强对 GIT 的支持                      |
| Markdown All in One       | 增强对 Markdown 的支持                 |
| Markdown Preview Enhanced | 可预览 Markdown 文件                   |
| Markdown TOC              | 增强对 Markdown 中 TOC 语法的支持      |
| markdownlint              | Markdown 语法检查                      |
| Open In Default Browser   | 在浏览器中打开 html 文件               |
| Prettier                  | 格式化工具                             |
| ESLint                    | 检查 es 代码                           |
| Prettier ESLint           | 根据 prettier 定义的 eslint 规则       |
| TSLint                    | 检查 typescript 代码                   |
| Auto Close Tag            | 自动闭合标签                           |
| Auto Rename Tag           | 自动对前后标签重命名                   |
| Path Intellisense         | 可以让 Vue 智能支持@开头的路径(要配置) |

- Path Intellisense 配置让 Vue 智能支持@开头的路径(要配置)
  在 settings.json 中加入
  ```json
  {
    ....
    "path-intellisense.mappings": {
      "@": "${workspaceFolder}/src"
    },
    "path-intellisense.autoSlashAfterDirectory": true
    ....
  }
  ```

## 2. 配置

### 2.1. 换行符

`[Settings]` -> 搜索 `eof` -> 设置 `"prettier.endOfLine": "lf"`

### 2.2. Markdown

- 对齐表格
  默认中英文混合是对不齐表格的，需设置 Mono 字体(推荐更纱字体<https://github.com/be5invis/Sarasa-Gothic>，下载 release 和 ttf 文件并解压到/usr/share/fonts/sarasa 目录下)
  `Settings` > `Editor: Font Family` > 开头加上 `'Sarasa Mono SC', ...`

## 3. 插件配置

### 3.1. GitLens

- 解决每次 `push` 都要输入用户名和密码的问题

```sh
git config --global credential.helper store
```

不要忘记重启 VsCode

### 3.2. Markdown Preview Enhanced

- 解决预览的字体问题
  编辑 `~/.vscode/extensions/shd101wyy.markdown-preview-enhanced-0.5.3/node_modules/@shd101wyy/mume/styles/preview.css` 文件，查找 `.preview-container .mume[for="preview"] {......}`， 在省略号里面的开头添加 `font-family:'Microsoft YaHei';`
  最好使用等宽字体，如更纱字体(sarasa mono)

### 3.3. Markdown TOC

- 解决生成目录时连文章标题也算是一级的问题
  `File` -> `Preferences` - `Settings` -> 选择 `Workspace` Tab 标签 -> 在左边的树节点中选择 `Extensions`-`Markdown TOC configuration` 节点 -> `Depth From` 设置 `2`
