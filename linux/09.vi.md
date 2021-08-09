# vi与vim

[TOC]

## 1. 安装与配置

### 1.1. Mac

#### 1.1.1. 乱码

复制中文过来发现乱码

```sh
vi ~/.vimrc
```

```ini
set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936
set termencoding=utf-8
set encoding=utf-8
```

```sh
. ~/.vimrc
```

### 1.2. CentOS

#### 1.2.1. 安装增强版的vim

```sh
yum -y install vim-enhanced
```

#### 1.2.2. 配置彩色显示文本

```sh
vi /etc/bashrc
```

```text
alias vi='vim'
```

```sh
source /etc/bashrc
```

### 1.3. Ubuntu

#### 1.3.1. 安装vim

```sh
apt install vim
```

#### 1.3.2. 设置语法高亮及行号等

```ini
syntax on
set tabstop=4
set softtabstop=4
set shiftwidth=4
set autoindent
set nu
colorscheme desert
```

```sh
# 设置语法高亮
sed -i '$a\syntax on' /etc/vim/vimrc
# 设置制表符宽度为4
sed -i '$a\set tabstop=4' /etc/vim/vimrc
# 设置软制表符宽度为4
sed -i '$a\set softtabstop=4' /etc/vim/vimrc
# 设置缩进的空格数为4
sed -i '$a\set shiftwidth=4' /etc/vim/vimrc
# 设置自动缩进
sed -i '$a\set autoindent' /etc/vim/vimrc
# 在左侧显示文本的行号
sed -i '$a\set nu' /etc/vim/vimrc
```

#### 1.3.3. 方向键及退格键乱码的问题

```sh
sed -i 's/set compatible/set nocompatible/' /etc/vim/vimrc.tiny
sed -i '/set nocompatible/a\set backspace=2' /etc/vim/vimrc.tiny
```

### 1.4. 配置主题

CentOS/MAC下测试通过

```sh
vi ~/.vimrc
```

MAC下一定要有第二句，CentOS可以没有

```text
colorscheme desert
syntax on
```

还有一些主题可以查找vim运行目录的colors目录下以 ```.vim``` 结尾的文件

BTW：如何知道vim运行目录？运行vim，输入指令 ```:echo $VIMRUNTIME``` 即可查到，我的为 ```/usr/share/vim/vim74``` 。

比较经典的主题还有: darkbule,elflord,koehler,slate,zellner

## 2. 保存

没有权限保存文件

```sh
:w !sudo tee %
```

## 3. 快速移动光标

| 操作       | 快捷键 |
|:-----------|:-------|
| 文首       | gg     |
| 文尾       | G      |
| 行首       | 数字0  |
| 行尾       | $      |
| 向上翻页   | ctrl+b |
| 向下翻页   | ctrl+f |
| 向上翻半页 | ctrl+u |
| 向下翻半页 | ctrl+d |

## 4. 撤销与重做

| 操作               | 快捷键 |
|:-------------------|:-------|
| 撤销操作           | u      |
| 撤销所有操作回原状 | 两次u  |
| 重做               | ctrl+r |

## 5. 查找

### 5.1. 向下查找

```sh
/pattern<Enter>
```

### 5.2. 向上查找

```sh
?pattern<Enter>
```

### 5.3. 查找下一个

使用了查找命令之后，使用如下两个键快速查找：

- n：按照同一方向继续查找
- N：按照反方向查找

### 5.4. 正则表达式

pattern是需要匹配的字符串的正则表达式，例如：

```sh
/abc<Enter>      #查找abc
/ abc <Enter>    #查找abc单词（注意前后的空格）
/^abc<Enter>     #查找以abc开始的行
/test$<Enter>    #查找以abc结束的行
//^test<Enter>   #查找^tabc字符串
```

**正则表达式中的“/”为转义字符**


## 6. 替换

基本替换 

1:  :s/vivian/sky/         #替换当前行第一个 vivian 为 sky
2:  :s/vivian/sky/g     #替换当前行所有 vivian 为 sky
3:  :n,$s/vivian/sky/     #替换第 n 行开始到最后一行中每一行的第一个 vivian 为 sky
4:  :n,$s/vivian/sky/g     #替换第 n 行开始到最后一行中每一行所有 vivian 为 sky
5:  （n 为数字，若 n 为 .，表示从当前行开始到最后一行）
6:  
7:  :%s/vivian/sky/        #（等同于 :g/vivian/s//sky/） 替换每一行的第一个 vivian 为 sky
8:  :%s/vivian/sky/g    #（等同于 :g/vivian/s//sky/g） 替换每一行中所有 vivian 为 sky
  可以使用 #或+ 作为分隔符，此时中间出现的 / 不会作为分隔符 

1:  :s#vivian/#sky/#         替换当前行第一个 vivian/ 为 sky/
2:  :%s+/oradata/apras/+/user01/apras1+ （
3:  使用+ 来 替换 / ）： /oradata/apras/替换成/user01/apras1/
  
删除文本中的^M 

问题描述：对于换行，window下用回车换行（0A0D）来表示，Linux下是回车（0A）来表示。这样，将window上的文件拷到unix上用时，总会有个^M，请写个用在unix下的过滤windows文件的换行符（0D）的shell或c程序。 
使用命令：cat filename1 | tr -d “^V^M” > newfile; 
使用命令：sed -e “s/^V^M//” filename > outputfilename 
需要注意的是在1、2两种方法中，^V和^M指的是Ctrl+V和Ctrl+M。你必须要手工进行输入，而不是粘贴。 
在vi中处理：首先使用vi打开文件，然后按ESC键，接着输入命令：

1:  :%s/^V^M//
2:  :%s/^M$//g
如果上述方法无用，则正确的解决办法是：

1:  tr -d “/r” < src >dest
2:  tr -d “/015″ dest
3:  
4:  strings A>B
  
其它用法 

1:  :s/str1/str2/          #用字符串 str2 替换行中首次出现的字符串 str1
2:  :s/str1/str2/g         #用字符串 str2 替换行中所有出现的字符串 str1
3:  :.,$ s/str1/str2/g     #用字符串 str2 替换正文当前行到末尾所有出现的字符串 str1
4:  :1,$ s/str1/str2/g     #用字符串 str2 替换正文中所有出现的字符串 str1
5:  :g/str1/s//str2/g      #功能同上
从上述替换命令可以看到： 
g 放在命令末尾，表示对指定行的搜索字符串的每次出现进行替换；不加 g，表示只对指定行的搜索字符串的首次出现进行替换； 
g 放在命令开头，表示对正文中所有包含搜索字符串的行进行替换操作。 
也就是说命令的开始可以添加影响的行，如果为g表示对所有行；命令的结尾可以使用g来表示是否对每一行的所有字符串都有影响。 

三、简单的vim正则表达式规则 

在vim中有四种表达式规则： 
magic(/m)：除了$.*^之外其他元字符都要加反斜杠 
nomagic(/M)：除了$^之外其他元字符都要加反斜杠 
/v（即 very magic 之意）：任何元字符都不用加反斜杠 
/V（即 very nomagic 之意）：任何元字符都必须加反斜杠 

vim默认使用magic设置，这个设置也可以在正则表达式中通过 /m /M /v /V开关临时切换。例如：

1:  //m.*          # 查找任意字符串
2:  //M.*          # 查找字符串 .* （点号后面跟个星号）
3:  
4:  //v(a.c){3}$   # 查找行尾的abcaccadc
5:  //m(a.c){3}$   # 查找行尾的(abc){3}
6:  //M(a.c){3}$   # 查找行尾的(a.c){3}
7:  //V(a.c){3}$   # 查找任意位置的(a.c){3}$
推荐使用默认的magic设置，在这种情况下，常用的匹配有：

 1:  //<abc          #查找以test开始的字符串 
 2:  /abc/>          #查找以test结束的字符串 
 3:  
 4:  $       匹配一行的结束
 5:  ^       匹配一行的开始
 6:  /<      匹配一个单词的开始，例如//<abc<Enter>:查找以abc开始的字符串
 7:  />      匹配一个单词的结束，例如/abc/><Enter>:查找以abc结束的字符串 
 8:  
 9:  *       匹配0或多次
10:  /+      匹配1或多次
11:  /=      匹配0或1次
12:  
13:  .        匹配除换行符以外任意字符    
14:  /a      匹配一个字符
15:  /d      匹配任一数字      
16:  /u      匹配任一大写字母
17:  
18:  []      匹配范围，如t[abcd]s 匹配tas tbs tcs tds
19:  /{}     重复次数，如a/{3,5} 匹配3~5个a
20:  /( /)   定义重复组，如a/(xy/)b 匹配ab axyb axyxyb axyxyxyb ...
21:  /|      或，如：for/|bar 表示匹配for或者bar
22:  
23:  /%20c   匹配第20列
24:  /%20l   匹配第20行
关于正则表达式的详细信息，请参见参考文献。