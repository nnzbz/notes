# Deepin下安装PowerDesigner16

[TOC]

## 1. 安装 wine64

```sh
sudo apt install wine64
```

## 2. 创建一个干净的容器

```sh
WINEPREFIX=~/.deepinwine/PowerDesigner wineboot --init
```

## 3. 如果已经安装 mono，要将其卸载

```sh
WINEPREFIX=~/.deepinwine/PowerDesigner wine uninstaller --remove '{E45D8920-A758-4088-B6C6-31DBB276992E}'
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 uninstaller --remove '{E45D8920-A758-4088-B6C6-31DBB276992E}'
```

## 4. 将容器设置为 WinXP 系统

```sh
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 winecfg
```

## 5. 下载并安装 .NET Framework 4.0

```sh
wget 'http://download.microsoft.com/download/9/5/A/95A9616B-7A37-4AF6-BC36-D6EA96C8DAAE/dotNetFx40_Full_x86_x64.exe'
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 dotNetFx40_Full_x86_x64.exe /q && WINEPREFIX=~/.deepinwine/PowerDesigner wineserver -k
```

## 6. 将容器设置为 Win7 系统

```sh
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 winecfg
```

然后设置 mscoree 到 native

## 7. 下载并安装 .NET Framework 4.7.1

```sh
wget 'http://download.microsoft.com/download/9/E/6/9E63300C-0941-4B45-A0EC-0008F96DD480/NDP471-KB4033342-x86-x64-AllOS-ENU.exe'
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 NDP471-KB4033342-x86-x64-AllOS-ENU.exe /q && WINEPREFIX=~/.deepinwine/PowerDesigner wineserver -k
```

## 8. 复制字体到容器中的 `drive_c/windows/Fonts` 目录下(略)

## 9. 注册字体

新建 `font.reg` 文件，内容如下:

```ini
REGEDIT4

[HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\FontLink\SystemLink]
"Lucida Sans Unicode"="msyh.ttc"
"Microsoft Sans Serif"="msyh.ttc"
"MS Sans Serif"="msyh.ttc"
"Tahoma"="msyh.ttc"
"Tahoma Bold"="msyhbd.ttc"
"msyh"="msyh.ttc"
"Arial"="msyh.ttc"
"Arial Black"="msyh.ttc"
```

运行

```sh
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 regedit font.reg
```

## 10. 安装 PowerDesigner16

```sh
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 ~/.deepinwine/pd/pd.exe
```

## 11. 复制 crack 文件到 PowerDesigner 的安装目录(略)

## 12. 运行 PowerDesigner16

```sh
WINEPREFIX=~/.deepinwine/PowerDesigner wine64 '~/.deepinwine/PowerDesigner/drive_c/Program Files/SAP/PowerDesigner 16/PdShell16.exe'
```

