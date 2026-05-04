# EPIC 028:火腿加工与窖藏工艺管理 (Dry-Cured Ham Management)
*目标：建立从鲜腿采购到窖藏分级的全全生命周期管理体系，通过脱水率动态核销与窖藏环境存证，锁定“年份火腿”的极致溢价。*

## 1. 用户故事 (User Stories)

1. **[US-028-01] 鲜腿入库与原料 DNA 继承 (Fresh Leg Intake)**：💡 待实现
    - **描述**：作为加工主管，我希望记录鲜腿的来源批次，并自动继承原始生猪的品种与饲喂指纹。
    - **验收条件**：
        - **(Logic)** 继承 `AgriTraceabilityMixin`。
        - **(Linkage)** 强制关联 `farm.lot.livestock` 批次。

2. **[US-028-02] 脱水率与重量动态核销 (Dehydration Tracking)**：💡 待实现
    - **描述**：作为窖藏师，我希望定期称重，系统自动计算失重率，并对比标准工艺曲线。
    - **验收条件**：
        - **(Math)** `Weight_Loss = (Fresh_Weight - Aged_Weight) / Fresh_Weight`。
        - **(Alert)** 若脱水过快或过慢，触发 `AgriIncidentAlertMixin`。

3. **[US-028-03] 窖藏环境门控与温湿度存证 (Cellar Environment)**：💡 待实现
    - **描述**：作为品控专员，我希望系统自动记录窖藏室的温湿度波动，并作为品质分级的输入。
    - **验收条件**：
        - **(IoT)** 集成 `industrial_iot` 遥测。
        - **(Gate)** 继承 `AgriQualityGateMixin`，环境超标时自动拦截该批次进入下一阶段。

4. **[US-028-04] 年份资产动态估值 (Vintage Asset Valuation)**：💡 待实现
    - **描述**：作为财务经理，我希望火腿价值随窖藏月份（12、24、36个月）自动更新。
    - **验收条件**：
        - **(Algorithm)** 继承 `AgriBiologicalValuationMixin` 实现时间增值模型。

## 2. 业务价值
- **金融化支撑**: 100% 透明的窖藏数据使火腿成为优质的质押融资资产。
- **品牌防伪**: 基于哈希指纹的“一腿一码”，杜绝年份造假。
- **精益生产**: 降低窖藏过程中的霉变与损毁率 10%。

---
*最后更新：2026-02-01*
