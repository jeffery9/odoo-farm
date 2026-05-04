# GeninIT Odoo Farm - Visual Branding Guide for AI Agents

> **⚠️ AI AGENT INSTRUCTION ⚠️**
> 
> This document is the absolute source of truth for generating, modifying, and maintaining Odoo App Store marketing assets (icons, banners, and HTML) within the `odoo-farm-dev` workspace. 
> 
> **Do NOT manually guess color codes, dimensions, or banner text placements. Follow this exact protocol.**

## 1. The GIVL Standard (GeninIT Industrial Visual Language)

All modules MUST adhere to the following visual constraints:
- **Base Color (Canvas/Plate):** `#FFF9F2` (A warm, organic white/beige).
- **Primary Brand Color (Motif):** `#C9382B` (GeninIT Red).
- **Icon Dimensions:** Exactly `256x256` with a base `<rect rx="40">`.
- **Banner Dimensions:** Exactly `628x314`.
- **Typography:** To prevent rendering issues across OS platforms during PNG conversion, all SVG `<text>` elements MUST use the exact font stack: `'PingFang SC', 'Microsoft YaHei', 'SimHei', sans-serif`.

## 2. Directory Architecture

- `docs/icon/*.svg|png`: The centralized library of 40 pre-designed vector motifs (13 core categories + 27 industry subdivisions).
- `docs/icon/scripts/`: The automation engine.
  - `apply_custom_motifs.py`: Dictionary mapping module names (e.g., "mushroom") to specific SVG `<path>` data.
  - `rebuild_banners.py`: The dynamic composition engine.
- `<module_name>/static/description/`: The ultimate destination for App Store assets. Contains:
  - `icon.svg` & `icon.png`
  - `banner.svg` & `banner.png`
  - `main_screenshot.png` (copy of banner.png)
  - `geninit-banner-logo.png`
  - `index.html`

## 3. Standard Operating Procedure (SOP) for New Modules

When a user asks you to "create branding for a new module" or "update an icon", you MUST follow this exact sequence:

### STEP 1: Update or Create the Icon
**Never manually edit `banner.svg`.** The banner is a derivative of the icon. 
1. If the user wants a new specific motif (e.g., a tractor), open `docs/icon/scripts/apply_custom_motifs.py`.
2. Add the new keyword and its raw SVG `<path>` data to the `MOTIFS` dictionary.
3. Run the script to inject the new motif into the target module's `static/description/icon.svg`.
   ```bash
   python3 docs/icon/scripts/apply_custom_motifs.py
   ```

### STEP 2: Dynamically Rebuild the Banner
Because the banner inherits the icon's motif and the module's name, you must use the rebuild script.
1. Run the banner generation script:
   ```bash
   python3 docs/icon/scripts/rebuild_banners.py
   ```
   *What this does:* It strips the background from `icon.svg`, scales the motif to 42%, injects it into the left frame of the banner template, and injects the module's exact `__manifest__.py` name into the title.

### STEP 3: Convert SVG to PNG
Odoo's App Store requires PNGs. The previous python script generates a shell script containing the required `cairosvg` conversion commands.
1. Execute the generated commands:
   ```bash
   bash docs/icon/scripts/convert_commands.sh
   ```

### STEP 4: Update index.html
Ensure the module has the standard 5-section `index.html` in its `static/description/` folder, utilizing the relative references to `banner.png` and `geninit-banner-logo.png`.

## 4. Troubleshooting

- **XML Parsing Errors (`not well-formed`):** This usually happens if the module's name contains an unescaped ampersand (`&`). The `rebuild_banners.py` script automatically uses `xml.sax.saxutils.escape`, but if you ever write SVG manually, ensure `&` is written as `&amp;`.
- **Missing Motif in Banner:** Ensure the `icon.svg` contains the standard background `<rect width="256" height="256" rx="40" fill="#FFF9F2"/>`. The rebuild script specifically looks for this tag to strip it out. If the rect is missing or formatted differently, the entire icon might be injected, causing overlapping backgrounds.

---
**End of Instructions.** Rely on automation over manual SVG editing whenever possible.