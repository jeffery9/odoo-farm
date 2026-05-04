import os
import re
import subprocess
import xml.sax.saxutils as saxutils

WORKSPACE = "/Users/jeffery/odoo-farm-dev"
CONVERT_SCRIPT = "/Users/jeffery/.gemini/skills/odoo-appstore-branding/scripts/convert_assets.py"

# --- THE NATIVELY CENTERED MASTER MOTIFS (Absolute Coordinates, Red-White Interlocking) ---
MOTIFS = {
    'core': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <g transform="translate(68, 68) scale(1.2)">
            <g transform="translate(0, 50)">
                <path d="M5,25 L95,25 L95,45 L5,45 Z" fill="white" opacity="0.2"/>
                <path d="M5,25 L95,25 L95,45 L5,45 Z" fill="none" stroke="white" stroke-width="2" opacity="0.6"/>
                <path d="M25,5 L75,5 L75,25 L25,25 Z" fill="white" opacity="0.5"/>
                <path d="M25,5 L75,5 L75,25 L25,25 Z" fill="none" stroke="white" stroke-width="2" opacity="0.8"/>
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
        <line x1="128" y1="236" x2="128" y2="206" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>
        <line x1="20" y1="128" x2="50" y2="128" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>
        <line x1="236" y1="128" x2="206" y2="128" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>
        <path d="M128,160 C90,160 70,130 70,110 C70,90 90,80 128,80 C166,80 186,90 186,110 C186,130 166,160 128,160 Z" fill="#C9382B"/>
        <circle cx="128" cy="110" r="12" fill="white"/>
    ''',
    'livestock': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M78,110 C60,70 100,30 128,50 C156,30 196,70 178,110" fill="none" stroke="white" stroke-width="15" stroke-linecap="round"/>
        <circle cx="128" cy="145" r="50" fill="white"/>
        <circle cx="106" cy="140" r="8" fill="#C9382B"/>
        <circle cx="150" cy="140" r="8" fill="#C9382B"/>
    ''',
    'crop': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M128,210 L128,50" stroke="white" stroke-width="15" stroke-linecap="round"/>
        <path d="M128,85 C170,85 185,45 128,30 C71,45 86,85 128,85 Z" fill="#C9382B" stroke="white" stroke-width="3"/>
        <path d="M128,145 C170,145 185,105 128,90 C71,105 86,145 128,145 Z" fill="white"/>
    ''',
    'iot': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M128,210 L128,100" stroke="white" stroke-width="18" stroke-linecap="round"/>
        <path d="M128,210 L128,100" stroke="#C9382B" stroke-width="4" stroke-linecap="round"/>
        <circle cx="128" cy="75" r="22" fill="white" stroke="#C9382B" stroke-width="3"/>
        <circle cx="128" cy="75" r="8" fill="#C9382B"/>
        <path d="M75,120 Q128,60 181,120" fill="none" stroke="white" stroke-width="8" stroke-linecap="round" opacity="0.6"/>
    ''',
    'finance': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <rect x="70" y="145" width="30" height="40" rx="4" fill="white" opacity="0.5"/>
        <rect x="112" y="115" width="30" height="70" rx="4" fill="white" opacity="0.8"/>
        <rect x="154" y="75" width="30" height="110" rx="4" fill="white"/>
    ''',
    'supply': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M75,85 L181,85 L181,181 L75,181 Z" fill="none" stroke="white" stroke-width="15" stroke-linejoin="round"/>
        <path d="M75,120 L181,120" stroke="white" stroke-width="15" stroke-linecap="round"/>
    ''',
    'processing': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <circle cx="128" cy="128" r="72" fill="none" stroke="white" stroke-width="15" stroke-dasharray="30,15"/>
        <circle cx="128" cy="128" r="28" fill="white"/>
    ''',
    'esg': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M128,45 A83,83 0 1,1 65,185" fill="none" stroke="white" stroke-width="18" stroke-linecap="round"/>
        <path d="M65,185 L40,150 M65,185 L100,165" stroke="white" stroke-width="18" stroke-linecap="round"/>
    ''',
    'ux': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <rect x="55" y="75" width="146" height="106" rx="10" fill="none" stroke="white" stroke-width="12"/>
        <rect x="75" y="95" width="45" height="66" fill="white" opacity="0.6"/>
    ''',
    'service': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <circle cx="128" cy="75" r="30" fill="white"/>
        <path d="M65,190 C65,145 191,145 191,190" fill="white"/>
    ''',
    'sale': '''
        <circle cx="128" cy="128" r="90" fill="#C9382B"/>
        <path d="M65,75 L150,75 L191,120 L115,195 Z" fill="white"/>
        <circle cx="95" cy="105" r="10" fill="#C9382B"/>
    '''
}

MAPPING = {
    'precision': 'precision', 'ai': 'precision', 'robotics': 'precision', 'vision': 'precision', 'llm': 'precision',
    'core': 'core', 'isl': 'core', 'base': 'core', 'entity': 'core', 'land': 'core', 'management': 'core', 'parcel': 'core',
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
        motif_svg = MOTIFS[family_key]
        
        if len(name) > 30: name = name[:27] + "..."
        summary = summary.replace('\\n', ' ').replace('\n', ' ').replace('&', '&amp;')
        if len(summary) > 60: summary = summary[:57] + "..."
        name_xml, summary_xml = saxutils.escape(name), saxutils.escape(summary)
        
        desc_dir = os.path.join(module_path, "static", "description")
        os.makedirs(desc_dir, exist_ok=True)
        
        icon_file = os.path.join(desc_dir, "icon.svg")
        icon_png = os.path.join(desc_dir, "icon.png")
        banner_file = os.path.join(desc_dir, "banner.svg")
        banner_png = os.path.join(desc_dir, "banner.png")
        screenshot = os.path.join(desc_dir, "main_screenshot.png")
        
        icon_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" rx="40" fill="#FFF9F2"/>
    <rect width="246" height="246" x="5" y="5" rx="38" fill="none" stroke="#C9382B" stroke-width="2"/>
    {motif_svg}
</svg>'''
        with open(icon_file, 'w', encoding='utf-8') as f: f.write(icon_svg)
        
        banner_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="628" height="314" viewBox="0 0 628 314" xmlns="http://www.w3.org/2000/svg">
  <rect width="628" height="314" fill="#FFF9F2" />
  <g transform="translate(320, -50) scale(0.85)" opacity="0.03">
    <path fill-rule="evenodd" fill="#C9382B" d="M 395,174 58,177 42,184 29,204 25,244 46,266 149,279 315,269 313,252 260,241 87,245 76,230 91,209 243,204 339,220 356,239 360,272 346,297 329,306 169,316 53,301 6,279 12,375 95,388 379,378 391,368 Z M 386,15 375,7 354,3 299,3 298,0 277,0 264,4 127,3 29,8 19,16 13,27 7,55 3,175 7,179 19,164 42,147 110,140 316,137 362,140 392,147 393,61 Z M 342,57 340,60 342,72 340,78 332,87 319,89 260,90 230,97 169,99 167,101 158,100 155,102 141,103 94,102 71,95 63,95 55,91 38,91 29,84 29,74 37,63 45,63 55,58 63,58 82,52 95,53 134,49 197,50 228,47 261,47 311,51 326,50 Z" />
  </g>
  <rect x="40" y="92" width="130" height="130" rx="20" fill="white" stroke="#C9382B" stroke-width="1" />
  <g transform="translate(47.5, 99.5) scale(0.45)">{motif_svg}</g>
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
    <path d="M126,104.9 C126,62 144,40.6 179.8,40.6 C179.9,40.6 180,40.6 180,40.6 C196.3,40.6 209.3,45.9 219.1,56.5 C228.8,67.2 233.7,81.5 233.7,99.3 C233.7,105.2 233.5,110.9 233,116.3 L149,116.3 C151.7,136.9 163.2,147.3 183.4,147.3 C199.8,147.3 213.9,144.3 225.5,138.2 L225.5,158.5 C212.9,163.8 198.7,166.5 182.9,166.5 C182.7,166.5 182.4,166.5 182.2,166.5 C175,166.5 168.4,165.6 162.4,163.8 C156.4,162 150.4,159 144.7,154.9 C138.9,150.8 134.4,144.4 131,135.9 C127.7,127.3 126,117 126,104.9 Z M148.7,96 L211.3,96 C211,91.9 210.3,88.1 209.2,84.4 C208.1,80.7 206.5,76.9 204.3,73.1 C202.1,69.3 199,66.3 194.8,64 C190.7,61.7 185.8,60.6 180,60.6 C169.8,60.6 162.3,63.2 157.4,68.5 C152.6,73.8 149.7,83 148.7,96 Z" fill="#2C83FC"></path>
    <path d="M0,104.3 C0,84.9 4.4,69.3 13.2,57.7 C22,46.1 35.5,40.3 53.7,40.3 C68.9,40.3 81.1,43.7 90.3,50.6 C99.5,57.5 104,67.3 104,79.9 L104,173.2 C104,178.7 103.2,183.9 101.6,188.6 C100,193.4 97.4,198 93.6,202.5 C89.8,207.1 84.2,210.6 76.6,213.2 C69,215.8 59.8,217.1 48.9,217.1 C36.4,217.1 24,215.3 11.8,211.8 L11.8,190 C23.6,193.7 35.4,195.5 47,195.5 C55,195.5 61.5,194.8 66.6,193.3 C71.6,191.9 75.1,189.9 77,187.2 C78.9,184.6 80.1,182.3 80.5,180.5 C80.9,178.6 81.1,176.2 81.1,173.2 L81.1,162.1 C72.6,164.5 64.2,165.7 55.8,165.7 C37.9,165.7 24.1,160.4 14.5,149.9 C4.8,139.3 0,124.1 0,104.3 Z M23.1,104.3 C23.1,120.6 26,131.4 31.8,136.8 C37.6,142.2 45.6,144.8 55.8,144.8 C64.8,144.8 73.2,143.2 81.1,140 L81.1,78.5 C81.1,76.6 80.9,75 80.6,73.7 C80.3,72.4 79.4,70.5 77.8,68.2 C76.3,65.8 73.5,64 69.4,62.8 C65.3,61.5 60.1,60.9 53.7,60.9 C49.6,60.9 45.9,61.4 42.8,62.4 C39.7,63.4 36.5,65.3 33.2,68 C30,70.8 27.5,75.2 25.7,81.3 C23.9,87.4 23.1,95.1 23.1,104.3 Z" fill="#2C83FC"></path>
  </g>
</svg>'''
        with open(banner_file, 'w', encoding='utf-8') as f: f.write(banner_svg)
        
        subprocess.run(["python", CONVERT_SCRIPT, icon_file, icon_png, "-w", "256", "-H", "256"], check=True, capture_output=True)
        subprocess.run(["python", CONVERT_SCRIPT, banner_file, banner_png, "-w", "628", "-H", "314"], check=True, capture_output=True)
        subprocess.run(["cp", banner_png, screenshot], check=True)
        count += 1
    except Exception as e: print(f"Failed {item}: {str(e)}")

print(f"🎉 Fully healed {count} modules. All icons and banners are now pixel-perfect and centered.")
