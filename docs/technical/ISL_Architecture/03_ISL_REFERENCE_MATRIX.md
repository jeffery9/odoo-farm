# 03_ISL_REFERENCE_MATRIX



---

## 📄 Source Document: isl_architecture_matrix.md

# ISL Architecture Cross-Industry Reusability Matrix

## Evaluation Criteria
Each model is evaluated based on the following criteria:
- **Cross-Industry Usage**: How commonly the model is used across different industries
- **Customization Needs**: Level of industry-specific customization typically required
- **Complexity**: Complexity of the model and potential for industry variations
- **ISL Suitability**: Recommendation for ISL architecture implementation

## Matrix Legend
- **CIU**: Cross-Industry Usage (1-5: 1=Very Low, 5=Very High)
- **CN**: Customization Needs (1-5: 1=Very Low, 5=Very High)
- **C**: Complexity (1-5: 1=Very Simple, 5=Very Complex)
- **ISL**: ISL Recommendation (H=High, M=Medium, L=Low, N=Not Recommended)

## Core Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `res.partner` | 5 | 2 | 2 | M | Core entity, some industry extensions |
| `res.company` | 5 | 2 | 2 | M | Basic company info with industry variations |
| `res.users` | 5 | 1 | 1 | L | Authentication - minimal industry variation |
| `uom.uom` | 5 | 3 | 2 | M | Units vary by industry needs |
| `uom.category` | 5 | 2 | 1 | L | Basic categorization |

## Sales Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `sale.order` | 5 | 4 | 4 | H | Major industry variations in workflow and fields |
| `sale.order.line` | 5 | 3 | 3 | M | Line-specific industry requirements |
| `product.template` | 5 | 5 | 4 | H | Significant industry-specific attributes |
| `product.product` | 5 | 4 | 4 | H | Product variants with industry specs |
| `product.category` | 5 | 3 | 2 | M | Categorization varies by industry |

## Purchase Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `purchase.order` | 5 | 4 | 4 | H | Procurement processes vary significantly |
| `purchase.order.line` | 5 | 3 | 3 | M | Line-level procurement rules |

## Inventory Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `stock.picking` | 5 | 4 | 4 | H | Picking processes vary by industry |
| `stock.move` | 5 | 3 | 4 | M | Movement rules by industry type |
| `stock.quant` | 5 | 2 | 3 | M | Stock tracking with some variations |
| `stock.location` | 5 | 4 | 3 | H | Location types vary significantly |
| `stock.lot` | 5 | 5 | 4 | H | Traceability requirements vary greatly |

## Manufacturing Models (High Priority for ISL)

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `mrp.production` | 4 | 5 | 5 | H | Manufacturing processes highly industry-specific |
| `mrp.bom` | 4 | 5 | 5 | H | Formulas/recipes vary dramatically by industry |
| `mrp.bom.line` | 4 | 4 | 4 | H | BOM line variations for industry |
| `mrp.workorder` | 4 | 5 | 4 | H | Work operations vary by industry |
| `mrp.routing` | 4 | 4 | 4 | M | Process routing by industry |
| `mrp.workcenter` | 4 | 5 | 4 | H | Equipment/facility types vary by industry |

## Quality Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `quality.point` | 3 | 5 | 3 | H | Quality standards vary significantly |
| `quality.check` | 3 | 5 | 4 | H | Check procedures vary by industry |
| `quality.alert` | 3 | 4 | 3 | M | Alert mechanisms by industry |

## Accounting Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `account.move` | 5 | 3 | 4 | M | Some industry-specific requirements |
| `account.account` | 5 | 4 | 3 | M | Chart of accounts by industry |
| `account.journal` | 5 | 3 | 2 | L | Basic journal types |
| `account.payment` | 5 | 2 | 3 | L | Payment processing varies less |

## HR Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `hr.employee` | 5 | 3 | 3 | M | Some industry-specific fields |
| `hr.department` | 5 | 4 | 2 | M | Department structures vary |
| `hr.job` | 5 | 4 | 3 | M | Job positions by industry |

## Project Models

| Model | CIU | CN | C | ISL | Notes |
|-------|-----|----|----|-----|--------|
| `project.project` | 4 | 4 | 4 | H | Project management varies by industry |
| `project.task` | 4 | 4 | 3 | M | Task management by industry type |

## ISL Implementation Priority

### Priority 1 (Immediate): Manufacturing Core
1. `mrp.production` - Manufacturing orders with industry-specific processes
2. `mrp.bom` - Bill of materials/formulas with industry-specific requirements
3. `mrp.workcenter` - Work centers/facilities with specialized equipment tracking
4. `stock.lot` - Lot tracking with industry-specific traceability

### Priority 2 (High): Sales & Purchase
5. `sale.order` - Sales processes with industry-specific workflows
6. `purchase.order` - Procurement with industry-specific requirements
7. `product.template` - Product definitions with industry attributes

### Priority 3 (Medium): Support Models
8. `stock.picking` - Picking with industry-specific processes
9. `mrp.workorder` - Work orders with specialized operations
10. `quality.point` - Quality control with industry standards

## ISL Architecture Guidelines

### When to Use ISL Architecture
- **High Industry Variation**: Models that require significant customization per industry
- **Complex Business Logic**: Models with complex, industry-specific workflows
- **Regulatory Compliance**: Models subject to industry-specific regulations
- **Extensive Field Customization**: Models that commonly add many industry-specific fields
- **Process Differentiation**: Models where the business process varies significantly

### When NOT to Use ISL Architecture
- **Core Infrastructure**: Authentication, basic system models
- **Simple Extensions**: Models that only need a few additional fields
- **Universal Logic**: Models with business logic that's truly universal
- **Performance Critical**: Models where inheritance might impact performance significantly

### Implementation Pattern
```
Abstract Mixins (farm.{module}.mixin) → Concrete ISL Models (farm.{module}) → Industry Extensions
```

For example:
```
farm.agri.bom.mixin (Abstract) → farm.processing.bom (Concrete ISL) → farm.livestock.bom (Industry Extension)
```

