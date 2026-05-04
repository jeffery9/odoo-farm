#!/usr/bin/env python3
"""
基于现有的 icon.svg 动态合成 banner.svg，并填充清单内的模块名称和所属领域的 Slogan。
提取 icon.svg 的路径 (Motif)，嵌入 banner 的相框。
"""
import os
import re
import xml.sax.saxutils as saxutils

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
# Banner Template
TEMPLATE_BANNER = os.path.expanduser("~/my-skills/odoo-appstore-branding/assets/templates/banner_base.svg")

CATEGORIES = {
    "crop": ["crop", "floriculture", "mushroom", "orchard", "cultivation", "seed", "viticulture", "medicinal", "land", "horticulture", "agri_science"],
    "livestock": ["livestock", "apiculture", "aquaculture", "breeding", "symbiosis"],
    "financial": ["financ", "valuation", "insurance", "subsidy", "exchange"],
    "iot": ["iot", "weather", "green_monitor", "greenhouse", "agri_iot", "precision_production_iot"],
    "supply": ["supply", "logistics", "sale", "pos", "marketing", "procurement"],
    "quality": ["quality", "cert", "label", "safety", "input_reg"],
    "esg": ["esg", "ecology", "waste", "disaster", "crisis"],
    "ai": ["ai_", "precision", "knowledge", "decision", "vision", "agent"],
    "hr": ["hr", "training"],
    "equipment": ["equipment", "machinery", "robotics"],
    "processing": ["processing", "mrp", "fermentation", "winery"],
    "industry": ["multi_farm", "isl", "agritourism", "live_streaming"],
    "core": ["core", "dashboard", "ux", "mobile", "operation", "planning", "entity_reg"]
}

SLOGANS = {
    "crop": "全生命周期种植追踪 / Full Cycle Tracking", "livestock": "智慧养殖与谱系追踪 / Smart Breeding",
    "financial": "产融结合与风险穿透 / Industry-Finance Integration", "iot": "实时感知与自动化控制 / Real-time Sensing",
    "supply": "农资农产品全链协同 / Supply Chain Collaboration", "quality": "溯源体系与食品安全 / Traceability &amp; Safety",
    "esg": "碳汇追踪与可持续发展 / Carbon &amp; Sustainability", "ai": "机器视觉与决策大脑 / Vision &amp; Decision Brain",
    "hr": "劳务排班与技能考核 / Labor &amp; Training", "equipment": "资产生命周期与精细维保 / Asset Lifecycle",
    "processing": "增值转化与批次管理 / Value-added Transformation", "industry": "垂直场景与商业闭环 / Vertical Scenarios",
    "core": "现代农业数字底座 / Digital Foundation"
}

def determine_category(mod_dir):
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in mod_dir:
                return cat
    return "core"

def get_module_name(mod_dir):
    manifest_path = os.path.join(BASE_DIR, mod_dir, "__manifest__.py")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r"'name'\s*:\s*['\"]([^'\"]+)['\"]", content)
                if match:
                    return saxutils.escape(match.group(1))
        except Exception:
            pass
    return saxutils.escape(" ".join(word.capitalize() for word in mod_dir.replace("farm_", "").split("_")))

def extract_icon_motif(icon_path):
    with open(icon_path, 'r', encoding='utf-8') as f:
        content = f.read()
    svg_inner = re.search(r'<svg[^>]*>(.*?)</svg>', content, re.DOTALL | re.IGNORECASE)
    if not svg_inner: return ""
    inner_str = svg_inner.group(1)
    # 剔除底座
    inner_str = re.sub(r'<rect[^>]*width="256"[^>]*height="256"[^>]*fill="#FFF9F2"[^>]*/>', '', inner_str, flags=re.IGNORECASE)
    return inner_str.strip()

if __name__ == "__main__":
    if not os.path.exists(TEMPLATE_BANNER):
        print(f"Error: Base banner template not found at {TEMPLATE_BANNER}")
        exit(1)

    with open(TEMPLATE_BANNER, 'r', encoding='utf-8') as f:
        banner_template_content = f.read()

    modules = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and os.path.exists(os.path.join(BASE_DIR, d, "__manifest__.py"))])

    sh_path = os.path.join(os.path.dirname(__file__), "convert_commands.sh")
    with open(sh_path, "w") as convert_sh:
        convert_sh.write("#!/bin/bash\n")
        
        count = 0
        for mod in modules:
            icon_path = os.path.join(BASE_DIR, mod, "static/description/icon.svg")
            target_banner = os.path.join(BASE_DIR, mod, "static/description/banner.svg")

            if not os.path.exists(icon_path): continue
            motif_content = extract_icon_motif(icon_path)
            if not motif_content: continue
            
            motif_content = motif_content.replace('\\', '\\\\')

            cat = determine_category(mod)
            mod_name = get_module_name(mod)
            slogan = SLOGANS.get(cat, SLOGANS["core"])

            new_banner = banner_template_content
            # 注入 Motif
            new_banner = re.sub(
                r'(<g transform="translate\(51,\s*103\)\s*scale\(0\.42\)">)(.*?)(</g>)', 
                r'\g<1>\n' + motif_content + r'\n\g<3>', 
                new_banner, 
                flags=re.DOTALL
            )
            # 注入文本标题
            new_banner = re.sub(r'(<text[^>]*font-size="26"[^>]*>)(.*?)(</text>)', r'\g<1>' + mod_name + r'\g<3>', new_banner, flags=re.DOTALL)
            new_banner = re.sub(r'(<text[^>]*font-size="14"[^>]*>)(.*?)(</text>)', r'\g<1>' + slogan + r'\g<3>', new_banner, flags=re.DOTALL)
            # 兜底替换
            new_banner = re.sub(r'模块完整名称 \| Module Title', mod_name, new_banner)
            new_banner = re.sub(r'核心价值描述与业务痛点解决 / Slogan', slogan, new_banner)

            with open(target_banner, 'w', encoding='utf-8') as f:
                f.write(new_banner)

            convert_sh.write(f'python3 ~/my-skills/odoo-appstore-branding/scripts/convert_assets.py {mod}/static/description/icon.svg {mod}/static/description/icon.png -w 256 -H 256\n')
            convert_sh.write(f'python3 ~/my-skills/odoo-appstore-branding/scripts/convert_assets.py {mod}/static/description/banner.svg {mod}/static/description/banner.png -w 628 -H 314\n')
            convert_sh.write(f'cp {mod}/static/description/banner.png {mod}/static/description/main_screenshot.png\n')
            count += 1
            
    os.chmod(sh_path, 0o755)
    print(f"Rebuilt banners for {count} modules. Conversion commands saved to {sh_path}.")
