# Odoo Farm Deployment Manifest (v1.0)

## Overview
This manifest outlines the requirements and steps for deploying the Odoo Farm ecosystem on Odoo 19.0 (Standardized CE/EE).

## 1. System Requirements
- **Odoo Version:** 19.0
- **PostgreSQL:** 16+ (with PostGIS extension)
- **External Dependencies:**
  - `paho-mqtt` (for Agri IoT bridge)
  - `shapely`, `pyproj` (for geospatial auditing)
  - `numpy`, `scipy` (for biological science engine)

## 2. Infrastructure Setup
- **MQTT Broker:** Mosquitto or equivalent for IIoT telemetry.
- **Storage:** Standard Odoo filestore with appropriate permissions.

## 3. Module Inventory & Installation Order
The following modules must be installed in sequence to ensure dependency satisfaction:

### Foundation (Level 0)
1. `farm_core`: Core agricultural entities and mixins.
2. `agri_intervention`: Core Intervention Engine (Abstract).
3. `farm_agri_science`: Agronomic profiles and GDD calculations.

### Functional Layers (Level 1-2)
4. `farm_operation`: Standardizes MRP into Agricultural Interventions.
5. `farm_ux`: Specialized OWL UI widgets (Gating, Gauges, DNA).
6. `farm_iot`: IoT telemetry and device management.
7. `farm_ecology`: Biodiversity and GEP (Ecological Score) tracking.

### Business Domains (Level 3-4)
8. `farm_biological_valuation`: Financial valuation framework.
9. `farm_financial_valuation`: GEP and Growth-integrated valuation.
10. `farm_financial_insurance`: Agricultural insurance and claims.
11. `farm_agritourism`: Resource booking and experience management.

*(Full inventory of 102 modules available in module_list.txt)*

## 4. Post-Installation Configuration
- **Term Mapping:** Configure local agricultural term aliases in `Farm UX > Term Mapping`.
- **IoT Profiles:** Define MQTT topics in `IoT > Device Profiles`.
- **Valuation Templates:** Setup "Anji Model" multipliers in `Financial > Valuation Templates`.

## 5. Security & Audit
- Ensure `ir.model.access.csv` is correctly loaded for all custom models.
- Verify "Trust DNA" integrity scores on biological lots after initial harvesting tests.
