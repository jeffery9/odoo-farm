# 🛠️ Odoo 农业生态系统：开发者引导门户

> **核心提示**：本文件是项目的开发入口。详细的治理规则、维护规范及开发细则已迁移至 **[docs/governance/](./docs/governance/README.md)**。

---

## 1. 快速上手 (Quick Start)
- **了解律令**：阅读 [docs/governance/MAINTENANCE_SPEC.md](docs/governance/MAINTENANCE_SPEC.md) 中的“无损更新律令”。
- **加载上下文**：执行根目录下的 `BOOTSTRAP_PROMPT.txt`。
- **定位任务**：查阅 `docs/business/MODULE_PLAN.md` 了解模块进度。

## 2. 绝对红线：无损修改 (Lossless Update)
所有开发者（包括 AI Agent）必须遵守：
- **物理资产保护**：严禁移除 `[ISA-88]`, `[LOSSLESS]`, `[US-XXX]` 等锚点。
- **读-改-核闭环**：修改前必读全文，修改后必做 `git diff` 统计校验。
- **禁止占位符**：严禁在代码回写时使用 `# ...`。

## 3. 架构索引
- **项目宪法**：[docs/governance/MAINTENANCE_SPEC.md](docs/governance/MAINTENANCE_SPEC.md)
- **开发规范**：[docs/governance/DEVELOPMENT_CONVENTIONS.md](docs/governance/DEVELOPMENT_CONVENTIONS.md)
- **分类指南**：[docs/governance/CLASSIFICATION_GUIDELINES.md](docs/governance/CLASSIFICATION_GUIDELINES.md)

---
*V1.2 - Portal Edition | 2026-02-01*