import os
import re

filepath = 'README.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_section = """
## 🌟 核心亮点：降维打击的商业能力 (The 3-Tier Edge)

除了 Odoo 原生的进销存财能力，Odoo Farm 在以下三个维度实现了对传统农业 ERP 的降维打击：

1. **[49 大科幻级商业闭环场景 (The Top 49 Showcases)](docs/business/marketing/SCENARIOS_SHOWCASE.md)**
   涵盖了从地里的基因溯源、温室大棚的微气候拦截，到供应链的 FEFO 调度，再到消费端的“丑果盲盒”与“时间银行”等 49 个全真实业务落地场景。
   👉 *[快速阅读：精选 Top 8 农业大客户营销路演画册](docs/business/marketing/TOP_8_SHOWCASE_PITCH.md)*

2. **[金融级三层数据隔离 (3-Tier Row-Level Security)](docs/business/analysis/DATA_ISOLATION_RLS_DESIGN.md)**
   针对中国及亚洲“大村集体 -> 承包大户 -> 临时散工”的嵌套型农业组织架构，我们首创了基于 ir.rule 的 3 级动态 RLS 防火墙。
   **农场主能够向下穿透监控下属散工的产出与贷款，但各农场之间平行绝密隔离。** 这彻底扫清了多个农户共用一个系统时的“露富”和“隐私泄漏”痛点。
   👉 *[点击查看 RLS 数据隔离架构设计图 (Draw.io Web Viewer)](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&edit=_blank#R3Zlbb6M4FMff%2Bym87EtHmqSBXJppSkahl1G17baaZne20kiVARO8NTgyTmn20%2B%2FhkmDSkCZt0q2WPARsH4N%2F5%2FyPjTn%2B%2BhQw9EhERHloanq9oSESOtyl4cjU%2Fhie17ra1%2F7ecfDkUUaQzyNpaq7AMeVaYWZ06g2w7O8hdOxSPBI4QCEOiKmdYonRRcQZltASDYTjU0kcOREkbQ4GwdM3gcf%2BFXcJy4qgUHAuZxdpmxPCGKKuqcEDHiyv0TU0xoKEcrFR0fqXWg1Z2HkYCT4JXXTCQ4lpCMNAtVq%2F3Oza5RxdhJHEoUPK1co9ad7g3h4BD8wmMObU8hyLAOlf6g2UILBxROadaSiSUwYNo5gGDIekB%2BVC3tJ%2FiNlq9AA0O%2BGMC%2FNXr538oFrwB5KXddKj58Gj36bd6Nl5Yq13eqlXJHkq4dC14ukz4oQHRIopgnYtgDXN%2FmLqSt%2FUuh049wkd%2BWDbNuACR6Y2ym00Ff9BxqK%2FV4Z3woMxDqdIP4JTPiYC3P9YTdGBNirBISUisf0TUOARKfWxn%2BK9mjBJa7PbzAPs0yq2zRJbF5Ou5yywdbrE9kpsl%2FJUvb6CrJGR7ShkDYVsq7UW2eVRnMbXdQyxiwaVXD1odI%2BfkTWOyub7QwKCHWwCr026bqsMr2vYzYXAXApv5uyNwDXVkEwvNg1JZcTWamD2C8CsHJi1ATDP8wxnIdrcjt1pbwdYq7UDYr9DRo6Qx0U2%2BOowC3AIKhX3eE5NDa%2Bf4f4pDyDNHuUjuqcuMlFEmFcATPMxcQFBnEwQt2PsEDOGeaHny4AlOa7EEo7XBV%2BhiBU09UZGs13Q1FWanVfqVkEWc%2FGQENPLgdY8Qj%2FSGjTQgdstAQcMcfSA9M9oEEVEIn17zPKZ5PWccpnqhwqn1m44GZWcjBIn4zO65Dj8YJi2wqkszvmq4jtxuHDX0qlrKxIdjAQFVk62MNsffPoZXlFH8FrCL8oKLsJHGCaHYVxymZYVGc%2FHY2I6U0YBrmi%2BTbZvkGoeg4bKVp1kD9%2Be%2BKwXE5%2B9LPFZ75L41p1Eiplt54lvlZDtyoRnlRNe8x0F%2FCIWfcsCLmvSrtKktahJa4kmrW1rMo%2BoN%2BDahSbP3BGERkylT8NZngN5xWGMhQsvChG1KaNy%2BqlSrAR6UCfc8wlU3JAQniDlDeE3l2nBNLHKhMWF9PmIh5idzcp6RWgWtZewXIOCv4mU03QliCeSz9iTJyr%2FMht1o52e3iVFISBIytrZ6Z3ZWJoks7IfKU8D3JM8WUXCRBGfCPC6ujKDhemISHXlUeVCQVj6qpV2vv78%2FZy1Ucl613gP%2F3O8xrbwVvMtTee7JvpWoC6O%2FPS%2B65FV1sczsulwdx2zyU2M%2FztUYzdQX0rY1urUbH%2BQ1LyBU%2FKpcr3UYS9NHfaz1GHr7xHl9kcM8qU8Xwxye1mQ2%2BXMYe8myIc%2BQedUkBgD3v0bLOCfMGU%2FsnqnKbcq7xpTURcTRtC8p1nnydp4%2BP3iZHh5h6zL65Pfzk53LAQ9d9vcW%2BC4udvqC5vSnteAo%2BS4JjR2B0Lw2LQZdx6WuW%2B%2B77tiQi2EsrkHVYvc6obTUGbb3tkqtdtQHZ25etb1OhvdfIyuskdcvb2dj2Pub3VPO%2B9AeWHUTX2WO%2FNNbsXdjNFxRNZY3hPdbZPDsqu%2BdA6buLO1Pe5mvvNYa1a8M3Y3WewfHxQfflJHlL4MHR%2FkH5f6e0ll8kWqv%2Fcv)*

3. **[F2P 消费端生态矩阵 (C2M Ecosystem Hub)](docs/business/marketing/C2M_ECOSYSTEM_VISION.md)**
   打通 C 端 App 与 Odoo 合作社之间的桥梁，创造基于“冰箱消耗率”的 C2M 订单农业与生态闭环。
"""

if '核心亮点' not in content:
    if '## Architecture' in content:
        content = content.replace('## Architecture', new_section + '\n\n## Architecture')
    else:
        content = content.replace('# Odoo Farm', '# Odoo Farm\n' + new_section)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
