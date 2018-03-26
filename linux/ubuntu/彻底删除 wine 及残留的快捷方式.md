# ubuntu 彻底删除 wine 及残留的快捷方式

wine很恶心的一个地方就是，你卸载了wine，但是你安装过的wine程序快捷方式还残留在你的主菜单里边，太蛋疼了，现在教你怎么彻底删掉wine：

1.卸载wine主程序，在终端里输入：

```sh
sudo apt-get remove --purge wine
```

2.然后删除wine的目录文件：

```sh
rm -r ~/.wine
```

3.卸载残留不用的软件包：

```sh
sudo apt-get autoremove
```

但我们在用wine卸载一些windows程序后，在“应用程序”-“其它”菜单里还残留着它的图标，我们可以通过以下方式把它彻底清除掉：

1.将 ~/.local/share/applications/ 下的相关文件或目录删除掉。

```sh
rm -r ~/.local/share/applications
```

2.删除 
~/.config/menus/applications-merged/ 里面相关的文件。

```sh
rm -r ~/.config/menus/applications-merged/wine*
```