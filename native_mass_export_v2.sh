#!/bin/bash
set -e
export PGPASSWORD='odoo'
export PGUSER='odoo'
export PGHOST='db'
DB="db_i18n_verified"

cd /mnt/extra-addons

echo ">>> Creating clean DB for i18n export..."
dropdb --if-exists $DB
createdb $DB

MODULES=$(ls -1d farm_* agri_* precision_* 2>/dev/null)
TOTAL=$(echo "$MODULES" | wc -w)
COUNT=0

for MOD in $MODULES; do
    COUNT=$((COUNT + 1))
    echo "[$COUNT/$TOTAL] Processing $MOD..."
    
    # Install the module. Odoo 19 will automatically install dependencies.
    # --stop-after-init ensures it just does the work and exits.
    echo "  - Installing..."
    odoo -c /etc/odoo/odoo.conf -d $DB -i $MOD --stop-after-init --workers=0 --without-demo=all > /tmp/install.log 2>&1 || true
    
    # Export the POT.
    echo "  - Exporting..."
    mkdir -p "$MOD/i18n"
    # Note: Odoo 19 'i18n export' subcommand
    odoo i18n export -c /etc/odoo/odoo.conf -d $DB -l pot -o "$MOD/i18n/$MOD.pot" $MOD > /tmp/export.log 2>&1
    
    if [ -s "$MOD/i18n/$MOD.pot" ]; then
        echo "  ✅ Done ($MOD.pot)"
    else
        echo "  ❌ Failed ($MOD)"
    fi
done
