# 遗传连锁图谱构建算法文档 (Genetic Linkage Mapping Algorithm)

## 算法目的
构建作物遗传连锁图谱，用于基因定位、分子标记辅助选择和育种决策支持。

## 输入参数
- `genotype_data`: 基因型数据 (dict 包含SNP、SSR等标记信息)
- `phenotype_data`: 表型数据 (农艺性状测量值)
- `population_type`: 群体类型 (F2、RIL、BC等)
- `marker_density`: 标记密度 (个/Mb)
- `recombination_threshold`: 重组率阈值 (0-0.5)
- `linkage_criteria`: 连锁判断标准 (LOD阈值)

## 输出结果
- `linkage_map`: 连锁图谱 (dict 包含连锁群和标记位置)
- `map_distance`: 图距 (cM)
- `marker_order`: 标记顺序
- `marker_density`: 标记密度分布
- `qtl_regions`: QTL定位区间
- `heritability_analysis`: 遗传力分析

## 算法流程
1. **数据预处理**: 清洗基因型数据，处理缺失值和异常值
2. **连锁检验**: 计算标记间重组率和LOD值
3. **连锁分组**: 基于重组率将标记分配到连锁群
4. **标记排序**: 使用连锁分析算法确定标记顺序
5. **图距计算**: 使用Haldane或Kosambi函数计算遗传距离
6. **QTL定位**: 使用区间作图法或复合区间作图法定位QTL
7. **结果验证**: 图谱质量评估和验证

## 业务规则
- LOD评分阈值 > 3.0
- 重组率阈值 < 0.4
- 支持多种群体类型分析
- 考虑性别特异性重组率
- 自动检测和处理异常标记

## 验证方法
- 与已知基因位置对比验证
- 交叉验证图谱稳定性
- 遗传参数一致性检验
- 与传统育种数据对比

## 性能指标
- 处理效率 > 1000标记/小时
- 图谱准确性 > 90%
- 内存使用 < 4GB (10000标记)
- 响应时间 < 30分钟