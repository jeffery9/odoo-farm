# 史诗 46：精准生产与变量作业 (Precision Production & VRA)
*目标：基于 PostGIS 空间网格与 NDVI 遥感数据，生成变量施肥处方图并闭环核销作业成本。*

## 1. 用户故事 (User Stories)

1. **[US-46-01] PostGIS 空间网格化引擎 (Spatial Grid Engine)**：🔄 待增强 (2026 技术升级)
    - **描述**：作为农场管理员，我希望系统能将地块自动划分为 5m-10m 的精细网格 Cell。
    - **验收条件**：
        - **(Backend)** 数据库必须启用 PostGIS 扩展，`farm.location` 支持 Geometry 存储。
        - **(Vectorization)** 必须使用 NumPy 向量化处理网格生成逻辑，严禁在 Odoo 模型循环中逐点处理。
        - **(Logic)** 提供网格生成算法，支持根据地块 Polygon 自动填充指定分辨率（如 5m 或 10m）的 Grid 记录。
        - **(Performance)** 1000 亩规模下检索响应时间严禁超过 100ms。

2. **[US-46-02] 卫星 NDVI 栅格自动映射 (Remote Sensing Mapping)**：🔄 待增强 (2026 技术升级)
    - **描述**：作为技术专家，我希望系统能自动同步卫星 NDVI 数据并映射到网格上。
    - **验收条件**：
        - **(Raster-to-Vector)** 系统实现“栅格到矢量”的自动化采样：提取卫星像素值并计算网格 Cell 平均值。
        - **(API)** 对接 Sentinel-2 或 Google Earth Engine (GEE) API，支持自动化时间序列快照拉取。

3. **[US-46-03] 变量处方图算法引擎 (VRA Prescription Engine)**：🔄 待增强 (2026 技术升级)
    - **描述**：作为农技员，我希望根据网格的长势数据，自动生成变量喷施处方逻辑。
    - **验收条件**：
        - **(Logic)** 支持专家定义逻辑（如：NDVI < 0.4 则补肥 20%，或对标 `BasePPOCritic` 风格的动态权重评估）。
        - **(Prescription-State)** 处方图必须支持 `State::Act` 迁移：从 `DRAFT_MAP` 到 `AUTHORIZED_PRESCRIPTION`（需经过农技总监数字签名）。
        - **(Vectorization)** 使用批量计算逻辑确保高性能。

4. **[US-46-04] 农机指令导出 (ISO-XML & Shapefile Export)**：💡 待规划
    - **描述**：作为机手，我希望导出符合标准的文件，以便让农机终端自动执行。
    - **验收条件**：
        - **(Standard-Export)** 支持导出 ISO-11783 (ISO-XML) 标准格式，包含变量速率控制（VRC）属性。
        - **(A2A-Dispatch)** 支持通过 A2A 协议直接将处方任务推送至具备网连能力的农机智能体。

5. **[US-46-05] 实喷图回传与库存对账闭环 (As-Applied Closure)**：🔄 待增强 (2026 技术升级)
    - **描述**：作为财务主管，我希望在作业完成后，系统自动解析作业日志，计算实际消耗。
    - **验收条件**：
        - **(Mass-Balance)** 必须满足物质守恒：`Sum(Cell_Applied_Rate) * Area = Total_Tank_Deduction`。
        - **(Parser)** 系统支持读取并解析 `.log` 或第三方农机云轨迹 JSON 数据。
        - **(Comparison)** 仪表盘展示“处方 vs 实喷”的物理偏差图层（Deviation Map / Spatial Error Heatmap）。

## 业务价值
- **核心价值**: 基于 PostGIS 空间网格与 NDVI 遥感数据，生成变量施肥处方图并闭环核销作业成本，提升农业生产精准度和效率。
- **目标用户**: 农场管理员、财务主管、技术专家、农技员、机手。
- **量化收益**: 减少农药/肥料浪费 15%-25%，提升大规模作业效率 30%，实现 100% 物理层面的作业存证。

## 技术挑战
- **复杂性**: 需要处理空间数据网格化、遥感数据映射、变量处方算法、ISOBUS 协议物理封装等技术。
- **性能要求**: 大规模空间数据处理需高效响应（如 1000 亩 100ms 响应）。
- **安全合规**: 需要符合农业数据安全和遥感数据使用相关法规要求。
- **集成难点**: 与 PostGIS、卫星 API、农机设备、库存系统等系统的集成。

---
*最后更新：2026-01-31*
