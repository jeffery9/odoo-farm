#!/usr/bin/env python3
"""
自动应用细分行业专属的图标 (Motif)。
当模块目录名称匹配到关键字时，使用专属 SVG 路径重写其 static/description/icon.svg
"""
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

MOTIFS = {
    "mushroom": '<path d="M128,60 C70,60 50,110 50,130 L206,130 C206,110 186,60 128,60 Z" fill="#C9382B"/><rect x="100" y="130" width="56" height="60" rx="10" fill="#C9382B"/><circle cx="90" cy="95" r="12" fill="#FFF9F2"/><circle cx="166" cy="95" r="12" fill="#FFF9F2"/><circle cx="128" cy="80" r="15" fill="#FFF9F2"/>',
    "floriculture": '<circle cx="128" cy="128" r="25" fill="#FFF9F2" stroke="#C9382B" stroke-width="12"/><circle cx="128" cy="70" r="30" fill="#C9382B" opacity="0.8"/><circle cx="128" cy="186" r="30" fill="#C9382B" opacity="0.8"/><circle cx="70" cy="128" r="30" fill="#C9382B" opacity="0.8"/><circle cx="186" cy="128" r="30" fill="#C9382B" opacity="0.8"/>',
    "viticulture": '<circle cx="128" cy="90" r="20" fill="#C9382B"/><circle cx="100" cy="120" r="20" fill="#C9382B"/><circle cx="156" cy="120" r="20" fill="#C9382B"/><circle cx="128" cy="150" r="20" fill="#C9382B"/><circle cx="128" cy="180" r="20" fill="#C9382B"/><path d="M128,90 C128,60 150,50 160,40" stroke="#C9382B" stroke-width="8" fill="none" stroke-linecap="round"/>',
    "winery": '<path d="M110,60 L146,60 L146,100 L180,180 L180,210 C180,220 170,230 156,230 L100,230 C86,230 76,220 76,210 L76,180 L110,100 Z" fill="#C9382B" opacity="0.5"/><path d="M76,160 L180,160 L180,210 C180,220 170,230 156,230 L100,230 C86,230 76,220 76,210 Z" fill="#C9382B"/><circle cx="128" cy="120" r="8" fill="#C9382B"/><circle cx="106" cy="140" r="5" fill="#C9382B"/><circle cx="146" cy="130" r="6" fill="#C9382B"/>',
    "fermentation": '<path d="M110,60 L146,60 L146,100 L180,180 L180,210 C180,220 170,230 156,230 L100,230 C86,230 76,220 76,210 L76,180 L110,100 Z" fill="#C9382B" opacity="0.5"/><path d="M76,160 L180,160 L180,210 C180,220 170,230 156,230 L100,230 C86,230 76,220 76,210 Z" fill="#C9382B"/><circle cx="128" cy="120" r="8" fill="#C9382B"/><circle cx="106" cy="140" r="5" fill="#C9382B"/><circle cx="146" cy="130" r="6" fill="#C9382B"/>',
    "apiculture": '<path d="M128,50 L168,70 L168,110 L128,130 L88,110 L88,70 Z" fill="#C9382B"/><path d="M128,130 L168,150 L168,190 L128,210 L88,190 L88,150 Z" fill="#C9382B" opacity="0.6"/><path d="M168,110 L208,130 L208,170 L168,190 L128,170 L128,130 Z" fill="#C9382B" opacity="0.4"/><path d="M88,110 L128,130 L128,170 L88,190 L48,170 L48,130 Z" fill="#C9382B" opacity="0.8"/>',
    "aquaculture": '<path d="M50,130 C90,80 166,80 206,130 C166,180 90,180 50,130 Z" fill="#C9382B"/><path d="M50,130 L30,100 L30,160 Z" fill="#C9382B"/><circle cx="160" cy="120" r="8" fill="#FFF9F2"/>',
    "breeding": '<path d="M80,60 C120,120 136,136 176,196" stroke="#C9382B" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M176,60 C136,120 120,136 80,196" stroke="#C9382B" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="80" cy="60" r="15" fill="#C9382B"/><circle cx="176" cy="60" r="15" fill="#C9382B"/><circle cx="80" cy="196" r="15" fill="#C9382B"/><circle cx="176" cy="196" r="15" fill="#C9382B"/>',
    "seed": '<path d="M128,180 C80,180 60,140 60,100 C100,100 128,140 128,180 Z" fill="#C9382B"/><path d="M128,180 C176,180 196,140 196,100 C156,100 128,140 128,180 Z" fill="#C9382B" opacity="0.6"/><path d="M128,180 L128,220" stroke="#C9382B" stroke-width="12" stroke-linecap="round"/><path d="M128,180 C128,100 160,60 200,40" stroke="#C9382B" stroke-width="8" fill="none" stroke-linecap="round"/>',
    "weather": '<circle cx="160" cy="90" r="30" fill="#C9382B" opacity="0.3"/><path d="M80,140 C80,110 120,110 130,120 C140,100 180,100 190,130 C210,130 210,170 190,170 L80,170 C50,170 50,140 80,140 Z" fill="#C9382B"/>',
    "robotics": '<rect x="80" y="80" width="96" height="80" rx="15" fill="#C9382B"/><circle cx="106" cy="120" r="12" fill="#FFF9F2"/><circle cx="150" cy="120" r="12" fill="#FFF9F2"/><rect x="110" y="180" width="36" height="20" fill="#C9382B" opacity="0.6"/><path d="M128,80 L128,50 M110,50 L146,50" stroke="#C9382B" stroke-width="8" stroke-linecap="round"/>',
    "logistics": '<path d="M40,100 L160,100 L160,180 L40,180 Z" fill="#C9382B"/><path d="M170,120 L210,120 L220,150 L220,180 L170,180 Z" fill="#C9382B" opacity="0.8"/><circle cx="80" cy="190" r="20" fill="#FFF9F2" stroke="#C9382B" stroke-width="8"/><circle cx="180" cy="190" r="20" fill="#FFF9F2" stroke="#C9382B" stroke-width="8"/>',
    "agritourism": '<path d="M128,70 L60,180 L196,180 Z" fill="#C9382B"/><path d="M128,70 L128,180 L196,180 Z" fill="#C9382B" opacity="0.5"/><path d="M128,120 L100,180 L156,180 Z" fill="#FFF9F2"/>',
    "medicinal": '<rect x="110" y="60" width="36" height="136" rx="10" fill="#C9382B"/><rect x="60" y="110" width="136" height="36" rx="10" fill="#C9382B"/><path d="M128,128 C160,90 200,90 200,128 C200,160 160,160 128,128 Z" fill="#FFF9F2" opacity="0.9"/>',
    "orchard": '<circle cx="128" cy="90" r="50" fill="#C9382B"/><circle cx="90" cy="120" r="40" fill="#C9382B" opacity="0.9"/><circle cx="166" cy="120" r="40" fill="#C9382B" opacity="0.9"/><path d="M118,150 L138,150 L148,220 L108,220 Z" fill="#C9382B" opacity="0.6"/>',
    "live_streaming": '<rect x="60" y="80" width="136" height="96" rx="20" fill="#C9382B"/><path d="M106,100 L156,128 L106,156 Z" fill="#FFF9F2"/><path d="M128,176 L100,220 L156,220 Z" fill="#C9382B" opacity="0.6"/>',
    "sale": '<path d="M70,90 L186,90 L170,170 L86,170 Z" fill="#C9382B"/><path d="M100,90 C100,60 156,60 156,90" stroke="#C9382B" stroke-width="12" fill="none" stroke-linecap="round"/><rect x="90" y="110" width="76" height="40" rx="8" fill="#FFF9F2" opacity="0.3"/>',
    "pos": '<path d="M70,90 L186,90 L170,170 L86,170 Z" fill="#C9382B"/><path d="M100,90 C100,60 156,60 156,90" stroke="#C9382B" stroke-width="12" fill="none" stroke-linecap="round"/><rect x="90" y="110" width="76" height="40" rx="8" fill="#FFF9F2" opacity="0.3"/>',
    "marketing": '<path d="M70,90 L186,90 L170,170 L86,170 Z" fill="#C9382B"/><path d="M100,90 C100,60 156,60 156,90" stroke="#C9382B" stroke-width="12" fill="none" stroke-linecap="round"/><rect x="90" y="110" width="76" height="40" rx="8" fill="#FFF9F2" opacity="0.3"/>',
    "dashboard": '<rect x="60" y="140" width="30" height="70" rx="5" fill="#C9382B" opacity="0.4"/><rect x="113" y="90" width="30" height="120" rx="5" fill="#C9382B" opacity="0.7"/><rect x="166" y="50" width="30" height="160" rx="5" fill="#C9382B"/>',
    "valuation": '<rect x="60" y="140" width="30" height="70" rx="5" fill="#C9382B" opacity="0.4"/><rect x="113" y="90" width="30" height="120" rx="5" fill="#C9382B" opacity="0.7"/><rect x="166" y="50" width="30" height="160" rx="5" fill="#C9382B"/>',
    "report": '<rect x="60" y="140" width="30" height="70" rx="5" fill="#C9382B" opacity="0.4"/><rect x="113" y="90" width="30" height="120" rx="5" fill="#C9382B" opacity="0.7"/><rect x="166" y="50" width="30" height="160" rx="5" fill="#C9382B"/>',
    "cert": '<path d="M80,40 L176,40 L176,140 L128,180 L80,140 Z" fill="#C9382B"/><path d="M100,180 L100,220 L128,200 L156,220 L156,180" fill="#C9382B" opacity="0.6"/><circle cx="128" cy="100" r="20" fill="#FFF9F2"/>',
    "label": '<path d="M80,40 L176,40 L176,140 L128,180 L80,140 Z" fill="#C9382B"/><path d="M100,180 L100,220 L128,200 L156,220 L156,180" fill="#C9382B" opacity="0.6"/><circle cx="128" cy="100" r="20" fill="#FFF9F2"/>',
    "insurance": '<path d="M128,40 L196,70 L196,130 C196,170 150,210 128,220 C106,210 60,170 60,130 L60,70 Z" fill="#C9382B"/><path d="M100,130 L120,150 L156,110" stroke="#FFF9F2" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "safety": '<path d="M128,40 L196,70 L196,130 C196,170 150,210 128,220 C106,210 60,170 60,130 L60,70 Z" fill="#C9382B"/><path d="M100,130 L120,150 L156,110" stroke="#FFF9F2" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "security": '<path d="M128,40 L196,70 L196,130 C196,170 150,210 128,220 C106,210 60,170 60,130 L60,70 Z" fill="#C9382B"/><path d="M100,130 L120,150 L156,110" stroke="#FFF9F2" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
}

SVG_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" rx="40" fill="#FFF9F2"/>
    {motif}
</svg>"""

if __name__ == "__main__":
    modules = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and os.path.exists(os.path.join(BASE_DIR, d, "__manifest__.py"))])
    count = 0
    for mod in modules:
        matched_motif = None
        for kw, svg_inner in MOTIFS.items():
            if kw in mod:
                matched_motif = svg_inner
                break
        
        if matched_motif:
            icon_path = os.path.join(BASE_DIR, mod, "static/description/icon.svg")
            os.makedirs(os.path.dirname(icon_path), exist_ok=True)
            with open(icon_path, 'w', encoding='utf-8') as f:
                f.write(SVG_TEMPLATE.replace('{motif}', matched_motif))
            count += 1
    print(f"Applied unique subdivision motifs to {count} specific industry modules.")
