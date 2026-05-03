# 01_ISL_CORE_ARCHITECTURE



---

## 📄 Source Document: ISL_ARCHITECTURE_SUMMARY.md

# 🏛️ Odoo 农业生态系统：ISL 架构与垂直行业细分全图谱 (V6.0)

本文件汇总了系统中所有基于 **ISL (Industry Standard Layer)** 架构的实现，明确了 Odoo 标准模型、农业代理模型（Domain Models）以及垂直行业扩展之间的 `_inherits` 映射关系。

---

## 1. 行业架构总览：ISL 代理路径

系统通过 `_inherits` (代理继承) 实现了从 Odoo 标准工业模型或域模型到农业垂直细分的透明映射。

| 行业分类 (Industry) | 实现模块 (Path) | 核心代理模型 (ISL Model) | 业务职责 | 已注入的 DNA (Mixin) |
| :--- | :--- | :--- | :--- | :--- |
| **种植业 (Planting)** | `farm_field_crops` | `farm.crop.production` | 大田作物、生产季管理。 | `AgriWeatherSensitive`, `AgriAgentInstruction` |
| **生态共生 (Symbiosis)**| `farm_symbiosis` | `farm.symbiotic.order` | 稻渔/稻虾、生态拦截。 | `NutrientMixin`, `AgriQualityGate` |
| **工厂化渔业 (RAS)** | `farm_aquaculture` | `farm.ras.production` | 循环水系统、能效优化。 | `AgriResourceConsumption`, `AgriIncidentAlert` |
| **畜牧业 (Livestock)** | `farm_livestock` | `farm.lot.livestock` | 个体档案、料肉比计算。 | `AgriBiologicalInventory`, `AgriBiologicalValuation` |
| **水产业 (Aquaculture)** | `farm_aquaculture` | `farm.lot.aquaculture` | 池塘载荷、水质联动。 | `AgriBiologicalInventory`, `AgriBiologicalValuation` |
| **酿造业 (Winery)** | `farm_winery` | `farm.winery.production` | 红酒发酵、陈酿管理。 | `AgriTraceability`, `AgriIncidentAlert` |
| **发酵业 (Ferment)**| `farm_fermentation` | `farm.fermentation.order` | 窖池酿造、年份增值。 | `AgriBiologicalValuation`, `GeoSpatialMixin` |
| **加工业 (Processing)** | `farm_processing` | `farm.processing.production` | 批次指纹、HACCP 门控。 | `AgriQualityGate` |
| **智能层 (Intelligence)**| `farm_ai_llm_integration` | `agri.llm.configuration` | AI 模型配置与架构适配。 | `AgriAiBaseMixin` |

---

## 2. 已实现的垂直行业细分详情 (Implemented Sub-sectors - Detailed)

### **A. 精密环境控制与花卉 (Precision Climate & Floriculture)**
*   **花卉与观赏园艺 (Floriculture)**
    *   *路径*：`farm_floriculture/models/flower_isl.py`
    *   *代理*：`farm.flower.order` (代理 `mrp.production`), `farm.lot.flower` (代理 `stock.lot`)
    *   *特征*：**DIF (昼夜温差) 驱动的开花诱导控制**、基于采收状态的**瓶插寿命 (Vase-life) 动态预测**、极致冷链红线拦截、**采后保鲜处理 (Preservation) 闭环**（保鲜后寿命 +3 天）。

### **B. 传统发酵、酿造与深加工 (Traditional Brewing & Refining)**
*   **传统发酵工业 (Vinegar/Soy/Baijiu)**
    *   *路径*：`farm_fermentation/models/fermentation_isl.py`
    *   *特征*：**窖池 (Pit DNA) 数字化档案**、发酵品温实时预警与主动冷却、**陈年原浆资产年化增值模型**、勾调指纹链式聚合。
*   **葡萄酒酿造 (Winery & Enology)**
    *   *路径*：`farm_winery/models/winery_isl.py`
    *   *特征*：**发酵动力学监控**（糖醇转换曲线）、橡木桶陈酿资产追踪、多级调配 DNA 聚合。
*   **火腿加工与窖藏 (Dry-Cured Ham)**
    *   *特征*：生猪批次 DNA 链式继承、**脱水率 (Weight Loss) 动态核销**、年份资产自动增值。
*   **水产加工与冷冻 (Aquatic Processing)**
    *   *特征*：**包冰率 (Glazing %) 自动核销**、速冻机中心温度强制门控、捕捞水质指纹继承。

### **C. 生态协同与工业化水产 (Eco-Symbiosis & Industrial Aquaculture)**
*   **稻渔/稻虾综合种养 (Symbiosis)**
    *   *路径*：`farm_symbiosis/models/symbiosis_isl.py`
    *   *特征*：**生态协同养分核算**（鱼粪抵扣肥力）、**高毒农药硬拦截 (Ecological Gate)**、双产物同步核销。
*   **工厂化循环水养殖 (RAS)**
    *   *路径*：`farm_aquaculture/models/ras_isl.py`
    *   *特征*：**维生系统 (LSS) 组件寿命追踪**、氨氮代谢负荷实时预测、极致能效比 (kWh/kg) 核算、水循环故障“生存模式”防御。

### **D. 基础种植、育种与畜牧 (Planting & Animal Husbandry)**
*   **商业种子产业 (Seed Industry)**：种子“四检”数字化、亲本哈希指纹、品种权 (PVP) 分销合规核验。
*   **果园与园艺 (Orchard)**：单株资产管理 (Digital Twin)、积温驱动的成熟度预测、多年生资产估值。
*   **大田作物 (Field Crops)**：变量作业 (VRA) 指令闭环、生产季驱动。
*   **家畜养殖 (Livestock)**：个体档案、FCR 与 ADG 自动计算、**休药期 (PHI) 强制门控**。

---

## 3. 已实现的 ISL 技术成就总结 (Implementation Achievements)

### **A. 双基线安全内核 (Dual Baseline)**
系统已建立 **ESG (可持续性)** 与 **HACCP (食品安全)** 双重 DNA 基线，作为非功能性需求贯穿全业态。

### **B. 订单与库存商业衔接 (Order & Inventory Bridge)**
通过 `farm_isl` 提供的自动钩子，实现了垂直行业 DNA 在商业流中的透明流转：
1.  **收货自动转型**：采购入库时，标准 `stock.lot` 自动向上转型为行业代理批次（如 `farm.lot.ham`）。
2.  **调拨硬红线**：移库确认前强制校验行业安全门控（如 PHI、冷链红线）。
3.  **销售品质锁定**：销售确认前核验行业品质指标（如 Vase-life）。

### **C. 语义去工业化**
用户界面已完全屏蔽工业术语（MO/BOM/Work Center），实现了“工业底座，农业/智能感官”的极致体验。

---

## 4. 规划中的垂直行业路线图 (Future Roadmap)

以下行业已完成架构预研，处于待实施状态：
*   **林业与木材管理 (Forestry & Timber)**：轮伐期管理、单株原木溯源、固碳核算。
*   **蚕桑丝绸 (Sericulture)**：蚕龄状态机 (Instar)、桑园与养蚕协同。
*   **城市与社区农业 (Urban Agriculture)**：立体空间映射、微型传感器接入。
*   **昆虫蛋白养殖 (Insect Farming)**：资源转化率 (BCR) 量化、生命周期加速。

---
*最后更新：2026-02-01 (V6.0 垂直细分与商业衔接全对齐版)*



---

## 📄 Source Document: ARCHITECTURE_OVERVIEW.md

# ISL Architecture: Current State and Organization

## Overview
This document provides a comprehensive overview of the current ISL (Industry Specialized Layer) architecture, including the centralized farm_isl module and industry-specific extensions, and recommendations for organization and standardization.

## Current Architecture Pattern

The current ISL architecture follows a **hybrid approach** combining centralized infrastructure with distributed specialization:

### 1. Centralized ISL Infrastructure (`farm_isl` module)
- Provides abstract base models (mixins) for common industry patterns
- Implements redirection mechanism for automatic routing
- Provides performance optimization and migration utilities
- Defines consistent architecture patterns

### 2. Industry-Specific Extensions
- `farm_processing`: Food processing specialization with artisan monitoring
- `farm_livestock`: Livestock management with breeding and health tracking
- `farm_aquaculture`: Aquaculture-specific processes
- `farm_field_crops`: Crop management specialization
- `farm_mrp`: MRP ISL extensions and redirection hooks

## Current Implementation Pattern

### A. Direct Inheritance Pattern (Processing/Livestock modules)
```python
# Industry-specific model that extends both ISL and industry mixins
class FarmProcessingBom(models.Model):
    _name = 'farm.processing.bom'
    _description = 'Farm Food Processing BOM (ISL Layer)'
    _inherit = ['farm.mrp.bom', 'farm.agri.bom.mixin']  # Inherit from centralized ISL model
```

### B. _inherits Pattern (Livestock module)
```python
# Industry-specific model using _inherits from base Odoo models
class FarmLotLivestock(models.Model):
    _name = 'farm.lot.livestock'
    _inherits = {'stock.lot': 'lot_id'}  # Direct inheritance from base model
```

### C. Redirection Integration (MRP module)
```python
# Uses centralized redirection mechanism with industry-specific logic
def _get_isl_model(self):
    parent_bom = self.bom_id
    if parent_bom:
        if parent_bom.industry_type == 'livestock':
            return 'farm.livestock.bom.line'
        elif parent_bom.industry_type == 'processing':
            return 'farm.processing.bom.line'
```

## Architecture Assessment

### ✅ **Strengths of Current Approach**
1. **Flexibility**: Industry-specific modules can add specialized functionality without affecting core ISL
2. **Modularity**: Each industry can evolve independently while maintaining ISL patterns
3. **Backward Compatibility**: Existing functionality is preserved
4. **Hybrid Benefits**: Combines centralized infrastructure with distributed specialization

### ⚠️ **Challenges with Current Approach**
1. **Architecture Consistency**: Not all modules follow the same ISL pattern
2. **Potential Duplication**: Some functionality may be duplicated across industry modules
3. **Complexity**: More complex navigation between centralized and distributed components
4. **Maintenance Overhead**: Multiple locations for ISL-related logic

## Recommendations for Organization

### 1. Hybrid Architecture Standardization
Rather than forcing a pure centralized approach, standardize the current hybrid pattern:

#### A. Centralized Foundation
- Keep core ISL infrastructure in `farm_isl` for common patterns
- Maintain abstract mixins for common industry functionality
- Keep redirection utilities centralized

#### B. Distributed Specialization Pattern
- Industry-specific modules should extend centralized ISL models using `_inherit`
- Follow consistent naming conventions: `farm.{industry}.{model}`
- Implement proper industry_type validation
- Use centralized redirection mechanism where appropriate

### 2. Improved Integration Patterns
- Use `_inherit` from centralized ISL models rather than creating parallel implementations where possible
- Ensure all industry-specific models follow the same architecture patterns
- Implement consistent security patterns across all ISL-related modules

### 3. Documentation and Guidelines
- Update integration guide to reflect the hybrid approach
- Document best practices for industry-specific extensions
- Provide clear migration paths for consistency

## Current Module Integration Status

### Well-Integrated:
- `farm_mrp`: Properly uses centralized redirection mechanism with industry-specific extensions
- `farm_isl`: Provides solid foundation with abstract models and utilities

### Needs Standardization:
- `farm_processing`: Uses direct inheritance from centralized ISL model (good approach)
- `farm_livestock`: Mix of _inherits and inheritance patterns (needs review)
- Other industry modules: Review for consistency

## Next Steps for Organization

### 1. Immediate Actions:
- Document the hybrid architecture pattern as the official approach
- Create consistency guidelines for industry-specific implementations
- Review security configurations across all ISL-related modules

### 2. Medium-Term Improvements:
- Refactor inconsistent modules to follow standardized hybrid pattern
- Improve cross-module integration and navigation
- Enhance testing of ISL functionality across modules

### 3. Long-Term Considerations:
- Evaluate if some distributed functionality should move to centralized ISL
- Consider creating industry-specific ISL submodules within farm_isl
- Implement better tooling for ISL model management

## Conclusion

The current ISL architecture represents a sophisticated hybrid approach that balances centralized infrastructure with distributed specialization. While this creates some complexity, it also provides significant flexibility for industry-specific customization. Rather than forcing a pure centralized model, the architecture should be standardize around the current hybrid approach with improved consistency and documentation.

The key to successful organization is ensuring all modules follow consistent patterns within this hybrid architecture rather than attempting to force a single approach that may not suit all use cases.



---

## 📄 Source Document: isl_architecture_recommendations.md

# ISL Architecture Recommendations & Implementation Guidelines

## Executive Summary

The Industry Specialized Layer (ISL) architecture is a proven pattern for creating extensible, industry-specific modules on top of standard Odoo models. Based on analysis of existing implementations and cross-industry reusability patterns, this document provides recommendations for ISL adoption and implementation guidelines.

## ISL Architecture Definition

The ISL architecture consists of three key components:

1. **Abstract Base Models (Mixins)**: Define common fields and business logic shared across industries
2. **Concrete ISL Models**: Use `_inherits` to extend Odoo base models while preserving compatibility
3. **Industry Extensions**: Use `_inherit` to specialize ISL models for specific industries

## Models Recommended for ISL Architecture

### Priority 1: Manufacturing Core (Implement Immediately)
| Model | Rationale |
|-------|-----------|
| `mrp.production` | Manufacturing processes vary dramatically between food processing, pharmaceuticals, chemicals, automotive, etc. |
| `mrp.bom` | Formulas, recipes, and material structures are fundamentally different across industries |
| `mrp.workcenter` | Equipment types, capacity calculations, and operational requirements differ significantly |
| `stock.lot` | Traceability, batch tracking, and compliance requirements vary greatly by industry |

### Priority 2: Business Operations (High Priority)
| Model | Rationale |
|-------|-----------|
| `sale.order` | Sales processes, compliance requirements, and document flows vary by industry |
| `purchase.order` | Procurement rules, supplier qualification, and approval processes differ |
| `product.template` | Product attributes, specifications, compliance data, and categorization vary |

### Priority 3: Support Functions (Medium Priority)
| Model | Rationale |
|-------|-----------|
| `stock.picking` | Picking processes, compliance requirements, and workflow patterns vary |
| `mrp.workorder` | Work execution, quality checks, and resource allocation differ by industry |
| `quality.point` | Quality standards, testing procedures, and compliance requirements are industry-specific |

## ISL Implementation Guidelines

### 1. Abstract Base Model (Mixin) Pattern
```python
class FarmAgriBomMixin(models.AbstractModel):
    _name = 'industry.agri.bom.mixin'
    _description = 'Industry Agnostic BOM Shared Logic'

    # Common fields and methods that apply across industries
    dilution_ratio = fields.Float("Dilution Ratio")
    max_loss_rate = fields.Float("Max Allowed Loss Rate (%)")

    def industry_hook_method(self):
        """Template method for industry-specific implementations"""
        pass
```

### 2. Concrete ISL Model Pattern
```python
class IndustryProcessingBom(models.Model):
    _name = 'industry.processing.bom'
    _description = 'Industry Processing BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}  # Preserve base Odoo functionality
    _inherit = ['industry.agri.bom.mixin']  # Include shared logic

    bom_id = fields.Many2one('mrp.bom', required=True, ondelete='cascade')

    # Industry-specific fields
    industry_type = fields.Selection([
        ('food', 'Food Processing'),
        ('pharma', 'Pharmaceutical'),
        ('chem', 'Chemical'),
    ], string='Industry Type')

    # Industry-specific methods
    def validate_industry_compliance(self):
        """Validate compliance specific to the industry"""
        pass
```

### 3. Transparent Redirection Pattern
```python
class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def get_formview_action(self, access_uid=None):
        """Redirect to ISL model for enhanced functionality"""
        res = super().get_formview_action(access_uid=access_uid)
        isl_record = self.env['industry.processing.bom'].search(
            [('bom_id', '=', self.id)], limit=1
        )
        if isl_record:
            res.update({
                'res_model': 'industry.processing.bom',
                'res_id': isl_record.id,
            })
        return res
```

### 4. Industry Extension Pattern
```python
class FoodProcessingBom(models.Model):
    _name = 'food.processing.bom'
    _description = 'Food Processing BOM'
    _inherits = {'industry.processing.bom': 'isl_bom_id'}  # Inherit from ISL model
    _inherit = ['industry.processing.bom']  # Inherit behavior

    isl_bom_id = fields.Many2one('industry.processing.bom', required=True, ondelete='cascade')

    # Food-specific fields
    haccp_required = fields.Boolean("HACCP Critical Control Point")
    allergen_controls = fields.Text("Allergen Control Measures")
```

## Implementation Process

### Phase 1: Core ISL Models
1. Create abstract base models (mixins) for each target model
2. Implement concrete ISL models using `_inherits`
3. Update base models to redirect to ISL models
4. Test compatibility with existing Odoo functionality

### Phase 2: Industry Modules
1. Create industry-specific modules (e.g., `food_processing`, `pharmaceutical`, `chemicals`)
2. Implement industry extensions using inheritance patterns
3. Add industry-specific views, workflows, and business logic
4. Test end-to-end functionality for each industry

### Phase 3: Migration & Integration
1. Migrate existing data to ISL structure
2. Ensure backward compatibility for existing modules
3. Update documentation and developer guides
4. Train development team on ISL patterns

## Benefits of ISL Architecture

### 1. Maintain Odoo Compatibility
- Preserves all standard Odoo functionality
- Uses `_inherits` to maintain foreign key relationships
- Allows seamless integration with Odoo apps

### 2. Enable Industry Specialization
- Supports complex industry-specific requirements
- Allows for regulatory compliance features
- Enables specialized business processes

### 3. Promote Code Reusability
- Abstract mixins share common logic
- Reduces code duplication across industries
- Standardizes extension patterns

### 4. Support Scalability
- New industries can be added without modifying core
- Supports complex multi-industry deployments
- Enables modular feature development

## Risks & Mitigation

### 1. Performance Impact
- **Risk**: Multiple inheritance layers may impact performance
- **Mitigation**: Optimize queries, use computed fields wisely, implement proper caching

### 2. Complexity Management
- **Risk**: Architecture becomes too complex to maintain
- **Mitigation**: Clear documentation, standardized patterns, comprehensive testing

### 3. Data Migration
- **Risk**: Migration of existing data is complex
- **Mitigation**: Phased migration approach, comprehensive backup, extensive testing

## Success Metrics

### 1. Technical Metrics
- Code reusability percentage
- Performance benchmarks vs. standard Odoo
- Module loading times
- Query execution efficiency

### 2. Business Metrics
- Time to implement new industry requirements
- Number of supported industries
- Developer productivity improvement
- User satisfaction scores

## Conclusion

The ISL architecture provides a robust foundation for supporting multiple industries on a single Odoo platform. The recommended implementation approach focuses on manufacturing core models first, as these show the greatest variation across industries and the highest need for specialization. This architecture pattern has been proven in the existing farm management system and can be extended to support a wide range of industries while maintaining Odoo compatibility.

The key to success is following the established patterns, maintaining clear abstraction layers, and ensuring proper documentation for future development teams.

