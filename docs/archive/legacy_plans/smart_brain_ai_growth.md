# 方向二：智慧大脑——生长预测与 AI 视觉技术细节

## 1. 数字化物候期模型 (Phenology Engine)
### 1.1 积温算法 (GDD Calculation)
- **模型**：`farm.location.gdd.log`
- **计算逻辑**：
  - `daily_gdd = max(0, (temp_max + temp_min) / 2 - Tbase)`。
  - `Tbase`：由品种定义（如水稻一般为 10°C）。
  - **动态预测**：利用未来 7 天天气预报，预计算 `accumulated_gdd`。

### 1.2 生长曲线拟合 (Logistic Growth Curve)
- **数学公式**：`W(t) = L / (1 + exp(-k(t - t0)))`
  - `L`：最大期望生物量（Max Yield/Biomass）。
  - `k`：生长速率常数。
  - `t0`：生长最快的时间点（拐点）。
- **偏差分析**：计算 `(W_actual - W_predicted) / W_predicted`。若偏差 > 20% 触发 `Agri Warning` 系统通知。

## 2. AI 视觉诊断流 (Vision Inference Flow)
### 2.1 移动端 PWA 离线识别
- **技术栈**：TensorFlow.js + WebAssembly。
- **流程**：
  1. 用户拍摄病叶照片。
  2. 提取特征向量，在浏览器端进行初筛。
  3. 若置信度 < 0.8，提示用户“等待信号时上传云端精细诊断”。

### 2.2 云端推理与知识关联
- **API 请求**：发送 Base64 图片 + GPS 坐标 + 作物 ID。
- **后端逻辑**：
  - 识别病害标签（如：`Rice_Blast`）。
  - 查询 `farm.knowledge` 中 `tag = 'Rice_Blast'` 的 `intervention_sop_id`。
  - 自动创建 `farm.task` 草稿，预填建议使用的药剂及其标准剂量。

## 3. 产量预测仪表盘 (Yield Dashboard)
- **可视化组件**：使用 `ECharts` 绘制双曲线图（标准生长线 vs 实际观测线）。
- **概率分布**：利用蒙特卡洛模拟（基于气象波动历史）计算“收割期概率分布图”，展示在 95% 置信区间下的收割日期。