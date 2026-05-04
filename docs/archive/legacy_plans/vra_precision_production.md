# 方向一：精准生产——VRA 与传感器融合技术细节

## 1. 空间网格化实现 (PostGIS Infrastructure)
### 1.1 数据模型
- **模型名**：`farm.location.grid.cell`
- **关键字段**：
  - `boundary`: `Geometry(Polygon, 4326)` - 栅格边界。
  - `centroid`: `Geometry(Point, 4326)` - 几何中心点。
  - `resolution`: `Float` - 精度（米），默认 10.0。
  - `latest_ndvi`: `Float` - 最近一次观测的植被指数。
  - `target_rate`: `Float` - 当前处方作业量（如：kg/mu）。

### 1.2 网格生成逻辑 (SQL 实现参考)
```sql
-- 使用 ST_MakeEnvelope 生成覆盖地块 Bounding Box 的网格并裁剪
INSERT INTO farm_location_grid_cell (boundary, location_id)
SELECT ST_Intersection(ST_SetSRID(ST_MakeEnvelope(xmin, ymin, xmax, ymax), 4326), parcel_geom)
FROM (
    SELECT ST_XMin(geom) as xmin, ... -- 基于地块边界计算范围
) as bbox;
```

## 2. 卫星数据感知 (Remote Sensing)
### 2.1 NDVI 计算逻辑
- **数据源**：Sentinel-2 (L2A 级别，已做大气校正)。
- **公式**：`NDVI = (B8 - B4) / (B8 + B4)` (近红外 - 红光)。
- **处理流**：
  1. 调用 Sentinel Hub API 获取 GeoTIFF。
  2. 使用 `rasterio` 或 `GDAL` 在后端解析栅格。
  3. 执行 **Zonal Statistics**：计算每个 `grid.cell` 范围内像素的均值并更新 `latest_ndvi`。

## 3. 处方生成算法 (Prescription Algorithm)
### 3.1 变量公式引擎
支持用户自定义策略（Policy），例如：
```python
# 线性修正模型
if cell.latest_ndvi < 0.4:
    cell.target_rate = base_rate * (1 + (0.4 - cell.latest_ndvi) * correction_factor)
else:
    cell.target_rate = base_rate
```

## 4. 农机指令交互 (Machinery I/O)
### 4.1 Shapefile 规范
- **坐标系**：必须为 WGS 84。
- **字段映射**：属性表中必须包含 `Rate` (Float), `Unit` (String), `TaskID` (Integer)。
### 4.2 ISO-XML 映射
- `PAN` (Process Data Entity)：对应作业任务。
- `VNP` (Value Presentation)：定义作业量单位映射。
- `DDI` (Data Dictionary Identifier)：如 DDI 141 代表氮肥施用量。

## 5. UI/UX 关键交互
- **地图图层切换**：支持 NDVI 热力图层与作业处方图层的叠加（Opacity Control）。
- **批量修正**：用户在地块地图上使用“Lasso”工具圈选网格，弹出 Action 窗口一键修改选中网格的 `target_rate`。

## 6. 变量决策引擎实现深度 (Decision Engine Implementation)

### 6.1 策略与处方模型设计
为实现灵活的农学决策，采用以下模型结构：
- **`farm.vra.strategy` (变量策略)**：定义核心决策逻辑（如线性修正、阈值步进）。
  - `strategy_type`: `Selection` - 决定使用的数学算法。
  - `base_rate`: `Float` - 基准作业量。
  - `python_code`: `Text` - 高级专家模式，支持直接编写计算脚本。
- **`farm.vra.prescription` (作业处方图)**：存储计算结果的容器。
  - `location_id`: `Many2one` - 目标地块。
  - `grid_line_ids`: `One2many` - 每个网格的具体作业指令。

### 6.2 向量化计算引擎 (NumPy Based)
由于单个地块可能包含数千个网格，计算必须在后端进行向量化优化，以避免 Odoo 模型循环带来的延迟。
```python
import numpy as np

def compute_batch_rates(self, ndvi_array, strategy):
    """
    ndvi_array: NumPy 向量，包含所有网格的 NDVI 值
    strategy: 策略对象
    """
    if strategy.strategy_type == 'linear':
        # Rate = Base * (1 + (Target_NDVI - Current_NDVI) * Slope)
        rates = strategy.base_rate * (1 + (strategy.target_ndvi - ndvi_array) * strategy.slope)
    elif strategy.strategy_type == 'step':
        # 分段步进函数
        rates = np.where(ndvi_array < 0.3, strategy.base_rate * 1.5, strategy.base_rate)
    return np.clip(rates, strategy.min_limit, strategy.max_limit) # 限制物理极值
```

### 6.3 交互式“刷选”微调逻辑 (Manual Fine-tuning)
PWA 地图端允许农技员手动干预模型结果：
1. **框选 (Box Select)**: 利用 `Leaflet-Geoman` 插件，用户在地块内拉出矩形或多边形。
2. **空间查询**: 后端通过 `ST_Within(grid.boundary, user_selection_polygon)` 快速识别被选中的网格 ID。
3. **批量更新**: 调用 Odoo 的 `write()` 方法统一修改选中网格的 `target_rate`。

### 6.4 最终指令下发流 (Dispatch Flow)
1. **对齐 (Alignment)**: 确保所有网格坐标系均已转换为 WGS 84 (EPSG:4326)。
2. **生成 (Generation)**: 利用 `pyshp` 库将网格几何体与 `target_rate` 属性写入 Shapefile。
3. **封装 (Packaging)**: 将 `.shp`, `.shx`, `.dbf`, `.prj` 四个核心文件打包为 `.zip`。
4. **分发 (Distribution)**: 通过 PWA 的“下载”按钮或 MQTT 云端推送至农机终端（如大疆农业云/极飞云 API）。

## 7. 数据闭环与财务核销深度设计 (Data Closed-loop & Financial Reconciliation)

### 7.1 实喷数据 (As-Applied) 解析与映射
作业完成后，农机生成的 As-Applied 数据是业财一体化的唯一真实凭证。
- **数据解析器 (Parser)**：系统需支持解析 ISO-XML 中的 `DLV` (Data Log Value) 节点或第三方云端回传的瞬时流量 GPS 轨迹。
- **网格对齐 (Spatial Join)**：利用 PostGIS 将实喷点位数据（Points）与处方网格（Grid Cells）进行空间联结。
  ```sql
  -- 计算每个网格的实际作业量均值
  UPDATE farm_vra_prescription_line l
  SET actual_rate = (
      SELECT AVG(p.flow_rate) 
      FROM as_applied_points p 
      WHERE ST_Within(p.geom, l.geometry)
  );
  ```

### 7.2 自动化库存核销逻辑
- **总量计算**：系统汇总所有网格的 `actual_rate * cell_area`，得出本次作业消耗的投入品（如尿素）总质量。
- **库存动作**：
  1. 自动定位对应的 `mrp.production` (生产指令)。
  2. 生成 `stock.move`：从原料库（Raw Material Location）移动至虚拟消耗库（Virtual/Consumption）。
  3. 关联 `stock.lot`：确保核销的是正确的农资批次，以维持全程溯源链条。

### 7.3 成本分摊与资产价值化
- **单位成本计算**：将投入品成本、农机折旧、人工费（基于工时记录）按实际作业面积比例，自动分摊到产出品的 Lot (批次) 中。
- **会计凭证**：自动生成 `account.move`。
  - 借：生产成本 - 直接材料（地块 ID / 批次 ID）。
  - 贷：原材料库存。

### 7.4 效能评估与偏差分析 (Efficiency & Deviation)
- **漏喷/过喷报警**：计算 `Deviation = (Actual - Planned) / Planned`。
  - 若 `Deviation > 15%`：标记为“过喷区”，提醒农技员检查设备压力补偿。
  - 若 `Actual = 0` 且 `Planned > 0`：标记为“漏喷区”，系统自动生成一个“补喷提醒”Activity。
- **覆盖率统计**：自动计算 `Effective_Coverage_Rate = (实喷面积 / 处方面积) * 100%`，作为机手绩效考核（Epic 13）的核心指标。