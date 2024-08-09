# cp system

Hazelcast 的 CP Subsystem（Consistency and Partitioning Subsystem）是一个用于提供强一致性和高可用性的功能模块。开启 CP Subsystem 的主要用途包括：

1. **强一致性**：CP Subsystem 提供了分布式数据结构的强一致性保证，确保在分布式环境中的多个节点之间的数据一致性。这对于需要严格一致性的应用场景（如金融交易、分布式锁等）非常重要。

2. **高可用性**：CP Subsystem 采用了 Raft 算法来实现数据的复制和故障恢复，确保在节点故障的情况下，系统仍然能够保持可用性并继续提供服务。

3. **分布式数据结构**：使用 CP Subsystem，您可以使用 Hazelcast 提供的分布式数据结构（如 CP Map、CP Semaphore、CP Lock 等），这些数据结构能够在多个节点之间共享并保持一致性。

4. **事务支持**：CP Subsystem 支持事务操作，可以在分布式环境中执行原子操作，确保数据的一致性和完整性。

5. **容错能力**：由于 CP Subsystem 的设计，系统能够在部分节点失效时仍然保持正常运行，保证业务连续性。

## 如何开启 CP Subsystem

要在 Hazelcast 中启用 CP Subsystem，您可以在配置文件（如  `hazelcast.xml` ）中进行设置。例如：

```xml
<hazelcast>
    <cp-subsystem>
        <!-- 如果设置为 0 与不开启是一样 -->
        <cp-member-count>3</cp-member-count>
    </cp-subsystem>
</hazelcast>
```

在上述配置中， `<cp-subsystem>`  标签中的  `<enabled>`  设置为  `true` ，表示启用 CP Subsystem。

### 注意事项

- 开启 CP Subsystem 会增加系统的复杂性和资源消耗，因此在不需要强一致性的场景下，可以考虑使用 Hazelcast 的默认数据结构和功能。
- 确保您的应用场景确实需要 CP Subsystem 提供的强一致性和高可用性特性，以便充分利用其优势。

通过启用 CP Subsystem，您可以构建更为可靠和一致的分布式应用程序，适应对一致性要求较高的业务场景。

## `cp-member-count`  的用途

在 Hazelcast 中， `cp-member-count`  配置选项用于指定应该参与 CP 子系统（一致性与分区子系统）的成员数量。这个设置对于定义 CP 数据结构正常操作所需的法定人数（quorum）至关重要。

1. **法定人数要求**： `cp-member-count`  定义了在集群中形成 CP 组所需的成员数量。这对于确保 CP 数据结构（如 CP Map、CP Lock 等）能够保持强一致性非常重要。法定人数对于领导者选举和确保大多数节点对数据状态的一致性至关重要。

2. **容错能力**：通过配置  `cp-member-count` ，您可以控制 CP 组的容错能力。例如，如果将  `cp-member-count`  设置为 3，则 CP 组可以容忍一个成员的故障（因为 3 个成员中的 2 个仍然可以形成法定人数）。

3. **集群规模**： `cp-member-count`  的值应小于或等于 Hazelcast 集群中的成员总数。如果您有一个较小的集群，可能希望将此值设置得更低，以确保即使在活动成员较少的情况下，CP 子系统仍然能够正常工作。

4. **性能考虑**：较高的  `cp-member-count`  可以提高 CP 子系统的可靠性，但也可能在操作中引入更多延迟，因为需要更多成员参与共识。根据应用程序的需求，平衡一致性的需求与性能要求非常重要。

### 示例配置

以下是如何在  `hazelcast.xml`  文件中配置  `cp-member-count`  的示例：

```xml
<hazelcast>
    <cp-subsystem>
        <!-- 如果设置为 0 与不开启是一样 -->
        <cp-member-count>3</cp-member-count>
    </cp-subsystem>
</hazelcast>
```

在这个例子中，CP 子系统被启用， `cp-member-count`  设置为 3，这意味着至少需要 3 个成员才能形成一个 CP 组。

### 总结

设置  `cp-member-count`  对于确保您的分布式应用程序能够达到所需的一致性和容错能力水平至关重要。它帮助定义维护 CP 数据结构完整性所需的成员数量，应根据您的应用程序和集群规模的具体需求进行配置。
