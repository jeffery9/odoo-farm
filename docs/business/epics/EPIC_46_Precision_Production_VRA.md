# 史诗 46：精准生产与变量作业 (Precision Production & VRA)
*目标：通过 PostGIS 空间网格化技术实现投入品的“按需变量投放”，降低成本并保护土壤。*

---

## 1. 用户故事 (User Stories)

1. **[US-46-01] PostGIS 空间网格化引擎 (Spatial Grid Engine)**：💡 待规划
    - **描述**：作为农场管理员，我希望系统能将地块自动划分为 5m-10m 的精细网格 Cell，以便进行毫秒级的空间属性检索。
    - **验收条件**：
        - **(Backend)** 数据库必须启用 PostGIS 扩展，`farm.location` 支持 Geometry 存储。
        - **(Logic)** 提供网格生成算法（Tiling Logic），支持根据地块 Polygon 自动填充指定分辨率（如 10m）的 Grid 记录。
        - **(Performance)** 在 1000 亩规模地块下，根据坐标检索所属网格 Cell 的响应时间严禁超过 100ms。
        - **(GIS)** 每个网格必须存储其中心点坐标（Centroid）和四个角点的空间坐标。

2. **[US-46-02] 卫星 NDVI 栅格自动映射 (Remote Sensing Mapping)**：💡 待规划
    - **描述**：作为技术专家，我希望系统定期同步 Sentinel-2 卫星数据，并将其栅格像素值自动映射到地块网格 Cell 中。
    - **验收条件**：
        - **(API)** 成功对接 Sentinel Hub，能根据地块 Bounding Box 获取近 5 天内的云量 < 10% 的 NDVI 栅格。
        - **(Logic)** 实现栅格到矢量的转换逻辑（Zonal Statistics），将卫星像素点值取平均/加权映射到 `farm.location.grid` 的属性字段中。
        - **(UX)** 地图界面必须支持渲染“网格颜色层”，通过色阶展示长势差异。

3. **[US-46-03] 变量处方图算法引擎 (VRA Prescription Engine)**：💡 待规划
    - **描述**：作为农技员，我希望根据网格的长势数据，自动生成变量喷施处方逻辑（例如：NDVI < 0.4 则补肥 20%）。
    - **验收条件**：
        - **(Logic)** 提供“处方公式编辑器”，支持 Python 脚本化定义：`rate = base_rate * f(ndvi, soil_n)`。
        - **(UI)** 生成结果需以热力图形式展现，并支持手动“刷选（Brush Selection）”修改特定网格的作业量。
        - **(Audit)** 系统必须记录处方生成的算法快照及修改记录。

4. **[US-46-04] 农机指令导出 (ISO-XML & Shapefile Export)**：💡 待规划
    - **描述**：作为机手，我希望导出符合 ISOBUS 标准的 XML 或带 Rate 属性的 Shapefile，以便让农机终端自动执行。
    - **验收条件**：
        - **(Export)** 支持导出 `.zip` 压缩包，内含 `.shp`, `.shx`, `.dbf` 文件，且 `.dbf` 中必须包含名为 `Rate` 的浮点数列。
        - **(Standard)** 支持符合 ISO 11783-10 标准的 XML 导出，包含 TaskData 节点。
        - **(Compatibility)** 导出的坐标系必须强制转换为 WGS 84 (EPSG:4326)。

5. **[US-46-05] 实喷图回传与库存对账闭环 (As-Applied Closure)**：💡 待规划
    - **描述**：作为财务主管，我希望在作业完成后，系统自动解析农机回传的作业日志，计算实际消耗并扣减库存。
    - **验收条件**：
        - **(Parser)** 系统支持读取并解析 `.log` 或第三方农机云（如极飞/大疆）的实喷轨迹 JSON 数据。
        - **(Inventory)** 根据实喷数据点位累加出的消耗量，自动核销 Odoo 库存并关联对应的 `mrp.production`。
        - **(Comparison)** 仪表盘必须展示“处方 vs 实喷”的偏差图层（Deviation Map），标出作业漏喷或过喷区域。
