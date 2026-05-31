# 4层扁平化宏观架构 (4-Layer Macro Architecture)

*版本: V1.1 | 日期: 2026-05-31 | 状态: Mandatory Enforcement (2026 Refactored)*

## 1. 设计初衷 (Design Purpose)
为了解决 Odoo 模块系统在超大规模（100+ 模块）开发中极易产生的“深层依赖污染”和“业务逻辑耦合”问题，本项目强制执行 4 层扁平化架构设计。该设计旨在实现**生产执行**、**价值流转**与**智能网关**的物理隔离。

---

## 2. 架构层级定义 (Layer Definitions)

### 🌿 Layer 0: 基础设施底座层 (Foundation)
- **定位**: 整个生态的物理根基，不包含任何具体的农产品或商业逻辑。
- **职责**: 定义地理空间 (GIS)、物理资产容器 (Locations)、IoT 基础通信协议及全站统一的“去工业化”UX。
- **代表模块**: `farm_core`, `agri_iot`, `farm_ux`。

### ⚙️ Layer 1: 算法与核心引擎层 (Core Engines)
- **定位**: 提供通用的农业科学计算与制造管理算法。
- **职责**: 计算积温 (GDD)、土壤养分平衡、ISA-88 精密控制逻辑、碳排放因子计算等。
- **代表模块**: `farm_agri_science`, `farm_supply`, `farm_operation`。

### 🌾 Layer 2: 垂直行业应用层 (Industry Apps)
- **定位**: 实现具体的、端到端的农业生产闭环。
- **职责**: 种植管理、畜牧养殖、水产、农产品深加工。
- **🚫 核心红线 (The Red Line)**: **Layer 2 内部模块之间严禁横向相互依赖**。畜牧模块绝不能 `depends` 种植模块。

### 💰 Layer 3: 商业价值与顶层智能 (Value & Intelligence)
- **定位**: 跨越农场边界的价值锚定与资金流转。
- **职责**: 农产品联采、CSA、农业金融保险、多智能体协同、出口合规。
- **代表模块**: `farm_financial_insurance`, `farm_multi_farm`, `farm_ai`, `farm_esg_compliance`。

---

## 3. 依赖规则 (Dependency Rules)
1. **单向向下**: 模块只能依赖同层级或更低层级的模块。
2. **严禁反向**: 底层 (L0/L1) 绝对禁止依赖上层 (L3)。
3. **隔离解耦**: L2 行业应用必须能够独立安装与运行，不因其他垂直行业的缺失而报错。

## 4. 实施要求 (Implementation)
- 任何新模块的 `__manifest__.py` 必须在说明中注明其所属的 **Layer**。
- `test_unit_core.py` 必须验证该模块在其层级内的隔离性。
