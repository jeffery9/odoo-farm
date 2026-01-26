# 垂直行业配置管理技术实现指南

## 概述
本文档描述了如何在Odoo 19系统中实现垂直行业模块的配置管理功能。通过 `res.config.settings` 模型，用户可以通过勾选选项来启用或禁用特定行业模块。

## 核心组件

### 1. 配置模型 (res.config.settings)
在 `farm_core` 模块中创建配置模型：

```python
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # 垂直行业模块配置选项
    module_farm_field_crops = fields.Boolean(
        string='大田作物管理',
        help='管理大田作物地块、播种收割、机械作业等功能'
    )
    module_farm_protected_cultivation = fields.Boolean(
        string='设施农业管理',
        help='管理温室大棚环境控制、水肥一体化、温湿度监控等功能'
    )
    module_farm_orchard_horticulture = fields.Boolean(
        string='果树园艺管理',
        help='管理果树剪枝记录、花期管理、采摘跟踪、年轮周期等功能'
    )
    module_farm_livestock = fields.Boolean(
        string='畜牧养殖管理',
        help='管理种畜档案、健康记录、配种管理、个体识别等功能'
    )
    module_farm_aquaculture = fields.Boolean(
        string='水产养殖管理',
        help='管理水产水质监测、投喂管理、生长跟踪、溶氧/pH监控等功能'
    )
    module_farm_medicinal_plants = fields.Boolean(
        string='中药材管理',
        help='管理中药材GMP合规、有效成分追踪、合规认证等功能'
    )
    module_farm_mushroom = fields.Boolean(
        string='食用菌管理',
        help='管理食用菌多批次栽培、环境控制、收获记录、多茬次跟踪等功能'
    )
    module_farm_apiculture = fields.Boolean(
        string='蜂业管理',
        help='管理蜂群管理、蜂箱定位、蜜源追踪、迁徙跟踪等功能'
    )
    module_farm_agricultural_processing = fields.Boolean(
        string='农产品加工管理',
        help='管理农产品配方、质量检验、包装追踪、批次继承等功能'
    )
    module_farm_agritourism = fields.Boolean(
        string='观光农业管理',
        help='管理资源预订、活动管理、会员服务、体验项目跟踪等功能'
    )
```

### 2. 配置视图 (XML)
创建配置视图，将字段组织到表单中：

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="res_config_settings_view_form" model="ir.ui.view">
        <field name="name">res.config.settings.view.form.inherit.farm.core</field>
        <field name="model">res.config.settings</field>
        <field name="inherit_id" ref="base.res_config_settings_view_form"/>
        <field name="arch" type="xml">
            <xpath expr="//div[hasclass('settings')]" position="inside">
                <div class="app_settings_block" data-string="Agricultural Industry Modules" string="农业垂直行业模块">
                    <h2>垂直行业配置</h2>
                    <div class="row mt16 o_settings_container">
                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_field_crops"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_field_crops"/>
                                <div class="text-muted">
                                    管理大田作物地块、播种收割、机械作业等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_protected_cultivation"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_protected_cultivation"/>
                                <div class="text-muted">
                                    管理温室大棚环境控制、水肥一体化、温湿度监控等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_orchard_horticulture"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_orchard_horticulture"/>
                                <div class="text-muted">
                                    管理果树剪枝记录、花期管理、采摘跟踪、年轮周期等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_livestock"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_livestock"/>
                                <div class="text-muted">
                                    管理种畜档案、健康记录、配种管理、个体识别等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_aquaculture"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_aquaculture"/>
                                <div class="text-muted">
                                    管理水产水质监测、投喂管理、生长跟踪、溶氧/pH监控等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_medicinal_plants"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_medicinal_plants"/>
                                <div class="text-muted">
                                    管理中药材GMP合规、有效成分追踪、合规认证等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_mushroom"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_mushroom"/>
                                <div class="text-muted">
                                    管理食用菌多批次栽培、环境控制、收获记录、多茬次跟踪等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_apiculture"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_apiculture"/>
                                <div class="text-muted">
                                    管理蜂群管理、蜂箱定位、蜜源追踪、迁徙跟踪等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_agricultural_processing"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_agricultural_processing"/>
                                <div class="text-muted">
                                    管理农产品配方、质量检验、包装追踪、批次继承等功能
                                </div>
                            </div>
                        </div>

                        <div class="col-12 col-lg-6 o_setting_box">
                            <div class="o_setting_left_pane">
                                <field name="module_farm_agritourism"/>
                            </div>
                            <div class="o_setting_right_pane">
                                <label for="module_farm_agritourism"/>
                                <div class="text-muted">
                                    管理资源预订、活动管理、会员服务、体验项目跟踪等功能
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </xpath>
        </field>
    </record>
</odoo>
```

### 3. 配置动作 (Action)
定义配置界面的访问入口：

```xml
<record id="action_farm_config_settings" model="ir.actions.act_window">
    <field name="name">行业配置</field>
    <field name="type">ir.actions.act_window</field>
    <field name="res_model">res.config.settings</field>
    <field name="view_mode">form</field>
    <field name="target">inline</field>
    <field name="context">{"module_name": "farm_core"}</field>
</record>

<menuitem id="menu_farm_config_settings"
          name="行业配置"
          parent="base.menu_administration"
          action="action_farm_config_settings"
          sequence="10"/>
```

## 实现步骤

### 步骤1: 创建新模块
创建 `farm_core` 模块来管理配置设置：
- 确保该模块被所有垂直行业模块依赖
- 作为配置管理的中心模块

### 步骤2: 实现配置模型
- 继承 `res.config.settings` 模型
- 为每个垂直行业模块添加布尔字段
- 使用 `module_` 前缀来标记模块依赖

### 步骤3: 创建配置视图
- 使用 XPath 扩展现有的配置界面
- 组织字段到逻辑分组
- 提供清晰的标签和帮助文本

### 步骤4: 设置依赖关系
- 配置模块间的依赖关系
- 确保启用特定行业时安装必要的依赖模块

### 步骤5: 测试配置流程
- 验证启用/禁用功能
- 确保模块安装/卸载按预期工作
- 验证数据的完整性

## 优势

1. **用户友好**: 通过简单的界面管理复杂的功能
2. **模块化**: 每个行业可以独立启用或禁用
3. **可扩展**: 易于添加新的行业模块
4. **标准化**: 遵循 Odoo 的配置管理标准
5. **灵活性**: 支持多行业的组合配置

## 注意事项

1. **数据迁移**: 启用行业模块时可能需要数据迁移
2. **权限管理**: 确保适当的访问权限控制
3. **依赖检查**: 验证模块依赖关系避免冲突
4. **性能影响**: 检查启用特定行业对系统性能的影响

## 模块重组与复合型态支持

为支持复合型农业经营模式，实现跨行业场景，需要对现有模块进行重组：

### 1. 核心共享模块重组
将现有通用功能重构为跨行业共享的模块：

```python
# farm_core 模块 - 通用基础数据
class LandParcel(models.Model):
    _inherit = 'stock.location'  # 继承基础库位

    industry_type = fields.Selection([
        ('field_crops', '大田作物'),
        ('protected_cultivation', '设施农业'),
        ('orchard', '果树园艺'),
        ('aquaculture', '水产养殖'),
        ('mixed', '复合型')
    ], string='行业类型')

    # 根据行业类型显示不同字段
    field_crop_specific_field = fields.Char('大田作物特有字段',
                                          compute='_compute_industry_fields',
                                          inverse='_inverse_industry_fields')
    orchard_specific_field = fields.Char('果树园艺特有字段',
                                       compute='_compute_industry_fields',
                                       inverse='_inverse_industry_fields')

# farm_operation 模块 - 通用作业管理
class FarmingOperation(models.Model):
    _inherit = 'project.task'  # 继承项目任务

    operation_type = fields.Selection([
        ('planting', '种植'),
        ('harvesting', '收获'),
        ('feeding', '投喂'),
        ('processing', '加工'),
        ('tourism', '观光服务'),
    ], string='作业类型')

    industry_specific_params = fields.Json('行业特有参数')
```

### 2. 行业专用模块设计
创建行业专用模块来扩展通用功能：

```python
# farm_field_crops 模块 - 大田作物专用
class FieldCropsOperation(models.Model):
    _name = 'farm.field.crops.operation'
    _inherits = {'project.task': 'operation_id'}

    operation_id = fields.Many2one('project.task', required=True, ondelete='cascade')

    # 大田作物特有字段
    seeding_rate = fields.Float('播种密度')
    fertilizer_application = fields.Float('施肥量')
    irrigation_schedule = fields.Char('灌溉计划')

# farm_agritourism 模块 - 观光农业专用
class AgritourismOperation(models.Model):
    _name = 'farm.agritourism.operation'
    _inherits = {'project.task': 'operation_id'}

    operation_id = fields.Many2one('project.task', required=True, ondelete='cascade')

    # 观光农业特有字段
    visitor_count = fields.Integer('访客数量')
    activity_type = fields.Selection([
        ('field_visit', '田间参观'),
        ('harvest_experience', '采摘体验'),
        ('processing_tour', '加工过程参观'),
    ], string='活动类型')
```

### 3. 配置依赖关系
更新配置模型以处理行业间的依赖关系：

```python
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # 基础行业模块
    module_farm_field_crops = fields.Boolean(
        string='大田作物管理',
        help='管理大田作物地块、播种收割、机械作业等功能'
    )
    module_farm_agritourism = fields.Boolean(
        string='观光农业管理',
        help='管理资源预订、活动管理、会员服务、体验项目跟踪等功能'
    )

    # 复合行业依赖检查
    @api.onchange('module_farm_field_crops', 'module_farm_agritourism')
    def _onchange_composite_industry_check(self):
        if self.module_farm_field_crops and self.module_farm_agritourism:
            # 如果同时启用大田作物和观光农业，提示复合场景
            self.env.user.notify_info(
                message="检测到复合行业配置：大田作物 + 观光农业。系统将启用农旅结合功能。"
            )

    def set_values(self):
        super().set_values()
        # 触发复合行业场景的特殊配置
        if self.module_farm_field_crops and self.module_farm_agritourism:
            self._setup_agritourism_composite_scenario()

    def _setup_agritourism_composite_scenario(self):
        """设置农旅结合场景的特殊配置"""
        # 启用农旅结合相关的业务流程
        # 创建农旅结合的默认工作流
        # 配置界面显示农旅结合专用选项
        pass
```

### 4. 界面动态适配
根据启用的行业动态调整用户界面：

```xml
<!-- 在视图中根据启用的行业模块动态显示字段 -->
<record id="view_farm_operation_form" model="ir.ui.view">
    <field name="name">farm.operation.form.composite</field>
    <field name="model">project.task</field>
    <field name="inherit_id" ref="project.view_task_form2"/>
    <field name="arch" type="xml">
        <xpath expr="//group[@name='extra_info']" position="inside">
            <group name="field_crops_group"
                   invisible="not context.get('show_field_crops_fields', False)">
                <field name="seeding_rate"/>
                <field name="fertilizer_application"/>
            </group>
            <group name="agritourism_group"
                   invisible="not context.get('show_agritourism_fields', False)">
                <field name="visitor_count"/>
                <field name="activity_type"/>
            </group>
        </xpath>
    </field>
</record>
```

### 5. 权限控制重组
为复合行业场景设置精细的权限控制：

```python
# 定义复合行业相关的权限组
class IrModuleCategory(models.Model):
    _inherit = 'ir.module.category'

    # 为复合行业场景创建权限组
    composite_industry_access = fields.Boolean('复合行业访问权限')

# 权限规则设置
class IrRule(models.Model):
    _inherit = 'ir.rule'

    def _compute_domain(self, model_name, mode="read"):
        # 根据用户启用的行业模块限制数据访问
        if model_name == 'project.task':
            enabled_industries = self.env.user.get_enabled_industries()
            if 'agritourism' not in enabled_industries:
                # 限制观光农业相关数据的访问
                pass
        return super()._compute_domain(model_name, mode)
```

### 6. 现有模块适配策略
为将当前系统中的模块适配到新的配置管理模式，需要以下迁移策略：

#### 6.1 当前模块重组
根据 MODULE_PLAN.md 中的现有模块结构，进行以下重组：

**基础模块适配**:
- **`farm_core`**: 保持为通用数据层，扩展支持行业类型标识
- **`farm_operation`**: 重构为通用作业管理层，支持多行业作业类型
- **`farm_iot`**: 保持为通用IoT管理层，扩展设备类型支持
- **`farm_mobile`**: 重构为动态界面层，根据启用行业显示相应功能

**业务模块拆分**:
- **`farm_livestock`** → `farm_livestock` (专用) + 通用功能并入 `farm_operation`
- **`farm_breeding`** → `farm_breeding` (专用) + 通用功能并入 `farm_livestock`
- **`farm_processing`** → `farm_agricultural_processing` (新命名) + 通用功能并入 `farm_operation`
- **`farm_agritourism`** → 保持为专用模块
- **`farm_aquaculture`** → 新增模块，继承通用功能
- **`farm_orchard`** → 新增模块，继承通用功能

#### 6.2 迁移脚本示例
```python
# 数据库迁移脚本示例
def migrate_to_configurable_modules(env):
    """将现有模块配置迁移到新的配置管理模式"""

    # 1. 识别当前启用的模块功能
    current_modules = get_current_module_usage(env)

    # 2. 基于现有数据推断行业类型
    industry_types = infer_industry_from_data(env, current_modules)

    # 3. 更新配置设置
    config = env['res.config.settings'].create({
        'module_farm_field_crops': 'farm_operation' in current_modules,
        'module_farm_livestock': 'farm_livestock' in current_modules,
        'module_farm_agritourism': 'farm_agritourism' in current_modules,
        'module_farm_agricultural_processing': 'farm_processing' in current_modules,
    })

    # 4. 更新现有数据的行业类型标识
    update_land_parcels_with_industry_type(env, industry_types)

    # 5. 调整权限设置
    adjust_permissions_for_industries(env, industry_types)

def map_existing_fields_to_industry_specific(env):
    """将现有字段映射到行业特有字段"""

    # 对于大田作物相关的数据
    field_data = env['project.task'].search([
        ('task_type', 'in', ['planting', 'harvesting', 'fertilizing'])
    ])

    for task in field_data:
        # 创建大田作物特有数据
        env['farm.field.crops.operation'].create({
            'operation_id': task.id,
            'seeding_rate': task.get('seeding_rate', 0),
            'fertilizer_application': task.get('fertilizer_amount', 0),
        })

    # 对于观光农业相关的数据
    tourism_data = env['project.task'].search([
        ('task_type', 'in', ['event_management', 'visitor_service'])
    ])

    for task in tourism_data:
        # 创建观光农业特有数据
        env['farm.agritourism.operation'].create({
            'operation_id': task.id,
            'visitor_count': task.get('visitor_count', 0),
            'activity_type': task.get('activity_type', 'field_visit'),
        })
```

#### 6.3 向后兼容性保证
- **API兼容**: 保持现有API端点的兼容性
- **数据库兼容**: 通过继承和视图保持数据结构向下兼容
- **界面兼容**: 逐步迁移界面，确保用户不会遇到突然的功能缺失
- **业务流程兼容**: 保持核心业务流程不变，仅在后台进行模块重组

### 7. 实施建议
- **分阶段实施**: 先实现基础模块重组，再添加复合行业支持
- **向后兼容**: 确保现有功能在重组后继续正常工作
- **数据迁移**: 为现有数据设计迁移脚本以适应新的模块结构
- **测试覆盖**: 对复合行业场景进行全面测试
- **用户培训**: 为管理员提供配置管理的培训材料
- **文档更新**: 更新所有相关技术文档以反映新的架构