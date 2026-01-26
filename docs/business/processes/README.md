# 核心业务流程规格文档 (Core Business Process Specifications)

## 目录概述

本目录包含农场管理系统的核心业务流程规格文档，重点描述业务流程的执行标准、操作规范和管理要求。

## 与行业解决方案的区别

- **业务流程规格** (`processes/`): 专注于业务流程的执行标准、操作规范、角色职责和合规要求
- **行业解决方案** (`industries/`): 专注于行业特点分析和如何使用farm模块构建解决方案

## 现有流程文档

### 核心生产流程
- `PLANTING_MANAGEMENT_PROCESS.md` - 种植管理流程：从土地准备到收获的完整种植管理
- `LIVESTOCK_MANAGEMENT_PROCESS.md` - 畜牧管理流程：动物生命周期管理
- `HARVEST_AND_PROCESSING_PROCESS.md` - 收获与加工流程：收获计划与执行、产后处理
- `INPUTS_MANAGEMENT_PROCESS.md` - 投入品管理流程：采购、使用、追溯管理
- `TRACEABILITY_PROCESS.md` - 追溯流程：从种子到消费者的全程追溯

## 流程文档标准结构

所有流程文档应遵循以下结构：

### 1. 流程概述 (Process Overview)
简要描述流程的目的、范围和主要环节

### 2. 流程图 (Process Flow Diagram)
使用Mermaid图表展示流程的环节和流向

### 3. 角色职责 (Role Responsibilities)
明确各角色在流程中的职责和权限

### 4. 业务规则 (Business Rules)
流程执行中必须遵循的业务规则和约束条件

### 5. 系统交互 (System Interactions)
描述流程中需要系统的支持和交互方式

### 6. 合规要求 (Compliance Requirements)
流程需要满足的法规和标准要求

### 7. 异常场景 (Exception Scenarios)
流程执行中可能出现的异常情况及处理方式

### 8. KPI指标 (KPI Metrics)
用于衡量流程执行效果的关键绩效指标

## 维护要求

- 所有流程文档需与实际业务操作保持一致
- 根据法规变化及时更新合规要求
- 确保流程图准确反映实际业务流程
- 定期审查和优化流程效率