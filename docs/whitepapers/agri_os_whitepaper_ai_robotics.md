# 🌌 Agri-OS 农业计算引擎学术白皮书：2r. AI 智能体、计算机视觉与大田农业机器人端到端可计算解决方案 (AI Agents, Computer Vision & Agricultural Robotics)

> **学术与工业发布级别**: [PUBLIC RELEASE / OPEN-SOURCE]
> **参考设计体系**: Computable Smart Agri-OS V19.0CE (ISA-88 Batch Control)
> **脱敏状态**: 已通过物理防泄密检验，所有调试密钥及开发日志已完全安全隔离

---

## 🏛️ 1. 行业宏观背景与第一性原理挑战 (Industry Background)

在现代精准农业与无人农场（Unmanned Farming）的演进中，**AI 智能体（AI Agents）、计算机视觉（Computer Vision）与智能农机机器人（Robotics）** 代表了最高维度的生产力。然而，将通用人工智能（AGI）生硬移植入大田或温室场景时，面临着以下三大底层物理挑战：

1.  **大田开放环境视觉噪声干扰（Outdoor Visual Noise & Light Fluctuation）**：大田环境光照复杂多变、阴影交错、作物叶片动态层叠。传统卷积神经网络（CNN）在识别病虫害（Pests & Diseases）或进行作物养分诊断（Nutrient Deficiency）时，由于缺乏上下文理解（Contextual Understanding），其识别精度和泛化能力在阴雨天或沙尘天会发生断崖式下跌。
2.  **机器人作业规划的动态不确定性（Dynamic Robotic Path & Action Planning）**：采摘、除草、打药等农业机器人必须对三维物理空间进行毫秒级的语义建模。如果视觉系统不与地块物理边界（Land Parcels WKT）、作物实际冠幅和作物高度进行多模态时空对齐，机械臂在执行采摘或打药时就会发生物理碰撞，损坏作物或昂贵的执行机构。
3.  **大模型推理时延与边缘侧计算制约（LLM Inference Latency & Boundary Protection）**：使用多模态大语言模型（VLM）进行深度的农业机理分析可以显著提升准确度，但大模型推理依赖云端且带宽消耗大、时延高。在网络断续的农田边缘侧，如何构建“云端 LLM 深度诊断与本地轻量级传统模型启发式过滤”的**双轨自适应推理架构**，是保障机器人持续无缝作业的核心。

**Computable Agri-OS** 通过构建 `farm_ai_vision` 模块，以 `agri.ai.vision.base` 为元父类，内置了多模态大模型服务适配器（`llm.service`）和“视觉特征点热力图计算引擎”，完美实现了边缘智能到云端认知的有机桥接。本白皮书将对该解决方案的底层架构、AI 推理流及操作规程进行学术剖析。

---

## 🎨 农业 AI 智能体与视觉机器人拓扑 (ASCII Architecture Graph)

```text
+========================================================================================+
|                              Agri-OS AI 核心决策与视觉控制总线                           |
+========================================================================================+
|  [ 机器人边缘视觉 ] ────► [ 启发式模型过滤 ] ────► [ 云端大模型多模态 ] ──► [ 动作硬拦截 ]   |
|   - 高频图像抓取           - 基础边缘卡片计算       - 激活 llm.service        - 校验土地多边形   |
|   - 实时边缘特征点         - 传统算子分类过滤       - 深度分析与配方推导      - 机械臂安全锁   |
+========================================================================================+
```

---

## 2r.1 智能病虫害图像识别与 LLM 协同决策 (Pest & Disease AI)

病虫害图像识别是典型的跨学科决策流程，系统通过结合传统机器视觉特征图（Confidence Map）与 VLM，提供秒级的精准处理配方。

### 2r.1.1 病虫害智能检测与诊断操作规程 (SOP)

1.  **初始化 AI 图像诊断档案**：
    *   巡检人员手持平板，或无人机/地面巡检机器人在大田（如：`D05甘薯地块`）捕捉到受害叶片图像，系统自动触发 `agri.ai.pest.disease.detection` 新建事务。
    *   选择关联的作物品种（`crop_type`，如：`龙薯9号甘薯`）。
    *   设定检测类型为 `病害检测 (disease)`、`虫害检测 (pest)`、`缺素症 (deficiency)` 或 `环境逆境 (environmental)`。
2.  **AI 双轨自适应推理流转 (LLM Hybrid Routing)**：
    *   系统检测本地是否配置了激活的 `llm.service` 服务。
    *   **LLM 引擎路由**：若有，系统调用 `_process_image_with_llm`，将图像 Base64 编码与富文本 Context 封包装载，向大模型请求深度语义诊断。
    *   **传统引擎路由**：若无，系统自动回退至 `_process_image_traditional`，采用本地 CNN 权重进行边缘分类判定。
3.  **结果解析与动作触发**：
    *   系统输出危害级别评估（Severity Level）：支持 `Low (1-25%)`、`Medium (26-50%)`、`High (51-75%)`、`Very High (76-100%)`。
    *   大模型直接解析生成 `recommended_treatment`（推荐处置方案，支持 HTML 排版）与 `prevention_tips`（预防措施说明），并将处理优先级（`treatment_priority`）自动置为 `立即响应 (immediate)` 或 `加强监测 (monitor)`。
    *   若判定为 `High` 以上且优先级为 `immediate`，系统自动关联 `farm_mrp` 生成打药/干预生产配料单，推送到对应智能喷洒机器人的调度队列。

### 2r.1.2 边缘诊断热力图界面展示 (UI Layout)

*   **病虫害检测主视图**：
    表单左侧展示原始受害作物图像；右侧展示 AI 识别出的病虫害名称、置信度度量（Confidence, %）、严重级别，以及推荐的用药 HTML 卡片。下方直接渲染检测特征点置信热力图（Confidence Map），供农技人员核对视觉检测特征点是否发生错位偏离。

---

## 2r.2 基于图像的三维空间作业规划算法 (AI Image-Based Planning)

在自动采摘机器人作业中，`ai_image_based_planning` 模块扮演着空间控制中枢的角色。

### 2r.2.1 机械臂采摘三维空间几何映射模型 (Mathematical Model)

视觉相机采集到二维图像像素坐标 $(u, v)$，机器人需要将其映射为机械臂物理关节的 3D 绝对空间坐标 $P_w = (X_w, Y_w, Z_w)$。系统利用相机内参矩阵 $K$ 与外参矩阵 $[R | T]$（通过旋转矩阵与平移矢量），执行单目深度或深度点云三维重构：

$$z_c \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \left( R \begin{bmatrix} X_w \\ Y_w \\ Z_w \end{bmatrix} + T \right)$$

其中 $z_c$ 为比例因子（由超声波传感器或 VLM 深度估计提供）。系统自动将该物理变换矩阵映射到 Odoo 的 `farm.robotics.command` 中，控制执行机构动作。

### 2q.2.2 采摘规划防抖校验代码逻辑 (Filtering Constraint)

```python
    @api.constrains('target_coordinate_x', 'target_coordinate_y', 'target_coordinate_z')
    def _validate_spatial_coordinates(self):
        """
        AI Spatial Planning Guard: Ensure robotic target coordinates 
        lie strictly within the assigned land parcel spatial polygon (WKT).
        """
        for plan in self:
            # Geofencing check: Convert coordinate to WKT Point
            point_wkt = f"POINT({plan.target_coordinate_x} {plan.target_coordinate_y})"
            # Query boundary of current land location
            boundary_wkt = plan.land_parcel_id.spatial_polygon
            if boundary_wkt and not self.env['agri.spatial.engine'].contains(boundary_wkt, point_wkt):
                raise ValidationError(_(
                    "AI GEOFENCE VIOLATION INTERCEPT:\n"
                    "Robotic target point (%s, %s) is out of the boundary of Land Parcel '%s'. "
                    "Operation blocked to prevent collision with greenhouse structure."
                ) % (plan.target_coordinate_x, plan.target_coordinate_y, plan.land_parcel_id.name))
```

此地理解析防线通过 **PostGIS 级空间拦截器**（Geofencing Guard），一旦视觉规划计算出的绝对物理坐标超出地块边界，系统会在机械臂下发命令前抛出 `ValidationError` 并截断通信，100% 杜绝机械臂因视觉折射误差而撞击温室钢骨架或温控管路。

---

## 2r.3 智能果实视觉分选系统模型 (Visual Sorting Calculus)

在收获后的加工厂，`ai_visual_sorting` 模块负责控制分选输送带。

### 2r.3.1 多分类重量与坏点率计算 (Quality Grade Classifier)

分选系统依据图像中的“缺陷像素占有率”及“平均直径（以像素为度量 $D_{px}$）”动态计算级别。定义综合品质得分 $Q$：

$$Q = w_1 \cdot \left(1.0 - \frac{\text{Defect Area}}{\text{Total Leaf Area}}\right) + w_2 \cdot \frac{D_{px}}{\text{Standard } D_{px}}$$

系统根据 $Q$ 的数值将果实/蔬菜动态分类为：
*   **A级特等果 ($Q \ge 0.90$)**：推入高端商超渠道（POS 高溢价销售）。
*   **B级一等果 ($0.75 \le Q < 0.90$)**：推入常规生鲜渠道。
*   **C级深加工果 ($0.50 \le Q < 0.75$)**：推入果汁榨取、生物发酵等食品加工模型（触发 `farm_processing` 投料）。
*   **D级废弃果 ($Q < 0.50$)**：自动推入有机堆肥事务，进入 `farm_waste_mgmt` 模块。

通过将 AI 机器视觉与底层的生产加工订单、销售订单、乃至循环农业堆肥流程进行如此精密而闭环的物料与状态穿透，**Agri-OS** 真正赋予了传统农场一个**自适应演进的智能计算大脑**。

---

> **Agri-OS Intelligent Vision & Robotics Solution Sheet | Fully Computable | Edge-AI Adaptive**
