# 物联网与传感器数据处理算法 (IoT & Sensor Data Processing Algorithm)

## 算法目的
实时处理来自各类农业传感器（温湿度、pH值、EC值等）的数据流，通过数据融合与异常检测算法，确保环境监控的准确性并提供毫秒级告警。

## 输入参数
- `sensor_data_stream`: 原始传感器遥测报文 (MQTT/JSON)
- `threshold_config`: 阈值配置表（上限/下限/死区） (Dict)
- `moving_average_window`: 滑动窗口大小 (Integer)
- `fusion_weights`: 多传感器加权系数 (Dict)

## 输出结果
- `fused_environment_metrics`: 融合后的环境指标 (Dict)
- `alert_payload`: 告警报文（含严重程度） (Dict)
- `is_anomaly`: 是否为异常离群值 (Boolean)

## 算法流程
1. **数据清洗**: 过滤报文中的非法字符、零值及超出物理极限的无效值。
2. **滑动窗口计算**: 实时计算当前窗口内的移动平均值（MA）与标准差（SD）。
3. **离群值检测**: 采用 Z-Score 算法，判断 `|Value - MA| > 3 * SD`，若是则标记为 `anomaly`。
4. **多点融合**: 对同一地块内的多个同类传感器，执行加权平均：`Fused_Value = Σ (Value[i] * Weight[i])`。
5. **阈值判定**: 检查结果是否触碰安全红线，必要时下发告警至 PWA 端。

## 具体实现 (Implementation)
```python
import numpy as np

def process_sensor_stream(raw_value, history_window, config):
    """
    处理实时 IoT 指标
    raw_value: 当前原始值
    history_window: 历史数据数组 [v1, v2, ... vn]
    config: {'limit_high': 40, 'limit_low': 5, 'sd_k': 3}
    """
    # 1. 基础物理极限过滤
    if not (0 <= raw_value <= 100): # 假设为百分比或常规传感器量程
        return {'status': 'error', 'value': np.nan}
        
    # 2. 离群值检测 (Z-Score)
    if len(history_window) > 5:
        ma = np.mean(history_window)
        sd = np.std(history_window)
        if abs(raw_value - ma) > config['sd_k'] * sd:
            return {'status': 'anomaly', 'value': raw_value, 'reason': 'Outlier'}
            
    # 3. 阈值判定
    alert = None
    if raw_value > config['limit_high']:
        alert = {'severity': 'critical', 'msg': 'Temperature too high'}
    elif raw_value < config['limit_low']:
        alert = {'severity': 'warning', 'msg': 'Temperature too low'}
        
    return {'status': 'ok', 'value': raw_value, 'alert': alert}
```

## 业务规则
- **补偿逻辑**: 若传感器离线，系统需自动调用前一小时的趋势均值进行历史数据插值。
- **降噪处理**: 设置死区（Hysteresis），防止测量值在阈值边缘小幅波动导致告警频繁触发（告警风暴）。

## 验证方法
- 使用模拟器生成噪声数据流，验证离群值过滤算法的稳健性。

## 性能指标
- 单点处理延迟 < 50ms。
- 告警实时性：端到端延迟 < 1 秒。