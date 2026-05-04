# Odoo Farm: 核心治理与运维脚本中心 (Operations & Maintenance Hub)

本目录包含了用于系统升级、分支同步、代码迁移以及工业化发布的自动化脚本工具链。

## 目录结构 (Directory Structure)

### 1. `migration_tools/` (版本与架构迁移)
包含用于架构重构和 Odoo 版本升级的补丁程序：
*   `fix_batch8.sh`: 历史遗留的批量热修复脚本。
*   `fix_epic_numbering.py`: 用于文档内部序号重塑的工具。
*   `migrate_sql_constraints.py`: SQL 约束向新版迁移的工具。
*   `odoo19_api_patch.py`: 应对 Odoo 19 API 签名变更（如 `trans_export`）的自动化注入脚本。

### 2. `release_tools/` (CI/CD 与商业发布)
包含用于将 `dev` 分支纯净化并推向 `19.0` release 环境的工具：
*   `release.sh`: 基础版发版工具。
*   `enhanced_automated_release.sh`: 高级发布管道，执行诸如清理测试桩、剥离文档等纯净代码打包任务。
*   `release_config.conf`: 发布流水线配置文件。

### 3. `sync_tools/` (分支与 Git 协同)
包含用于多环境间隔离与同步的 Git 战术脚本：
*   `BRANCH_SYNC_GUIDE.md`: 分支同步战术指导规范。
*   `sync_from_clean_dev.sh`: 从稳定版本反向拉取修复。
*   `sync_from_clean_dev_isolated.sh`: 隔离式环境同步器。

---
> **警告 (WARNING)**: 执行上述脚本前，请务必阅读对应目录下的指引或 `POLICY.md`。部分脚本具备全局破坏性（如 AST 重写、Git Hard Reset），非框架维护者请勿随意调用。
