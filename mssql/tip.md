# Tip

## mssql 的 jtds 和 native 驱动有什么区别？

jTDS 和 Native 驱动是用于连接 Microsoft SQL Server 数据库的两种不同 JDBC 驱动。它们之间有几个主要区别：

1. **驱动类型**：
   - **jTDS**：是一个开源的 JDBC 驱动，基于 JDBC 3.0 规范，支持 SQL Server 和 Sybase 数据库。它是完全用 Java 编写的，因此可以在任何支持 Java 的平台上运行。
   - **Native 驱动**：通常指的是 Microsoft 提供的 JDBC 驱动（如 Microsoft JDBC Driver for SQL Server），它可能会使用本地代码（如 C++）来实现更高效的数据库连接和操作。

2. **性能**：
   - **jTDS**：由于是用 Java 编写的，性能上可能不如 Native 驱动，尤其是在处理大量数据时。
   - **Native 驱动**：通常性能更好，因为它可以利用本地代码的优势，特别是在处理复杂查询和大数据量时。

3. **功能支持**：
   - **jTDS**：支持大多数 SQL Server 功能，但可能不支持一些最新的 SQL Server 特性。
   - **Native 驱动**：通常会更快地支持 SQL Server 的新特性，因为它是由 Microsoft 开发和维护的。

4. **兼容性**：
   - **jTDS**：兼容性较好，支持较老版本的 SQL Server 和 Sybase。
   - **Native 驱动**：可能需要特定版本的 SQL Server，且对新版本的支持通常更好。

5. **使用和配置**：
   - **jTDS**：配置相对简单，适合快速开发和测试。
   - **Native 驱动**：可能需要更多的配置，尤其是在处理安全性和连接选项时。

总的来说，选择哪个驱动取决于你的具体需求，包括性能、功能支持和兼容性等方面。如果你需要使用最新的 SQL Server 特性，Native 驱动可能是更好的选择；而如果你需要一个简单、兼容性好的解决方案，jTDS 可能更适合。
