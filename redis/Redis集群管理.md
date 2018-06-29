# Redis集群管理

[TOC]

## 1. 命令行登录及集群指令

```sh
redis-cli -c -p 7000
```

```sh
//集群(cluster)  
CLUSTER INFO 打印集群的信息  
CLUSTER NODES 列出集群当前已知的所有节点（node），以及这些节点的相关信息。   
  
//节点(node)  
CLUSTER MEET <ip> <port> 将 ip 和 port 所指定的节点添加到集群当中，让它成为集群的一份子。  
CLUSTER FORGET <node_id> 从集群中移除 node_id 指定的节点。  
CLUSTER REPLICATE <node_id> 将当前节点设置为 node_id 指定的节点的从节点。  
CLUSTER SAVECONFIG 将节点的配置文件保存到硬盘里面。   
  
//槽(slot)  
CLUSTER ADDSLOTS <slot> [slot ...] 将一个或多个槽（slot）指派（assign）给当前节点。  
CLUSTER DELSLOTS <slot> [slot ...] 移除一个或多个槽对当前节点的指派。  
CLUSTER FLUSHSLOTS 移除指派给当前节点的所有槽，让当前节点变成一个没有指派任何槽的节点。  
CLUSTER SETSLOT <slot> NODE <node_id> 将槽 slot 指派给 node_id 指定的节点，如果槽已经指派给另一个节点，那么先让另一个节点删除该槽>，然后再进行指派。  
CLUSTER SETSLOT <slot> MIGRATING <node_id> 将本节点的槽 slot 迁移到 node_id 指定的节点中。  
CLUSTER SETSLOT <slot> IMPORTING <node_id> 从 node_id 指定的节点中导入槽 slot 到本节点。  
CLUSTER SETSLOT <slot> STABLE 取消对槽 slot 的导入（import）或者迁移（migrate）。   
  
//键 (key)  
CLUSTER KEYSLOT <key> 计算键 key 应该被放置在哪个槽上。  
CLUSTER COUNTKEYSINSLOT <slot> 返回槽 slot 目前包含的键值对数量。  
CLUSTER GETKEYSINSLOT <slot> <count> 返回 count 个 slot 槽中的键。
```

## 2. 删除从节点

```sh
redis-trib.rb del-node 127.0.0.1:7004 '2aca89e16a8a0a2a68c073cfdf6e2a70b592918a'
```

## 3. 删除主节点

如果有slot，先取消分配(取消分配之前可能要fix)

```sh
redis-trib.rb reshard 192.168.56.70:7000

....

redis-trib.rb reshard 192.168.56.70:7001

....

redis-trib.rb reshard 192.168.56.70:7002
```

删除主节点

```sh
redis-trib.rb del-node 192.168.56.70:7000 '78d7e771f4f9fb87f80c2155310af6638129dae6'
redis-trib.rb del-node 192.168.56.70:7001 '68cd4872ddba23853a1ab7bb5c61dbd43b67502d'
redis-trib.rb del-node 192.168.56.70:7002 '13b3ea6eddb25bc330e422f3f729fc7e71d125a3'
```