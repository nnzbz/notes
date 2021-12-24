# SELinux入门

[TOC]

## 1. 简介

- SELinux 是什么
  `Security-Enhanced Linux` 简称 SELinux，它是一个 Linux 内核模块，也是 Linux 的一个安全子系统
- 来源
  由美国国家安全局开发。2.6 及以上版本的 Linux 内核都已经集成了 SELinux 模块
- 作用
  就是最大限度地减小系统中服务进程可访问的资源（最小权限原则）

## 2. 权限

### 2.1. DAC

传统控制权限的机制是：用户是否对某个资源拥有对应权限（**读、写、执行**）
这种机制的主体是 **用户** ，被称为自主访问控制（**DAC**）

缺点:

- 只要访问这个资源的进程符合以上的条件就可以被访问
- 更致命的是，root 用户不受任何管制，系统上任何资源都可以无限制地访问

### 2.2. MAC

启用了 SELinux 后，除了需要拥有传统的权限外，还需要判断进程的类型是否拥有对资源的访问权限
这种机制的主体是 **进程**，也称为强制访问控制（**MAC**）

MAC 分为两种模式

- 类别安全（MCS）模式
- 多级安全（MLS）模式

### 2.3. DAC 和 MAC 对比

![DAC和MAC对比图](DAC和MAC对比图.jpg)

可以看到，在 DAC 模式下，只要相应目录有相应用户的权限，就可以被访问。而在 MAC 模式下，还要受进程允许访问目录范围的限制

## 3. MAC中的概念

### 3.1. 主体（Subject）

在MAC中，主体就是进程。

### 3.2. 目标（Object）

被主体访问的资源。可以是文件、目录、端口、设备等。

### 3.3. 策略和规则（Policy & Rule）

- 策略可以在 `/etc/selinux/config` 中设定
- 策略决定哪些进程需要管制、要怎么管制
- 一套策略里面有多个规则
- 规则是模块化、可扩展的。在安装新的应用程序时，应用程序可通过添加新的模块来添加规则。用户也可以手动地增减规则
- 部分规则可以按照需求启用或禁用（这种类型的规则称为布尔型规则）

CentOS 7 系统中，有三套策略，分别是：

- targeted(**默认**)
  对大部分网络服务进程进行管制
- minimum
  以 `targeted` 为基础，仅对选定的网络服务进程进行管制。一般不用
- mls
  多级安全保护。对所有的进程进行管制。这是最严格的策略，配置难度非常大。一般不用，除非对安全性有极高的要求

### 3.4. 安全上下文（Security Context）

主体要存取目标，经过策略规则判断后，还需要主体与目标的安全上下文一致才行

## 4. 安全上下文（Security Context）

### 4.1. 格式

安全上下文为一个**字符串**，用3个 `:` 隔开，分为 **4** 个部分，例如: `system_u:object_r:admin_home_t:s0`

| Identify | Role | Domain/Type | .... |
| :------- | ---- | ----------- | ---- |
| 身份识别 | 角色 | 领域/类型   | .... |

### 4.2. 意义

- 身份识别 （Identify）: 相当于帐号方面的身份识别
  - unconfined_u：不受限的用户，也就是说，该文件来自于不受限的程序所产生的！一般来说，我们使用可登陆帐号来取得 bash 之后， 默认的 bash 环境是不受 SELinux 管制的～因为 bash 并不是什么特别的网络服务！因此，在这个不受 SELinux 所限制的 bash 程序所产生的文件， 其身份识别大多就是 unconfined_u 这个“不受限”用户
  - system_u：系统用户，大部分就是系统自己产生的文件
- 角色 （Role）: 说明是主体、目标还是使用者
  - object_r：目标
  - system_r: 进程或使用者
- 领域/类型 （Domain/Type）:
  - 在默认的 `targeted` 策略中， `Identify` 与 `Role` 字段基本上是不重要的！重要的在于这个类型 （type） 字段！
    - domain：在主体上称为领域 （domain）
    - type：在目标上称为类型 （Type）
  - `Domain` 需要与 `Type` 搭配，则该主体才能存取目标

### 4.3. 查看

```sh
# 查看主体的安全上下文
ps -eZ
# 查看目标的安全上下文
ls -Z
```

## 5. SELinux的运行模式

### 5.1. SELinux的三种模式

- enforcing
  强制模式。违反 SELinux 规则的行为将被阻止并记录到日志中
- permissive
  宽容模式。违反 SELinux 规则的行为只会记录到日志中。一般为调试用
- disabled
  禁用

### 5.2. 开启和禁用

```sh
vi /etc/selinux/config
```

默认情况下会看到

```ini
....
SELINUX=disabled
....
```

将 `disabled` 修改为  `enforcing` 或 `permissive`，`reboot` **重启操作系统**

**注意**:

- 如果模式从 `enforcing` / `permissive` 改变为 `disabled` 需要重新启动才能生效，反之亦然

为什么要重启操作系统?
因为 SELinux 是整合到内核中的，启用和禁用必须重启操作系统才能生效

### 5.3. 切换  `enforcing` / `permissive` 模式

```sh
# 从permissive切换到enforcing
setenforce 1
# 从enforcing切换到permissive
setenforce 0
```
