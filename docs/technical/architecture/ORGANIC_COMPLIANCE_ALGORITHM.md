# 有机合规与黑名单实时校验算法 (Organic Compliance Checker)

## 算法目的
在农事作业录入阶段，实时校验投入品是否符合有机或特定绿色认证标准，防止违规化学品进入生产环节导致认证失效。

## 输入参数
- `project_id`: 目标地块所属项目 (Integer)
- `product_id`: 拟使用的投入品 ID (Integer)
- `certification_standards`: 当前激活的认证标准列表 (List[String])

## 输出结果
- `is_compliant`: 是否合规 (Boolean)
- `forbidden_substances`: 检出的禁用成分 (List[String])
- `audit_log_id`: 审计记录 ID (Integer)

## 算法流程
1. **获取标准**: 提取项目定义的认证类型（如：有机、GlobalG.A.P.）。
2. **成分穿透**: 读取 `product.product` 的 `aquaculture_composition`（化学成分）字段。
3. **黑名单比对**: 将产品成分与对应认证标准的 `forbidden_substances_registry` 进行字符串模糊或正则匹配。
4. **状态判定**:
   - 若匹配成功：`is_compliant = False`，并抛出 `ValidationError`。
   - 若匹配失败：允许记录并标记为“绿色合规”。
5. **审计存证**: 无论是否合规，必须在后台 `farm.compliance.log` 记录校验痕迹。

## 具体实现 (Implementation)
```python
import re
from odoo.exceptions import ValidationError

def check_organic_compliance(product, project):
    """
    实时校验投入品合规性
    product: product.product 记录对象
    project: project.project 记录对象
    """
    # 1. 识别项目认证标准 (例如: 'organic', 'green_food')
    cert_type = project.certification_type
    if not cert_type or cert_type == 'conventional':
        return True, []

    # 2. 获取该标准下的禁用物质黑名单 (正则表达式列表)
    # 示例: [r'glyphosate', r'carbofuran', r'paraquat']
    blacklist = project.certification_id.forbidden_substances_registry.split(',')
    blacklist = [item.strip().lower() for item in blacklist if item.strip()]

    # 3. 穿透产品成分字段
    composition = (product.aquaculture_composition or "").lower()
    
    # 4. 执行匹配检查
    detected = []
    for substance in blacklist:
        if re.search(r'\b' + re.escape(substance) + r'\b', composition):
            detected.append(substance)

    if detected:
        # 抛出异常执行硬拦截
        raise ValidationError(
            f"Compliance Error: Product '{product.display_name}' contains "
            f"forbidden substances: {', '.join(detected)} for {cert_type} standard."
        )

    return True, []
```

## 业务规则
- **硬拦截**: 合规校验失败必须阻止 `mrp.production` 或 `intervention` 任务的状态流转。
- **动态更新**: 黑名单库更新后，系统需自动对处于“转换期”的批次进行追溯检查。

## 验证方法
- 使用已知含禁用物质（如克百威）的物料进行录入测试，验证拦截效果。

## 性能指标
- 校验延迟 < 200ms。
- 误报率 0%。