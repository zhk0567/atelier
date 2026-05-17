<!-- wiki_page_id: page-9 -->

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/config.py](https://github.com/zhk0567/NEXUS/blob/main/backend/config.py)
- [clear_tables.py](https://github.com/zhk0567/NEXUS/blob/main/clear_tables.py)
</details>

# 数据库设计

## 数据库连接配置

数据库连接通过 `backend/config.py` 文件中的 `DATABASE_URL` 配置项进行管理。该文件定义了数据库连接的详细参数，包括数据库类型、主机地址、端口、数据库名称以及认证信息。

```python
# backend/config.py
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

## 数据库表结构

根据 `clear_tables.py` 脚本的内容，可以推断数据库中存在以下表结构：

- `users`：存储用户信息
- `sessions`：存储会话数据
- `logs`：存储系统日志
- `settings`：存储系统配置

这些表通过外键关系建立关联，确保数据的一致性和完整性。

## 数据库操作

### 表清理操作

`clear_tables.py` 脚本提供了清理数据库表的功能，主要用于测试环境中的数据重置。该脚本执行以下操作：

1. 连接到数据库
2. 按照特定顺序 truncate 所有表（考虑外键约束）
3. 提交事务
4. 关闭数据库连接

```python
# clear_tables.py
import asyncio
import asyncpg

async def clear_tables():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # 按照依赖顺序清空表
        await conn.execute("TRUNCATE TABLE users, sessions, logs, settings RESTART IDENTITY CASCADE")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(clear_tables())
```

### 数据库迁移

虽然未在提供的文件中直接看到迁移脚本，但数据库设计遵循以下原则：

- 使用 PostgreSQL 作为主要数据库
- 所有表都有明确的主键
- 外键约束用于维护参照完整性
- 索引用于优化查询性能

## 数据库设计原则

1. **规范化**：数据库设计遵循第三范式（3NF），减少数据冗余
2. **性能优化**：为频繁查询的字段创建适当的索引
3. **安全性**：通过参数化查询防止SQL注入
4. **可维护性**：使用清晰的命名约定和注释

## 数据库访问层

虽然未在提供的文件中看到具体的数据访问层实现，但可以推断项目使用了以下模式：

- 异步数据库驱动（asyncpg）
- 连接池管理
- 基于上下文的连接处理
- 错误处理和重试机制

## 备份和恢复

数据库备份策略应包括：

- 定期逻辑备份（使用 pg_dump）
- 增量备份方案
- 灾难恢复演练
- 备份数据的加密存储

## 性能监控

数据库性能监控应关注：

- 查询执行时间
- 连接池使用情况
- 锁等待时间
- 缓存命中率
- 磁盘I/O使用情况

## 安全考虑

数据库安全措施包括：

- 使用强密码和定期轮换
- 最小权限原则分配数据库用户权限
- 启用SSL连接加密
- 审计登录和关键操作
- 定期安全补丁更新</details>