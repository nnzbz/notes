# 1. Deepin实用技巧

[TOC]

## 1. 安装五笔输入法(存疑，再装时试试直接搜索input看看有没有Fcitx Configuration)

```sh
sudo apt remove fcitx* -y    //删除当前系统所有fcitx包
sudo apt autoremove    //自动清理所有孤立的包
sudo apt install fcitx fcitx-table-wbpy fcitx-config-gtk fcitx-frontend-all  fcitx-ui-classic fcitx-tools fcitx-ui-kimpanel
```

如果安装命令出现提示没有依赖的错误，请运行下面的指令

```sh
sudo apt --fix-broken install -f
```

最后注销再重新进来，配置输入法即可

## 2. Deepin中使用Windows字体

只需要把Windows下 `/Windows/Fonts` 文件夹复制到 Deepin下 `/usr/share/fonts/`，再把Fonts改名为winfonts 即可

## 3. 在文件管理器中修改后缀名

菜单 -> Settings -> Basic -> Open behavior -> 不要勾选 "Hide file extension when rename"

设置如下图

![修改后缀名](修改后缀名.png)
