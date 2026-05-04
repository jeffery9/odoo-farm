import os
import re
import subprocess
import xml.sax.saxutils as saxutils

WORKSPACE = "/Users/jeffery/odoo-farm-dev"
CONVERT_SCRIPT = "/Users/jeffery/.gemini/skills/odoo-appstore-branding/scripts/convert_assets.py"

# ALL 12 Motifs are now pure 256x256 flat circles. No external transforms needed.
MASTER_MOTIFS = {
    'core': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <g transform="translate(68, 68) scale(1.2)">
            <g transform="translate(0, 50)">
                <path d="M5,25 L95,25 L95,45 L5,45 Z" fill="white" opacity="0.2"/>
                <path d="M5,25 L95,25 L95,45 L5,45 Z" fill="none" stroke="white" stroke-width="2" opacity="0.6"/>
                <path d="M25,5 L75,5 L75,25 L25,25 Z" fill="white" opacity="0.5"/>
                <path d="M25,5 L75,5 L75,25 L25,25 Z" fill="none" stroke="white" stroke-width="2" opacity="0.8"/>
                <line x1="50" y1="5" x2="50" y2="45" stroke="white" stroke-width="2" opacity="0.5"/>
            </g>
            <g transform="translate(0, -10)">
                <path d="M50,60 L50,15" stroke="white" stroke-width="4" stroke-linecap="round"/>
                <path d="M50,45 C50,20 65,10 80,10 C80,30 65,40 50,45 Z" fill="#C9382B" stroke="white" stroke-width="2"/>
                <path d="M50,45 C50,25 35,15 20,15 C20,35 35,45 50,45 Z" fill="white"/>
            </g>
        </g>
    ''',
    'precision': '''
        <circle cx="128" cy="128" r="80" stroke="#8D6E63" stroke-width="10" fill="none" stroke-dasharray="20,10"/>
        <line x1="128" y1="20" x2="128" y2="50" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>
        <line x1="128" y1="206" x2="128" y2="236" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>
        <line x1="20" y1="128" x2="50" y2="128" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>
        <line x1="206" y1="128" x2="236" y2="128" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>
        <path d="M128,155 C100,155 80,130 80,110 C80,90 100,80 128,80 C156,80 176,90 176,110 C176,130 156,155 128,155 Z" fill="#C9382B"/>
        <circle cx="128" cy="110" r="10" fill="white"/>
    ''',
    'livestock': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M80,100 C60,60 100,20 128,40 C156,20 196,60 176,100" fill="none" stroke="white" stroke-width="12" stroke-linecap="round"/>
        <circle cx="128" cy="140" r="45" fill="white"/>
        <circle cx="108" cy="135" r="6" fill="#C9382B"/>
        <circle cx="148" cy="135" r="6" fill="#C9382B"/>
        <rect x="180" y="60" width="30" height="20" rx="4" fill="#8D6E63" transform="rotate(15 180 60)"/>
    ''',
    'crop': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M128,210 L128,50" stroke="white" stroke-width="12" stroke-linecap="round"/>
        <path d="M128,80 C170,80 180,40 128,20 C76,40 86,80 128,80 Z" fill="white"/>
        <path d="M128,140 C170,140 180,100 128,80 C76,100 86,140 128,140 Z" fill="white" opacity="0.8"/>
    ''',
    'iot': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M128,210 L128,90" stroke="white" stroke-width="15" stroke-linecap="round"/>
        <circle cx="128" cy="70" r="20" fill="white"/>
        <path d="M80,110 Q128,60 176,110" fill="none" stroke="white" stroke-width="10" stroke-linecap="round" opacity="0.6"/>
    ''',
    'finance': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <rect x="70" y="140" width="30" height="40" rx="4" fill="white" opacity="0.5"/>
        <rect x="110" y="110" width="30" height="70" rx="4" fill="white" opacity="0.8"/>
        <rect x="150" y="70" width="30" height="110" rx="4" fill="white"/>
        <path d="M60,150 L110,120 L150,130 L200,60" fill="none" stroke="white" stroke-width="10" stroke-linecap="round"/>
    ''',
    'supply': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M80,80 L176,80 L176,176 L80,176 Z" fill="none" stroke="white" stroke-width="12" stroke-linejoin="round"/>
        <path d="M80,110 L176,110" stroke="white" stroke-width="12" stroke-linecap="round"/>
        <path d="M128,110 L128,176" stroke="white" stroke-width="12" stroke-linecap="round"/>
        <path d="M110,135 L120,145 L145,120" fill="none" stroke="white" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    ''',
    'processing': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <circle cx="128" cy="128" r="70" fill="none" stroke="white" stroke-width="12" stroke-dasharray="25,12"/>
        <circle cx="128" cy="128" r="25" fill="white"/>
        <path d="M128,70 L128,186 M70,128 L186,128" stroke="white" stroke-width="8" stroke-linecap="round"/>
    ''',
    'esg': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M128,50 A78,78 0 1,1 70,180" fill="none" stroke="white" stroke-width="15" stroke-linecap="round"/>
        <path d="M70,180 L50,150 M70,180 L100,165" stroke="white" stroke-width="15" stroke-linecap="round"/>
        <path d="M128,190 C170,190 170,130 128,100 C86,130 86,190 128,190 Z" fill="white"/>
    ''',
    'ux': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <rect x="60" y="80" width="136" height="96" rx="8" fill="none" stroke="white" stroke-width="10"/>
        <rect x="75" y="100" width="40" height="50" rx="4" fill="white" opacity="0.6"/>
        <rect x="125" y="100" width="55" height="15" rx="4" fill="white"/>
        <rect x="125" y="125" width="55" height="15" rx="4" fill="white" opacity="0.8"/>
    ''',
    'service': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <circle cx="128" cy="80" r="25" fill="white"/>
        <path d="M70,180 C70,140 186,140 186,180" fill="white"/>
    ''',
    'sale': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M70,80 L140,80 L180,120 L110,180 Z" fill="white"/>
        <circle cx="95" cy="105" r="8" fill="#C9382B"/>
    '''
}

MAPPING = {
    'precision': 'precision', 'ai': 'precision', 'robotics': 'precision', 'vision': 'precision', 'llm': 'precision',
    'core': 'core', 'isl': 'core', 'base': 'core', 'entity': 'core', 'land': 'core', 'management': 'core',
    'livestock': 'livestock', 'breed': 'livestock', 'health': 'livestock', 'aqua': 'livestock', 'fish': 'livestock', 'bee': 'livestock',
    'crop': 'crop', 'field': 'crop', 'plant': 'crop', 'greenhouse': 'crop', 'viticulture': 'crop', 'winery': 'crop', 'mushroom': 'crop',
    'financial': 'finance', 'valuation': 'finance', 'subsidy': 'finance', 'credit': 'finance', 'loan': 'finance', 'insurance': 'finance',
    'supply': 'supply', 'logistics': 'supply', 'procurement': 'supply', 'mrp': 'supply', 'inventory': 'supply',
    'processing': 'processing', 'agricultural_processing': 'processing', 'fermentation': 'processing',
    'esg': 'esg', 'carbon': 'esg', 'ecology': 'esg', 'waste': 'esg', 'safety': 'esg', 'compliance': 'esg', 'disaster': 'esg',
    'ux': 'ux', 'dashboard': 'ux', 'mobile': 'ux', 'live_streaming': 'ux',
    'training': 'service', 'hr': 'service', 'operation': 'service', 'planning': 'service', 'knowledge': 'service',
    'sale': 'sale', 'pos': 'sale', 'market': 'sale', 'exchange': 'sale', 'csa': 'sale', 'iot': 'iot'
}

def extract_value(content, key):
    match = re.search(fr"'{key}'\s*:\s*(['\"])(.*?)\1", content, re.DOTALL)
    if not match: match = re.search(fr'"{key}"\s*:\s*(["\'])(.*?)\1', content, re.DOTALL)
    return match.group(2) if match else None

count = 0
for item in os.listdir(WORKSPACE):
    module_path = os.path.join(WORKSPACE, item)
    manifest_path = os.path.join(module_path, "__manifest__.py")
    if not os.path.isdir(module_path) or not os.path.exists(manifest_path): continue

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f: content = f.read()
        
        name = extract_value(content, 'name') or item.replace('_', ' ').title()
        summary = extract_value(content, 'summary') or "Farm Ecosystem Module"
        
        family_key = 'core'
        for k, v in MAPPING.items():
            if k in item.lower():
                family_key = v
                break
                
        motif_svg = MASTER_MOTIFS[family_key]
        
        if len(name) > 30: name = name[:27] + "..."
        summary = summary.replace('\\n', ' ').replace('\n', ' ').replace('&', '&amp;')
        if len(summary) > 60: summary = summary[:57] + "..."
        name_xml, summary_xml = saxutils.escape(name), saxutils.escape(summary)
        
        desc_dir = os.path.join(module_path, "static", "description")
        os.makedirs(desc_dir, exist_ok=True)
        
        icon_svg_path = os.path.join(desc_dir, "icon.svg")
        icon_png_path = os.path.join(desc_dir, "icon.png")
        banner_svg_path = os.path.join(desc_dir, "banner.svg")
        banner_png_path = os.path.join(desc_dir, "banner.png")
        main_screenshot_path = os.path.join(desc_dir, "main_screenshot.png")
        
        # 1. ICON (No internal translation needed, drawn at 256x256 natively)
        icon_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" rx="40" fill="#FFF9F2"/>
    <rect width="246" height="246" x="5" y="5" rx="38" fill="none" stroke="#C9382B" stroke-width="2"/>
    {motif_svg}
</svg>'''
        with open(icon_svg_path, 'w', encoding='utf-8') as f: f.write(icon_content)
        
        # 2. BANNER (Uniform transform for perfectly centering ANY 256x256 native graphic into the 130x130 box)
        banner_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="628" height="314" viewBox="0 0 628 314" xmlns="http://www.w3.org/2000/svg">
  <rect width="628" height="314" fill="#FFF9F2" />
  <g transform="translate(320, -50) scale(0.85)" opacity="0.03">
    <path fill-rule="evenodd" fill="#C9382B" d="M 395,174 58,177 42,184 29,204 25,244 46,266 149,279 315,269 313,252 260,241 87,245 76,230 91,209 243,204 339,220 356,239 360,272 346,297 329,306 169,316 53,301 6,279 12,375 95,388 379,378 391,368 Z M 386,15 375,7 354,3 299,3 298,0 277,0 264,4 127,3 29,8 19,16 13,27 7,55 3,175 7,179 19,164 42,147 110,140 316,137 362,140 392,147 393,61 Z M 342,57 340,60 342,72 340,78 332,87 319,89 260,90 230,97 169,99 167,101 158,100 155,102 141,103 94,102 71,95 63,95 55,91 38,91 29,84 29,74 37,63 45,63 55,58 63,58 82,52 95,53 134,49 197,50 228,47 261,47 311,51 326,50 Z" />
  </g>
  <rect x="40" y="92" width="130" height="130" rx="20" fill="white" stroke="#C9382B" stroke-width="1" />
  
  <!-- Flawless mathematical center mapping: 256x256 scaled to ~115px -> translated into the 130px box -->
  <g transform="translate(48, 100) scale(0.45)">{motif_svg}</g>
  
  <g transform="translate(190, 150)">
    <text x="0" y="0" fill="#C9382B" font-family="'PingFang SC', 'Microsoft YaHei', 'SimHei', 'Source Han Sans CN', sans-serif" font-size="24" font-weight="bold">{name_xml}</text>
    <text x="0" y="42" fill="#8D6E63" font-family="'PingFang SC', 'Microsoft YaHei', 'SimHei', 'Source Han Sans CN', sans-serif" font-size="14">{summary_xml}</text>
  </g>
  <g transform="translate(540, 280) scale(0.1)">
    <path d="M605.1,55.8 L605.1,36.8 L626.6,36.8 L626.6,0 L649.1,0 L649.1,36.8 L681.9,36.8 L681.9,55.8 L649.1,55.8 L649.1,127.5 C649.1,137.2 655.2,142 667.4,142 C667.4,142 667.5,142 667.6,142 C673.2,142 678,140.8 681.9,138.4 L681.9,158.6 C676.3,160.9 670.7,162 665.1,162 C664.9,162 664.7,162 664.5,162 C661.5,162 658.3,161.6 654.9,160.9 C651.6,160.2 647.5,158.8 642.8,156.6 C638.1,154.5 634.2,150.8 631.2,145.5 C628.1,140.3 626.6,133.7 626.6,125.9 L626.6,55.8 L605.1,55.8 Z" fill="#00AC47"></path>
    <path d="M555.1,13.9 C555.1,6.2 561.3,0 569,0 L569.3,0 C576.9,0 583.1,6.2 583.1,13.9 C583.1,21.5 576.9,27.7 569.3,27.7 L569,27.7 C561.3,27.7 555.1,21.5 555.1,13.9 Z M558.1,167.8 L558.1,43 L581.1,43 L581.1,167.8 L558.1,167.8 Z" fill="#00AC47"></path>
    <path d="M429.6,168 L429.6,53.9 C446.9,45.3 464.7,41 482.8,41 C498.5,41 510.8,45.1 519.8,53.3 C528.7,61.5 533.1,72.9 533.1,87.5 L533.1,168 L510,168 L510,85.9 C510,78.6 508.2,72.8 504.4,68.6 C500.7,64.4 493.2,62.2 481.8,62.2 C471.7,62.2 461.9,63.7 452.6,66.8 L452.6,168 L429.6,168 Z" fill="#FE2C25"></path>
    <path d="M379.6,13.9 C379.6,6.2 385.8,0 393.5,0 L393.7,0 C401.4,0 407.6,6.2 407.6,13.9 C407.6,21.5 401.4,27.7 393.7,27.7 L393.5,27.7 C385.8,27.7 379.6,21.5 379.6,13.9 Z M382.6,167.8 L382.6,43 L405.6,43 L405.6,167.8 L382.6,167.8 Z" fill="#FE2C25"></path>
    <path d="M255.7,167.6 L255.7,55.3 C272.8,46.8 290.2,42.6 308.1,42.6 C323.6,42.6 335.7,46.6 344.4,54.7 C353.2,62.8 357.6,74 357.6,88.4 L357.6,167.6 L334.9,167.6 L334.9,86.8 C334.9,79.6 333.1,73.9 329.4,69.7 C325.7,65.6 318.3,63.5 307.1,63.5 C297.1,63.5 287.5,65 278.3,67.9 L278.3,167.6 L255.7,167.6 Z" fill="#2C83FC"></path>
  </g>
</svg>'''
        with open(banner_svg_path, 'w', encoding='utf-8') as f: f.write(banner_content)
        
        subprocess.run(["python", CONVERT_SCRIPT, icon_svg_path, icon_png_path, "-w", "256", "-H", "256"], check=True, capture_output=True)
        subprocess.run(["python", CONVERT_SCRIPT, banner_svg_path, banner_png_path, "-w", "628", "-H", "314"], check=True, capture_output=True)
        subprocess.run(["cp", banner_png_path, main_screenshot_path], check=True)
        count += 1
    except Exception as e: print(f"Failed {item}: {str(e)}")

print(f"Done! {count} modules successfully healed and perfectly aligned.")
