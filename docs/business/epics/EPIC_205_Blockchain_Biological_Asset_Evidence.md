# EPIC 205: Blockchain-based Biological Asset Evidence
## 基于区块链的生物资产价值存证

### 1. 核心愿景 (Core Vision)
利用区块链的不可篡改性，将 [EPIC 201] 的科学数据（GDD, Biomass）与 [EPIC 203] 的物理证据（IoT Logs）转化为**“信用生物资产”**。通过对关键生长节点进行上链哈希存证，为金融估值、农业保险及 ESG 绿色认证提供不可伪造的数字化凭证。

---

### 2. 用户故事集 (User Stories)

#### **[US-205-01] 生物量价值建模 (Biological Value Modeling)**
- **描述**: 作为财务主管，我希望根据当前的生理阶段 (GDD) 和生物量 (Biomass) 实时计算在产品 (WIP) 的公允价值。
- **验收标准 (AC)**:
    - 实现 `agri.valuation.engine`，支持基于 Logistic 曲线进度的价值映射。
    - 当生理阶段从 V1 进入 R1 时，资产估值应自动按预设模型调整。

#### **[US-205-02] 关键行为哈希存证 (Evidence Hashing)**
- **描述**: 作为合规官，我希望将每一次关键的 AI 补救决策和边缘控制指令进行哈希计算，为上链做准备。
- **验收标准 (AC)**:
    - 增强 `agri.evidence.mixin`，支持对 `mrp.production` 关联的 `farm.command.log` 进行摘要计算。
    - 生成包含 (Timestamp, Operator, Action, Result Hash) 的存证数据包。

#### **[US-205-03] 异步存证分发 (Blockchain Notarization)**
- **描述**: 作为技术架构师，我希望存证过程是异步且非阻塞的，通过通讯框架下发至区块链网关。
- **验收标准 (AC)**:
    - 实现 `agri.blockchain.gateway`，支持队列化的存证请求。
    - 支持模拟上链反馈 (TxHashID) 的回写与溯源。

#### **[US-205-04] 生物资产电子证书 (Growth Certificate)**
- **描述**: 作为销售经理，我希望为每一个采收批次 (Lot) 生成一份包含全生命周期科学数据的电子证书。
- **验收标准 (AC)**:
    - 自动生成 PDF/JSON 格式的证书，包含存证节点、累计 GDD、RUE/WUE 指标及区块链验证链接。

---

### 3. 技术架构 (Technical Architecture)
- **数据源**: `farm_agri_science` (GDD), `farm_iot` (Logs), `farm_ai_decision` (Actions)。
- **核心 Mixin**: `agri.evidence.mixin` [Level 2]。
- **依赖模块**: `farm_financial_core`, `agri_iot` (作为上链通道)。

---
*V1.0 - Digital Credit Foundation | 2026-02-02*
