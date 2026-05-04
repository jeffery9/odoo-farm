#!/bin/bash
set -e

# 配置环境变量以实现免密操作
export PGPASSWORD='odoo'
export PGUSER='odoo'
export PGHOST='db'
DB="db_automated_i18n"

cd /mnt/extra-addons

# 1. 准备干净的数据库
echo ">>> [INIT] Creating clean database: $DB"
dropdb --if-exists $DB
createdb $DB

# 获取所有待处理模块
MODULES=$(ls -1d farm_* agri_* precision_* 2>/dev/null)
TOTAL=$(echo "$MODULES" | wc -w)
COUNT=0
SUCCESS=0

echo ">>> [START] Starting native Odoo i18n pipeline for $TOTAL modules..."

for MOD in $MODULES; do
    COUNT=$((COUNT + 1))
    echo "--------------------------------------------------------"
    echo "[$COUNT/$TOTAL] Processing: $MOD"
    
    # 步骤 A: 安装模块 (确保注册表完整)
    # 使用 --stop-after-init 确保安装后自动退出
    echo "  -> Installing..."
    odoo -c /etc/odoo/odoo.conf -d $DB -i $MOD --stop-after-init --workers=0 --without-demo=all > /tmp/install.log 2>&1
    
    # 步骤 B: 导出 POT 模板
    echo "  -> Exporting POT..."
    mkdir -p "$MOD/i18n"
    POT_PATH="/mnt/extra-addons/$MOD/i18n/$MOD.pot"
    
    # 使用 Odoo 19 官方 i18n export 子命令
    odoo i18n export -c /etc/odoo/odoo.conf -d $DB -l pot -o "$POT_PATH" $MOD > /tmp/export.log 2>&1
    
    if [ -s "$POT_PATH" ]; then
        SIZE=$(stat -c%s "$POT_PATH")
        echo "  ✅ Success: $MOD.pot ($SIZE bytes)"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "  ❌ Failed: $MOD.pot is empty or missing"
    fi
done

echo "========================================================"
echo "PIPELINE COMPLETE: $SUCCESS/$TOTAL exported successfully."
echo "========================================================"
