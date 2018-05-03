# Shell解析参数

[TOC]

## 1. 原生处理

| 参数        | 说明                                         |
|:------------|:---------------------------------------------|
| $0          | ./test.sh,即命令本身，相当于C/C++中的argv[0] |
| $1,$2,$3... | 按顺序第几个参数                             |
| $#          | 参数的个数(不包括命令本身)                   |
| $@          | 参数本身的列表(不包括命令本身)               |
| $*          | 和$@相同                                     |
| "$@"        | 将所有的参数解释成一个参数数组               |
| "$*"        | 将所有的参数解释成一个字符串                 |

示例

```sh
#!/bin/bash
for arg in "$*"
do
    echo $arg
done

for arg in "$@"
do
    echo $arg
done
```

## 2. 参数传递的典型用法

| 示例                             | 用法                                                       |
|:---------------------------------|:-----------------------------------------------------------|
| ./test.sh -a -b -c               | 短选项，各选项不需参数                                     |
| ./test.sh -abc                   | 短选项，和上一种方法的效果一样，只是将所有的选项写在一起。 |
| ./test.sh -a args -b -c          | 短选项，其中-a需要参数，而-b -c不需参数。                  |
| ./test.sh --a-long=args --b-long | 长选项                                                     |

## 3. getopts

getopts是由Bash内置的命令，**不支持长选项**。

```sh
#!/bin/bash
while getopts ":a:bc" arg #第一个冒号表示忽略错误,选项后面的冒号表示该选项需要参数
do
    case $arg in
        a)
            echo "a's arg:$OPTARG" #参数存在$OPTARG中
            ;;
        b)
            echo "b"
            ;;
        c)
            echo "c"
            ;;
        ?)  #当有不认识的选项的时候arg为?
            echo "unkonw argument"
            exit 1
            ;;
    esac
done
```

## 4. getopt

getopt是C提供的独立的可执行文件，**支持长选项**。

- -o表示短选项，两个冒号表示该选项有一个可选参数，可选参数必须紧贴选项
 如-carg 而不能是-c arg
- --long表示长选项
- "$@"在上面解释过
- -n:出错时的信息
- -- ：举一个例子比较好理解：
 我们要创建一个名字为 "-f"的目录你会怎么办？
 mkdir -f #不成功，因为-f会被mkdir当作选项来解析，这时就可以使用
 mkdir -- -f 这样-f就不会被作为选项。

```sh
TEMP=`getopt -o ab:c:: --long a-long,b-long:,c-long:: \
     -n 'example.bash' -- "$@"`

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

# Note the quotes around `$TEMP': they are essential!
#set 会重新排列参数的顺序，也就是改变$1,$2...$n的值，这些值在getopt中重新排列过了
eval set -- "$TEMP"

#经过getopt的处理，下面处理具体选项。
while true ; do
    case "$1" in
        -a|--a-long) echo "Option a" ; shift ;;
        -b|--b-long) echo "Option b, argument \`$2'" ; shift 2 ;;
        -c|--c-long)
            # c has an optional argument. As we are in quoted mode,
            # an empty parameter will be generated if its optional
            # argument is not found.
            case "$2" in
                    "") echo "Option c, no argument"; shift 2 ;;
                    *)  echo "Option c, argument \`$2'" ; shift 2 ;;
            esac ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done
echo "Remaining arguments:"
for arg do
   echo '--> '"\`$arg'" ;
done
```

## 5. 总结

一般小脚本手工处理也许就够了，getopts能处理绝大多数的情况，getopt较复杂，功能也更强大。
getopt 最牛的可以提取参数，被提取的参数可以随便放位置，getopts就不行，提取参数必须放在其他的参数前面才行