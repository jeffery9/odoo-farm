# 🗺️ 空间智能 (Spatial Intelligence) 架构规格

## 1. 原子空间单元：网格化 (The Grid)
在我们的架构中，地块不再是一个多边形，而是一个**动态 Raster 网格集合**。

- **模型**：`agri.geospatial.grid.cell`
- **逻辑**：每个单元格持有 NDVI、pH、水分、养分等多维属性。
- **优势**：支持空间插值（Kriging/IDW），从有限的采样点推导出全田图谱。

## 2. 空间-物理映射 (Spatial-Physical Mapping)

```mermaid
sequenceDiagram
    participant Machine as 农机 (IoT)
    participant Bridge as agri_iot 桥接
    participant Logic as VRA 逻辑层
    participant Grid as 空间网格系统

    Machine->>Bridge: 上报实时 GPS [Lat, Lng]
    Bridge->>Logic: 触发位置感知请求
    Logic->>Grid: 检索坐标所属 Cell_ID
    Grid-->>Logic: 返回 Cell 属性 (目标施肥量: 12.5kg)
    Logic->>Logic: 叠加生理权重与天气对冲
    Logic->>Bridge: 下发 Setpoint (11.8kg)
    Bridge->>Machine: 修改阀门/频率
```

## 3. 技术壁垒
- **性能优化**：通过向量化计算（NumPy）处理万级网格的实时计算。
- **空间索引**：GIST 索引支持毫秒级的邻域发现与碰撞判定。
