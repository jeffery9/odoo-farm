# Odoo 19 Migration: Batch Testing & Hardening Guide

Based on the execution of Batches 1 through 7, here is the accumulated experience and systematic methodology to accelerate the handling of subsequent batches or new module additions for Odoo 19.

## 1. Pre-Flight Checks (Run these BEFORE starting Odoo)

Odoo 19's `RelaxNG` parser and registry loader are extremely strict. Running these automated regex replacements before testing saves hours of debugging:

*   **XML Structure:**
    *   Strip all `attrs="..."`, `states="..."`, and `expand="..."` from XML files.
    *   Escape all bare `& ` symbols to `&amp; ` in XML.
    *   Ensure all `<menuitem>` tags appear **after** their corresponding `<record type="ir.actions.act_window">` tags.
    *   Ensure `<search>` views do not contain `<group string="...">` directly; use `<filter>` or properly formatted `<separator/>`.
*   **Python Definitions:**
    *   Ensure every directory with python files has an `__init__.py` that imports them.
    *   Ensure `_inherit` arrays do not mix abstract and non-abstract models inappropriately.
    *   Convert old `fields.Selection(['a', 'b'])` to list of tuples `fields.Selection([('a', 'A'), ('b', 'B')])`.
*   **Dependencies:**
    *   Run a script to verify all modules listed in `depends` inside `__manifest__.py` actually exist.

## 2. Common Odoo 19 Crash Signatures & Fast Resolutions

### A. XML / RelaxNG Syntax Errors
**Error:** `lxml.etree.XMLSyntaxError: Opening and ending tag mismatch...` or `Element odoo has extra content...`
*   **Cause:** Usually a bad `<xpath>` injection (e.g., trying to inject into a `<header>` or `<notebook>` that no longer exists in the parent Odoo 19 base view).
*   **Fast Fix:** 
    *   For `mrp.production`: Change `<xpath expr="//header" position="inside">` to `<xpath expr="//sheet" position="before"><header>...`.
    *   For `stock.lot`: Change `<xpath expr="//notebook" position="inside">` to `<xpath expr="//sheet" position="inside"><notebook>...`.

### B. Registry Dependency / Cyclic Imports
**Error:** `odoo.exceptions.UserError: Recursion error in modules dependencies!`
*   **Cause:** Module A depends on Module B, which depends back on Module A (e.g., `farm_ai_agent` -> `farm_robotics` -> `farm_ai_agent`).
*   **Fast Fix:** Use a python AST script (`find_cycle.py`) to trace the `depends` list across all `__manifest__.py` files and remove the cyclical link from the least-dependent module.

### C. Missing Model / Proxy Errors
**Error:** `TypeError: Model 'X' does not exist in registry.` or `AssertionError: Field X with unknown comodel_name 'Y'`
*   **Cause:** Module is missing an `import models` in its `__init__.py`, OR the dependency containing the target model is missing from `__manifest__.py`.
*   **Fast Fix:** Check `__init__.py`. If correct, grep the workspace for `_name = 'Y'` to find which module actually owns the model, and add it to the failing module's `depends`.

### D. Relational Inversion / One2many Crashes
**Error:** `KeyError: 'some_id'` in `setup_inverses` during model load.
*   **Cause:** A `One2many` field defines an inverse `Many2one` field that either doesn't exist on the target model or is shadowed by an incorrect `_inherit` / `_inherits` hierarchy.
*   **Fast Fix:** Search for `fields.One2many(..., 'some_id')`. Verify the target model actually possesses `some_id = fields.Many2one(...)` pointing back to the exact correct model.

### E. Concurrent Update / Serialization Failures
**Error:** `psycopg2.errors.SerializationFailure: could not serialize access due to concurrent update`
*   **Cause:** Odoo's test runner / registry loader is trying to flush module states to Postgres simultaneously.
*   **Fast Fix:** This is transient. Simply re-run the `odoo` command. If persistent, reduce workers or run the update command explicitly on single modules first.

## 3. Recommended Toolkit for Next Batches

Always deploy these utility scripts to the root of the project to batch-process modules:
1.  `fix_xml_batch.py`: Strips `attrs`, `states`, fixes `&`.
2.  `check_batch_deps.py`: Validates `__manifest__.py` imports.
3.  `find_cycle.py`: Detects circular dependencies.
4.  `fix_menu_order.py`: Repositions menu items after actions.
