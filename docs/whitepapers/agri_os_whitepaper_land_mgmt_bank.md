# 🌌 Agri-OS 农业计算引擎学术白皮书：2w. 土地银行、确权流转租赁与地力轮作管理端到端可计算解决方案 (Land Banking, Leaseback Contracts & Soil Rotation Health)

> **学术与工业发布级别**: [PUBLIC RELEASE / OPEN-SOURCE]
> **参考设计体系**: Computable Smart Agri-OS V19.0CE (ISA-88 Batch Control)
> **脱敏状态**: 已通过物理防泄密检验，所有调试密钥及开发日志已完全安全隔离

---

## 🏛️ 1. 行业宏观背景与第一性原理挑战 (Industry Background)

在推进农业现代化集约经营与深化农村土地制度改革的宏观浪潮中，**村集体“土地银行（Land Banking）”、农村土地确权、流转租赁（Leasing & Leaseback）与大田轮作土壤地力管理（Soil Rotation Health）** 构成了农业操作系统最底层、最核心的资产底盘。农村土地具有“三权分置（Ownership, Contract Right, Use Right）”的中国特色独特物理与政策属性。在建设规模化农场和合作社时，面临着以下三大底层第一性原理计算与治理挑战：

1.  **分散家庭承包地块的数字化“确权-流转”时空碰撞（Fragmented Land Rights & Boundary Overlaps）**：中国农村承包地高度零碎、边界不规则。在将成百上千户散农地块流转并入大户或“土地银行”统一经营时，如果系统不能基于 PostGIS 高维空间多边形（Polygon WKT）对承包权、经营权进行矢量级拓扑校验（Overlap / Boundary Auditing），极易发生租金计费纠纷和地籍地界物理交叉碰撞的诉讼事故。
2.  **长期流转过程中的地力耗竭与重金属毒害（Soil Degradation & Chemical Depletion）**：大户在长期租赁经营中，极易发生掠夺性掠夺性种植（如连年重茬单一种植），导致土壤有机质骤降、缺素症暴发以及有害农药/重金属物理残留。如何将土地资产卡片（`land_mgmt`）与每季土壤化验档案（`agri_land_health_record`）和多轮作历史（`agri_land_crop_rotation_history`）在数据链条上进行强行闭合审计，是绿色有机农业合规的先决防线。
3.  **“土地回租返包”资金流与租赁合同周期的智能对账（Financial Capital Flow & Leasing Recalculation）**：村集体土地银行的运作涉及极为复杂的“散户存地给租 -> 集体平整大田 -> 大户返包交租”的双向回租（Leaseback）现金流。资金利息、阶梯保底收益、与种植合同履约周期的多维联动，对传统静态核算造成了极大的对账阻碍。

**Computable Agri-OS** 的 `farm_land_mgmt` 模块，通过构建以 `agri.land.mgmt` 为核心的空间资产实体、`agri.land.leaseback` 土地银行流转凭证，并超链 `agri.land.health.record` 地力化验链条，完美解决了土地资源、资产、资金（三资）的三维级联可计算性。本白皮书将对该解决方案的底层地籍拓扑、土壤健康评估和土地银行 SOP 规程进行公开学术披露。

---

## 🎨 土地银行确权与地力轮作管理控制总线 (ASCII Topology Graph)

```text
+==========================================================================================+
|                           Agri-OS 土地银行确权、流转与地力轮作控制中枢                      |
+==========================================================================================+
|  [ 1. 承包户散地登记 ] ────► [ 2. 土地银行平整整合 ] ────► [ 3. 租约与回租合同 ] ──► [ 4. 轮作审计 ] |
|   - 录入物理边界 WKT Polygon  - 自动拓扑重叠校验（PostGIS）  - 自动核算保底/阶梯租金  - 限制作物连作 |
|                                                                                       - 检测土壤重金属|
|                                                                                              │ |
|                                                                                              ▼ |
|  [ 有机作物高溢价销售 ] ◄──── [ 自动触发绿色准入 ] ◄────── [ 地力化验: Health Record ] ◄─────┘ |
|   - 链向溯源 Lot 护照          - 有机质/pH/重金属达标校验    - 自动化验指标容差范围拦截          |
+==========================================================================================+
```

---

## 2w.1 土地确权登记、流转与土地银行运作 (Land Registry & Banking)

土地确权是流转的前提。系统利用空间网格化地图，建立合规的“三权”数字账册。

### 2w.1.1 土地存入流转与返包返租操作规程 (SOP)

1.  **承包地物理确权登记**：
    *   登录 Agri-OS，导航至“地籍流转控制 -> 土地台账”菜单，点击“新建”。系统自动初始化土地卡片编码（如：`LAND-PARCEL-D04`）。
    *   录入土地四至边界、承包户姓名（res.partner）、承包确权面积。在“空间边界（`spatial_polygon`）”中录入标准 WKT 多边形坐标（如 `POLYGON((X1 Y1, X2 Y2, ...))`）。
2.  **存入土地银行流转凭证**：
    *   导航至“土地回租合同”菜单，点击“新建”。
    *   合同类型选择 `存入（leaseback）`，关联土地银行载体（res.partner），录入保底年租金及阶梯收益比例，触发并生成租金计付流水账。
3.  **大户连片返包出租**：
    *   大户承租连片整合地块时，系统自动检索所选格网，并调用 PostGIS 进行空间求并（Union）及无缝边界碰撞校验。
    *   合同类型选择 `返包（sublease）`，关联大户账号，锁定租约周期、租金账期。点击“生效”，自动释放地块的“经营使用权”给对应的种植业务部门。

---

## 2w.2 土壤健康化验档案与地力容差控制模型 (Soil Health Records)

土地不能“越种越瘦”，系统将每次大宗化验指标以 GxP 品控级别存储。

### 2w.2.1 土壤理化指标限值安全拦截 (Soil Metric Gating)

在 `agri.land.health.record` 模型中，系统内置了对重金属（铅 Pb、镉 Cd、汞 Hg、砷 As）及理化核心指标（有机质含量、pH 值）的安全限值约束。

例如，若该地块被标记为 `有机农产品认证保护区 (organic_certified)`，其土壤重金属化验极限值执行国家 GB 15618-2018 严格二级标准（例如：铅 $\le 50.0\text{ mg/kg}$，镉 $\le 0.3\text{ mg/kg}$）。

系统重金属毒性超标判定算子 $F_{toxic}$ 定义如下：

$$F_{toxic} = \sum \max\left(0.0, \frac{\text{Measured Value}_i - \text{Limit}_i}{\text{Limit}_i}\right)$$

如果 $F_{toxic} > 0.0$（即任何一项重金属超标），系统在 `action_verify_health()` 接口中判定该地力档案异常。

通过 **Odoo @api.constrains** 强力约束，一旦判定地块土壤异常，系统将自动抛出 `UserError` 锁死该地块，并将地块的种植准入等级（`planting_permission_level`）自动降级为 `禁止种植（blocked）` 或 `休耕净化（fallow）`，从源头上切断了受重金属污染土壤种出“毒大米/毒药材”流入市场的社会灾难。

---

## 2w.3 作物多轮作历史历史与病害自动预警 (Crop Rotation & Disease Alerts)

连作重茬会导致严重的土传病害（Soil-borne Diseases）。

### 2w.3.1 连续重茬（Monoculture）预警代码逻辑

`agri.land.crop.rotation.history` 模型在作物播种下单（`farm_crop` 的 `action_sow`）时，自动检索该地块历年的轮作历史记录，执行以下前哨硬核校验：

```python
    @api.model
    def check_monoculture_risk(self, land_parcel_id, incoming_crop_category):
        """
        Crop Monoculture Defensive Gating: Query historical crop rotation records for the selected land parcel.
        If the same crop category has been planted continuously for more than 2 consecutive cycles,
        automatically raise a high-risk warning and block production order dispatch 
        to prevent severe soil-borne disease outbreaks.
        """
        two_years_ago = fields.Date.today() - timedelta(days=730)
        history = self.search([
            ('land_parcel_id', '=', land_parcel_id),
            ('sow_date', '>=', two_years_ago),
        ], order='sow_date desc')
        
        continuous_count = 0
        for record in history:
            if record.crop_category_id.id == incoming_crop_category:
                continuous_count += 1
            else:
                break  # Crop rotation detected, rotation chain is healthy
                
        if continuous_count >= 2:
            raise UserError(_(
                "MONOCULTURE CROPPING BLOCKED:\n"
                "Land Parcel '%s' has been continuous cropped with '%s' for %s cycles. "
                "Agri-OS agronomical rules require immediate crop rotation (e.g., planting legumes) "
                "to restore soil nitrogen and suppress pathogens."
            ) % (
                self.env['agri.land.mgmt'].browse(land_parcel_id).name,
                self.env['product.category'].browse(incoming_crop_category).name,
                continuous_count
            ))
```

此防御机制是**智慧农场的“农学机理守护者”**。它强制推动大田农户采取“豆科（Legumes）固氮轮作制”或“休闲轮作制”，从软件系统层用**硬逻辑编织了地力保护与土传病害物理控制防线**，保障了土地银行托管资产的长期公允收益与绿色有机主粮生态的安全续航。

---

> **Agri-OS Land Management & Banking Solution Sheet | Highly Computable | Soil Agronomy Guard**
