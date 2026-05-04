import os
modules = [d for d in os.listdir('.') if os.path.isdir(d) and (d.startswith('farm_') or d.startswith('agri_') or d.startswith('precision_'))]
empty_mods = [m for m in modules if os.path.exists(os.path.join(m, 'i18n', f"{m}.pot")) and os.path.getsize(os.path.join(m, 'i18n', f"{m}.pot")) == 0]
print(",".join(empty_mods))
