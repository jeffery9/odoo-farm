# 2026 农业系统：模型命名空间普查清单 (V1.0)

本清单通过物理扫描系统中所有 `.py` 文件的 `_name` 定义生成，旨在为“Agri-Farm 语义纠偏”提供决策依据。

## 1. Agri 域名资产 (agri.*) - 语义合规
这些模型代表了农业领域的通用标准、协议和物理规律，符合 2026 架构律令。

- **协作协议**: `agri.a2a.message`, `agri.a2a.negotiation`, `agri.a2a.protocol`, `agri.a2a.arbitrator`.
- **清算引擎**: `agri.clearing.ledger`, `agri.clearing.netting.engine`, `agri.dividend.pool`.
- **物理 Mixins**: `agri.nutrient.mixin`, `agri.geospatial.mixin`, `agri.sustainability.mixin`, `agri.evidence.mixin`.
- **核心组件**: `agri.value.bridge`, `agri.mission.orchestrator`, `agri.neighborhood.registry`, `agri.view.mixin`.

## 2. Farm 域名资产 (farm.*) - 待清算区域
目前系统中有大量本应属于领域级 (Agri) 的模型被错误地冠以了农场 (Farm) 前缀。

### 2.1 物理与生物事实 (建议迁移至 agri.*)
- `farm.location` (地块)
- `farm.soil.analysis` (土质分析)
- `farm.biological.asset` (生物资产)
- `farm.growth.curve` (生长曲线)
- `farm.biodiversity.metric` (生物多样性)

### 2.2 作业与行业标准 (建议迁移至 agri.*)
- `farm.task`, `farm.activity` (作业单元)
- `farm.industry.variety` (品种标准)
- `farm.industry.physio.stage` (物候期标准)
- `farm.industry.uom.conversion` (行业单位换算)

### 2.3 真正的 Farm 资产 (建议保留 farm.*)
- `farm.agritourism.operation` (农旅经营)
- `farm.csa.subscription` (CSA 订阅)
- `farm.hr` (农场员工与计件)
- `farm.shared.tool` (农场间共享工具)

## 3. AI 域名资产 (ai.*) - 待归口
碎片化的 AI 命名，建议统一为 `agri.ai.*`。

- `ai.agent`, `ai.decision.engine`, `ai.model.registry`, `ai.coordination.layer`.
- `ai.harvest.timing`, `ai.fertilization.decision`, `ai.pest.disease.detection`.

## 4. 技术底层与遗留系统 (Others)
- `iiot.device.*`: 物联网底层。
- `isl.*`: 行业标准层技术。
- `stock.lot`, `purchase.order`: Odoo 原生扩展。

## 5. 重构律令 (2026)
1. **Agri 优先**: 只要逻辑在林业、水产、菌物中通用，必须使用 `agri.` 前缀。
2. **存量重定向**: 对于现有的 `farm.location` 等核心模型，采用“物理保留、逻辑代理”的方式逐步向 `agri.` 语义靠拢。
3. **新增禁令**: 严禁再创建包含物理事实的 `farm.*` 模型。

---
*普查时间：2026-01-31*
