# 史诗 46：精准生产与变量作业 (Precision Production & VRA)
*目标：基于 PostGIS 空间网格与 NDVI 遥感数据，生成变量施肥处方图并闭环核销作业成本。*

1. **[US-46-01] PostGIS 空间网格化引擎 (Spatial Grid Engine)**：✅ 已完成 (2026-01-25)
    - **描述**：作为农场管理员，我希望系统能将地块自动划分为 5m-10m 的精细网格 Cell。
    - **验收条件**：
        - **(Backend)** 数据库必须启用 PostGIS 扩展，`farm.location` 支持 Geometry 存储。
        - **(Logic)** 提供网格生成算法，支持根据地块 Polygon 自动填充指定分辨率的 Grid 记录。
        - **(Performance)** 1000 亩规模下检索响应时间严禁超过 100ms。

2. **[US-46-05] 实喷图回传与库存对账闭环 (As-Applied Closure)**：✅ 已完成 (2026-01-25)
    - **描述**：作为财务主管，我希望在作业完成后，系统自动解析农机回传的作业日志，计算实际消耗。
    - **验收条件**：
        - **(Parser)** 系统支持读取并解析 `.log` 或第三方农机云的轨迹 JSON 数据。
        - **(Inventory)** 自动核销 Odoo 库存并关联对应的 `mrp.production`。
        - **(Comparison)** 仪表盘展示“处方 vs 实喷”的偏差图层（Deviation Map）。

3. **[US-46-02] 卫星 NDVI 栅格自动映射 (Remote Sensing Mapping)**：💡 待规划
    - **描述**：作为技术专家，我希望系统能自动同步卫星 NDVI 数据并映射到网格上。
    - **验收条件**：
        - **(API)** 对接 Sentinel-2 或 Google Earth Engine API。

4. **[US-46-03] 变量处方图算法引擎 (VRA Prescription Engine)**：💡 待规划
    - **描述**：作为农技员，我希望根据网格的长势数据，自动生成变量喷施处方逻辑。
    - **验收条件**：
        - **(Logic)** 支持专家定义逻辑（如：NDVI < 0.4 则补肥 20%）。

5. **[US-46-04] 农机指令导出 (ISO-XML & Shapefile Export)**：💡 待规划
    - **描述**：作为机手，我希望导出符合 ISOBUS 标准的 XML 文件，以便让农机终端自动执行。
    - **验收条件**：
        - **(Export)** 支持导出 ISO-XML 或带 Rate 属性的 Shapefile。