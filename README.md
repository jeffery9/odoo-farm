# Odoo 19 农场管理系统：菜单架构设计与实现 (Farm Management System: Menu Architecture Design & Implementation)

## 项目概述

本项目是 Odoo 19 农场管理系统的菜单架构设计与实现，旨在为农业企业提供一套完整的、符合农业行业习惯的用户界面系统。系统通过三层用户组架构（技术层、应用层、角色层）实现了从基础功能到业务角色的完整权限管理。

## 架构设计原则

### 1. 三层用户组架构
- **技术层级用户组**：基于系统功能模块的技术权限（Addon级别）
- **应用层级用户组**：基于业务App的复合权限组
- **角色层级用户组**：基于业务角色的最终用户权限组

### 2. 单一职责原则 (SRP)
- 每个模块承担单一职责
- 每个模型文件只包含一个主要模型
- 每个视图文件只包含相关模型的视图定义
- 每个菜单项对应明确的业务功能

### 3. 农业术语去工业化
- 使用农业术语替代工业术语
- 符合农业行业习惯和认知
- 消除制造业术语的认知摩擦
- 提供本地化和区域化支持

## 菜单结构

### 顶级菜单项
```
Farm Management (农场管理)
├── Agricultural Families (农业活动家族)
├── Planting (种植管理)
├── Livestock (畜牧管理)
├── Aquaculture (水产养殖)
├── Agritourism (观光农业)
├── Processing (农产品加工)
├── Supply Chain (供应链)
├── Marketing (营销管理)
├── Quality & Safety (质量与安全)
├── HR & Labor (人力与劳力)
├── Finance & Costs (财务与成本)
├── Multi-Entity Collaboration (多实体协同)
├── IoT & Automation (物联网与自动化)
├── Sustainability (可持续发展)
├── Administration (系统管理)
└── Dashboards (仪表板)
```

### 核心功能模块
- **farm_core**: 基础主数据管理
- **farm_operation**: 生产作业管理
- **farm_planning**: 生产规划管理
- **farm_multi_farm**: 多实体协同与合作社管理
- **farm_ux_deindustrialization**: 用户体验与术语去工业化
- **farm_live_streaming**: 直播与抖音对接

## 实现的史诗 (Epics)

### 史诗 16：用户体验与术语去工业化 (UX & De-industrialization)
- **US-16-01**: 术语农业化映射
- **US-16-02**: 行业化表单布局
- **US-16-03**: 视觉化状态标识
- **US-16-04**: 个性化工作空间定制
- **US-16-05**: 智能上下文帮助
- **US-16-06**: 农业知识图谱集成
- **US-16-07**: 多感官交互体验
- **US-16-08**: 农业社交与协作功能
- **US-16-09**: 无障碍设计与包容性

### 史诗 19：多实体协同与合作社管理 (Multi-Entity Collaboration & Cooperative Management)
- **US-19-01**: 多农场实体关系建模
- **US-19-02**: 租户级数据隔离与共享
- **US-19-03**: 跨农场资源调度与协同
- **US-19-04**: 合作社级财务汇总与分摊
- **US-19-05**: 加盟农场标准化管理

### 史诗 21：直播与抖音对接 (Live Streaming & Douyin Integration)
- **US-21-01**: 抖音账号授权与绑定
- **US-21-02**: 商品库同步与管理
- **US-21-03**: 直播间商品关联
- **US-21-04**: 订单自动回传与处理
- **US-21-05**: 直播数据统计与分析
- **US-21-06**: 直播预告与推广
- **US-21-07**: 直播内容存档与复用

## 技术实现

### 模型层 (Models)
- 每个功能模块有独立的模型文件
- 遵循 Odoo 19 开发规范
- 实现完整的业务逻辑和数据验证

### 视图层 (Views)
- 每个模型有对应的树形和表单视图
- 支持移动端友好界面
- 实现农业术语的界面展示

### 安全层 (Security)
- 完整的权限控制体系
- 数据级访问控制
- 角色基础的访问控制 (RBAC)

### 业务价值
1. **提升用户体验**：使用农业术语，符合行业习惯
2. **增强协作效率**：支持多实体协同管理
3. **保障数据安全**：实现租户级数据隔离
4. **促进标准化**：统一的生产标准和管理流程
5. **支持合规管理**：符合中国农业法规要求

## 文件结构

```
farm/
├── EPICS_AND_USER_STORIES.md          # 用户故事汇总
├── MODULE_PLAN.md                     # 模块计划
├── DEVELOPMENT_CONVENTIONS.md         # 开发规范
├── MENU_STRUCTURE_PLAN.md             # 菜单结构规划
├── MENU_IMPLEMENTATION_PLAN.md        # 菜单实现计划
├── MENU_IMPLEMENTATION_CHECKLIST.md   # 菜单实现检查清单
├── MENU_ARCHITECTURE_DIAGRAM.md       # 菜单架构图
├── APPLICATION_ARCHITECTURE.md        # 应用架构
├── USER_GROUPS_DESIGN.md              # 用户组设计
├── farm_core/                         # 核心模块
├── farm_operation/                    # 生产作业模块
├── farm_multi_farm/                   # 多实体协同模块
├── farm_ux_deindustrialization/       # 用户体验模块
└── farm_live_streaming/               # 直播电商模块
```

## 安装与配置

1. 安装依赖模块：
   ```bash
   # 安装基础模块
   pip install odoo19
   ```

2. 安装农场管理系统模块：
   ```bash
   # 在 Odoo 配置中添加模块路径
   --addons-path=addons,/path/to/farm/modules
   ```

3. 启用模块：
   - 在 Odoo 应用商店中安装所需模块
   - 配置用户权限和角色

## 许可证

本项目采用 LGPL-3 许可证，允许自由使用、修改和分发。

## 联系方式

如需技术支持或功能定制，请联系项目团队。