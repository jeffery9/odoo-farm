# 🌱 生物数字孪生 (Bio-Digital Twin) 架构规格

## 1. 核心概念：数字化的生长生命周期
我们不只记录操作，我们模拟生命。通过 **Logistic 生长模型** 和 **GDD 积温模型**，系统能够感知作物的“生物年龄”而非物理日期。

## 2. 生物量亏缺补偿架构 [US-78-06]

```mermaid
graph TD
    subgraph Model["理论模型"]
        Logi["Logistic 曲线 (W_theo)"]
        GDD["累计积温 (Clock)"]
    end

    subgraph Sense["实测反馈"]
        IoT["生物量感知 (W_act)"]
        Stress["生物压力指数 (Stress)"]
    end

    subgraph Decision["决策修正"]
        Gap["亏缺计算 (delta_W)"]
        Mult["补偿乘数 (Multiplier)"]
    end

    GDD --> Logi
    Logi --> Gap
    IoT --> Gap
    Gap --> Mult
    Stress --> Mult
    Mult --> Prescription["VRA 变量处方"]
```

## 3. 商业价值：可预测的产出
- **成熟期预测**：通过 GDD 模型提前 7-14 天锁定采收窗口。
- **产量风险预警**：当实际生物量严重偏离理论曲线时，自动触发“干预警报”。
