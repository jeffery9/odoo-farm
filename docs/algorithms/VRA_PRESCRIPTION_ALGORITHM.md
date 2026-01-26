# 变量施用处方图算法文档 (Variable Rate Application Prescription Algorithm)

## 算法目的
基于地块内部空间差异（土壤养分、长势、病虫害）的精准投入品（肥、药、水、种）管理，生成变量施用处方图。

## 输入参数
- `grid_cells`: 地块网格数据，包含每个网格的边界和几何中心点 (list of dict)
- `resolution`: 网格精度（米），默认 10.0 (float)
- `ndvi_data`: 植被指数数据 (dict with grid_id as key and NDVI value)
- `base_rate`: 基准作业量 (float)
- `strategy_type`: 策略类型（如线性修正、阈值步进）(str)

## 输出结果
- `prescription_map`: 生成的处方图，包含各网格的施用率 (dict)
- `target_rates`: 每个网格的目标施用率 (dict)
- `efficiency_metrics`: 处方图效率评估指标 (dict)

## 算法流程
1. **网格生成**: 使用 PostGIS 的 ST_MakeEnvelope 生成覆盖地块 Bounding Box 的网格并裁剪
2. **数据预处理**: 对每个网格关联 NDVI 数据和其他农学指标
3. **策略应用**: 根据策略类型应用不同的计算公式
4. **向量化计算**: 使用 NumPy 进行批量计算以提高性能
5. **边界限制**: 对计算结果应用物理极值限制
6. **输出生成**: 生成符合 ISOBUS 标准的处方图文件

## 业务规则
- 支持多种策略类型：线性修正、阈值步进、分段函数等
- 实现向量化计算以处理数千网格的高效计算
- 限制施用率在物理可行范围内
- 支持人工干预调整和批量修正

## 验证方法
- 与专家经验处方图对比验证
- 田间作业效果评估
- 经济效益分析验证

## 性能指标
- 千量计算响应时间 < 5秒 (针对大规模地块)
- 计算精度与实际需求匹配度 > 90%
- 支持的网格数量 > 10,000个