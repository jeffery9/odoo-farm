# 农业套件逻辑架构全景图 (Logical Architecture Map)

> **架构说明**: 系统已从物理 12 层扁平化映射为 4 大逻辑宏层，旨在降低维护复杂度，提升模块间协作效率。

## Foundation (底座层)

```mermaid
graph TD
    classDef default fill:#fefefe,stroke:#333,stroke-width:1px,color:#000;
    classDef highlight fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000;
    agri_iot["agri_iot"]:::highlight
    farm_core["farm_core"]:::highlight
    farm_ux["farm_ux"]:::highlight
```

## Core Frameworks (业务核心层)

```mermaid
graph TD
    classDef default fill:#fefefe,stroke:#333,stroke-width:1px,color:#000;
    classDef highlight fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000;
    farm_agri_science["farm_agri_science"]:::highlight
    farm_agritourism["farm_agritourism"]:::highlight
    farm_ai_core["farm_ai_core"]:::highlight
    farm_ai_llm_integration["farm_ai_llm_integration"]:::highlight
    farm_biological_valuation["farm_biological_valuation"]:::highlight
    farm_csa["farm_csa"]:::highlight
    farm_data_security["farm_data_security"]:::highlight
    farm_ecology["farm_ecology"]:::highlight
    farm_entity_reg["farm_entity_reg"]:::highlight
    farm_esg["farm_esg"]:::highlight
    farm_financial_core["farm_financial_core"]:::highlight
    farm_financial_credit["farm_financial_credit"]:::highlight
    farm_financial_insurance["farm_financial_insurance"]:::highlight
    farm_financial_valuation["farm_financial_valuation"]:::highlight
    farm_greenhouse["farm_greenhouse"]:::highlight
    farm_insurance["farm_insurance"]:::highlight
    farm_iot["farm_iot"]:::highlight
    farm_multi_farm["farm_multi_farm"]:::highlight
    farm_multi_farm_equipment["farm_multi_farm_equipment"]:::highlight
    farm_multi_farm_financial["farm_multi_farm_financial"]:::highlight
    farm_multi_farm_procurement["farm_multi_farm_procurement"]:::highlight
    farm_operation["farm_operation"]:::highlight
    farm_pos["farm_pos"]:::highlight
    farm_robotics["farm_robotics"]:::highlight
    farm_sale_ch["farm_sale_ch"]:::highlight
    farm_supply["farm_supply"]:::highlight
    farm_supply_logistics["farm_supply_logistics"]:::highlight
    farm_supply_procurement["farm_supply_procurement"]:::highlight
    farm_supply_quality["farm_supply_quality"]:::highlight
    farm_valuation["farm_valuation"]:::highlight
    farm_weather["farm_weather"]:::highlight
    farm_operation["farm_operation"]:::highlight
    farm_agri_science --> farm_core
    farm_agri_science --> farm_iot
    farm_agritourism --> farm_core
    farm_ai_core --> farm_core
    farm_ai_llm_integration --> farm_ai_core
    farm_ai_llm_integration --> farm_core
    farm_biological_valuation --> farm_core
    farm_csa --> farm_core
    farm_data_security --> farm_core
    farm_ecology --> farm_core
    farm_ecology --> farm_esg
    farm_entity_reg --> farm_core
    farm_esg --> farm_core
    farm_financial_core --> farm_core
    farm_financial_credit --> farm_core
    farm_financial_credit --> farm_financial_core
    farm_financial_insurance --> farm_core
    farm_financial_insurance --> farm_financial_core
    farm_financial_valuation --> farm_biological_valuation
    farm_financial_valuation --> farm_core
    farm_financial_valuation --> farm_financial_core
    farm_greenhouse --> farm_agri_science
    farm_greenhouse --> farm_core
    farm_greenhouse --> farm_iot
    farm_insurance --> farm_agri_science
    farm_insurance --> farm_core
    farm_iot --> agri_iot
    farm_iot --> farm_core
    farm_multi_farm --> farm_core
    farm_multi_farm_equipment --> farm_multi_farm
    farm_multi_farm_financial --> farm_multi_farm
    farm_multi_farm_procurement --> farm_multi_farm
    farm_operation --> farm_agri_science
    farm_operation --> farm_ai_core
    farm_operation --> farm_core
    farm_pos --> farm_core
    farm_robotics --> farm_core
    farm_robotics --> farm_iot
    farm_sale_ch --> farm_core
    farm_supply --> farm_core
    farm_supply_logistics --> farm_core
    farm_supply_logistics --> farm_supply
    farm_supply_procurement --> farm_core
    farm_supply_procurement --> farm_supply
    farm_supply_quality --> farm_core
    farm_supply_quality --> farm_supply
    farm_supply_quality --> farm_supply_procurement
    farm_valuation --> farm_biological_valuation
    farm_valuation --> farm_core
    farm_valuation --> farm_financial_core
    farm_valuation --> farm_financial_valuation
    farm_weather --> farm_core
    farm_weather --> farm_iot
    farm_operation --> farm_agri_science
```

## Industry Apps (垂直应用层)

```mermaid
graph TD
    classDef default fill:#fefefe,stroke:#333,stroke-width:1px,color:#000;
    classDef highlight fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000;
    farm_operation["farm_operation"]:::highlight
    farm_agricultural_processing["farm_agricultural_processing"]:::highlight
    farm_ai_decision["farm_ai_decision"]:::highlight
    farm_ai_vision["farm_ai_vision"]:::highlight
    farm_apiculture["farm_apiculture"]:::highlight
    farm_aquaculture["farm_aquaculture"]:::highlight
    farm_breeding["farm_breeding"]:::highlight
    farm_cert_ch["farm_cert_ch"]:::highlight
    farm_certification["farm_certification"]:::highlight
    farm_crisis["farm_crisis"]:::highlight
    farm_crop["farm_crop"]:::highlight
    farm_dashboard["farm_dashboard"]:::highlight
    farm_disaster_risk["farm_disaster_risk"]:::highlight
    farm_equipment["farm_equipment"]:::highlight
    farm_esg_carbon["farm_esg_carbon"]:::highlight
    farm_esg_fair_trade["farm_esg_fair_trade"]:::highlight
    farm_esg_report["farm_esg_report"]:::highlight
    farm_esg_risk["farm_esg_risk"]:::highlight
    farm_esg_social["farm_esg_social"]:::highlight
    farm_exchange["farm_exchange"]:::highlight
    farm_fermentation["farm_fermentation"]:::highlight
    farm_field_crops["farm_field_crops"]:::highlight
    farm_finance_gov["farm_finance_gov"]:::highlight
    farm_financial_basic["farm_financial_basic"]:::highlight
    farm_financial_government["farm_financial_government"]:::highlight
    farm_floriculture["farm_floriculture"]:::highlight
    farm_hr["farm_hr"]:::highlight
    farm_isl["farm_isl"]:::highlight
    farm_knowledge["farm_knowledge"]:::highlight
    farm_label["farm_label"]:::highlight
    farm_land_mgmt["farm_land_mgmt"]:::highlight
    farm_livestock["farm_livestock"]:::highlight
    farm_machinery_ch["farm_machinery_ch"]:::highlight
    farm_marketing["farm_marketing"]:::highlight
    farm_medicinal_plants["farm_medicinal_plants"]:::highlight
    farm_mobile["farm_mobile"]:::highlight
    farm_mrp["farm_mrp"]:::highlight
    farm_multi_farm["farm_multi_farm"]:::highlight
    farm_multi_farm_quality["farm_multi_farm_quality"]:::highlight
    farm_mushroom["farm_mushroom"]:::highlight
    farm_orchard_horticulture["farm_orchard_horticulture"]:::highlight
    farm_planning["farm_planning"]:::highlight
    farm_processing["farm_processing"]:::highlight
    farm_protected_cultivation["farm_protected_cultivation"]:::highlight
    farm_quality["farm_quality"]:::highlight
    farm_safety["farm_safety"]:::highlight
    farm_seed_industry["farm_seed_industry"]:::highlight
    farm_subsidy["farm_subsidy"]:::highlight
    farm_subsidy_ch["farm_subsidy_ch"]:::highlight
    farm_symbiosis["farm_symbiosis"]:::highlight
    farm_training["farm_training"]:::highlight
    farm_viticulture["farm_viticulture"]:::highlight
    farm_waste_mgmt["farm_waste_mgmt"]:::highlight
    farm_iot["farm_iot"]:::highlight
    farm_operation --> agri_iot
    farm_operation --> farm_operation
    farm_agricultural_processing --> farm_processing
    farm_ai_decision --> farm_agri_science
    farm_ai_decision --> farm_agri_science
    farm_ai_decision --> farm_ai_core
    farm_ai_decision --> farm_ai_core
    farm_ai_decision --> farm_ai_llm_integration
    farm_ai_decision --> farm_ai_vision
    farm_ai_decision --> farm_core
    farm_ai_decision --> farm_operation
    farm_ai_vision --> farm_agri_science
    farm_ai_vision --> farm_ai_core
    farm_ai_vision --> farm_ai_core
    farm_ai_vision --> farm_ai_llm_integration
    farm_ai_vision --> farm_core
    farm_ai_vision --> farm_livestock
    farm_ai_vision --> farm_operation
    farm_ai_vision --> farm_quality
    farm_apiculture --> farm_core
    farm_apiculture --> farm_operation
    farm_aquaculture --> farm_core
    farm_aquaculture --> farm_iot
    farm_aquaculture --> farm_mrp
    farm_aquaculture --> farm_operation
    farm_breeding --> farm_core
    farm_breeding --> farm_operation
    farm_cert_ch --> farm_core
    farm_cert_ch --> farm_marketing
    farm_certification --> farm_core
    farm_certification --> farm_operation
    farm_crisis --> farm_core
    farm_crisis --> farm_safety
    farm_crop --> farm_core
    farm_crop --> farm_operation
    farm_dashboard --> farm_financial_core
    farm_dashboard --> farm_iot
    farm_dashboard --> farm_operation
    farm_dashboard --> farm_weather
    farm_disaster_risk --> farm_core
    farm_disaster_risk --> farm_crisis
    farm_disaster_risk --> farm_operation
    farm_disaster_risk --> farm_weather
    farm_equipment --> farm_operation
    farm_esg_carbon --> farm_core
    farm_esg_carbon --> farm_esg
    farm_esg_carbon --> farm_operation
    farm_esg_fair_trade --> farm_core
    farm_esg_fair_trade --> farm_esg
    farm_esg_fair_trade --> farm_hr
    farm_esg_report --> farm_core
    farm_esg_report --> farm_esg
    farm_esg_report --> farm_hr
    farm_esg_risk --> farm_core
    farm_esg_risk --> farm_esg
    farm_esg_risk --> farm_hr
    farm_esg_social --> farm_core
    farm_esg_social --> farm_esg
    farm_esg_social --> farm_hr
    farm_exchange --> farm_operation
    farm_fermentation --> farm_core
    farm_fermentation --> farm_isl
    farm_fermentation --> farm_processing
    farm_field_crops --> farm_core
    farm_field_crops --> farm_mrp
    farm_field_crops --> farm_operation
    farm_finance_gov --> farm_financial_government
    farm_financial_basic --> farm_core
    farm_financial_basic --> farm_financial_core
    farm_financial_basic --> farm_operation
    farm_financial_government --> farm_core
    farm_financial_government --> farm_financial_basic
    farm_financial_government --> farm_financial_core
    farm_floriculture --> farm_core
    farm_floriculture --> farm_isl
    farm_floriculture --> farm_operation
    farm_hr --> farm_operation
    farm_isl --> farm_core
    farm_isl --> farm_quality
    farm_knowledge --> farm_planning
    farm_label --> farm_core
    farm_label --> farm_marketing
    farm_land_mgmt --> farm_core
    farm_land_mgmt --> farm_operation
    farm_livestock --> farm_core
    farm_livestock --> farm_mrp
    farm_livestock --> farm_operation
    farm_machinery_ch --> farm_core
    farm_machinery_ch --> farm_equipment
    farm_marketing --> farm_core
    farm_marketing --> farm_operation
    farm_marketing --> farm_quality
    farm_medicinal_plants --> farm_core
    farm_medicinal_plants --> farm_operation
    farm_medicinal_plants --> farm_quality
    farm_mobile --> farm_core
    farm_mobile --> farm_operation
    farm_mrp --> farm_core
    farm_mrp --> farm_isl
    farm_multi_farm --> farm_agri_science
    farm_multi_farm --> farm_core
    farm_multi_farm --> farm_equipment
    farm_multi_farm --> farm_financial_core
    farm_multi_farm --> farm_hr
    farm_multi_farm --> farm_marketing
    farm_multi_farm --> farm_multi_farm
    farm_multi_farm --> farm_multi_farm_financial
    farm_multi_farm --> farm_multi_farm_procurement
    farm_multi_farm_quality --> farm_multi_farm
    farm_multi_farm_quality --> farm_quality
    farm_mushroom --> farm_core
    farm_mushroom --> farm_operation
    farm_orchard_horticulture --> farm_core
    farm_orchard_horticulture --> farm_operation
    farm_planning --> farm_hr
    farm_planning --> farm_operation
    farm_processing --> farm_core
    farm_processing --> farm_isl
    farm_processing --> farm_mrp
    farm_processing --> farm_quality
    farm_protected_cultivation --> farm_core
    farm_protected_cultivation --> farm_iot
    farm_protected_cultivation --> farm_operation
    farm_quality --> farm_core
    farm_quality --> farm_operation
    farm_safety --> farm_core
    farm_safety --> farm_operation
    farm_seed_industry --> farm_agricultural_processing
    farm_seed_industry --> farm_breeding
    farm_seed_industry --> farm_core
    farm_seed_industry --> farm_isl
    farm_subsidy --> farm_core
    farm_subsidy --> farm_mobile
    farm_subsidy_ch --> farm_core
    farm_subsidy_ch --> farm_operation
    farm_subsidy_ch --> farm_subsidy
    farm_symbiosis --> farm_aquaculture
    farm_symbiosis --> farm_core
    farm_symbiosis --> farm_isl
    farm_symbiosis --> farm_operation
    farm_training --> farm_core
    farm_training --> farm_operation
    farm_viticulture --> farm_agricultural_processing
    farm_viticulture --> farm_core
    farm_viticulture --> farm_isl
    farm_viticulture --> farm_operation
    farm_waste_mgmt --> farm_core
    farm_waste_mgmt --> farm_livestock
    farm_waste_mgmt --> farm_quality
    farm_iot --> agri_iot
    farm_iot --> farm_agri_science
    farm_iot --> farm_operation
```

## Intelligence & Compliance (智控合规层)

```mermaid
graph TD
    classDef default fill:#fefefe,stroke:#333,stroke-width:1px,color:#000;
    classDef highlight fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000;
    farm_ai_agent["farm_ai_agent"]:::highlight
    farm_ai_robotics_bridge["farm_ai_robotics_bridge"]:::highlight
    farm_esg_circular["farm_esg_circular"]:::highlight
    farm_esg_compliance["farm_esg_compliance"]:::highlight
    farm_esg_environmental["farm_esg_environmental"]:::highlight
    farm_esg_sustainability["farm_esg_sustainability"]:::highlight
    farm_green_monitor["farm_green_monitor"]:::highlight
    farm_input_reg["farm_input_reg"]:::highlight
    farm_live_streaming["farm_live_streaming"]:::highlight
    farm_supply["farm_supply"]:::highlight
    farm_supply_analytics["farm_supply_analytics"]:::highlight
    farm_winery["farm_winery"]:::highlight
    farm_ai_agent --> farm_agri_science
    farm_ai_agent --> farm_ai_core
    farm_ai_agent --> farm_ai_decision
    farm_ai_agent --> farm_ai_llm_integration
    farm_ai_agent --> farm_ai_vision
    farm_ai_agent --> farm_core
    farm_ai_agent --> farm_financial_insurance
    farm_ai_agent --> farm_operation
    farm_ai_agent --> farm_robotics
    farm_ai_robotics_bridge --> farm_ai_agent
    farm_ai_robotics_bridge --> farm_robotics
    farm_ai_robotics_bridge --> farm_robotics
    farm_esg_circular --> farm_core
    farm_esg_circular --> farm_equipment
    farm_esg_circular --> farm_esg
    farm_esg_circular --> farm_esg_environmental
    farm_esg_circular --> farm_operation
    farm_esg_compliance --> farm_agri_science
    farm_esg_compliance --> farm_ai_decision
    farm_esg_compliance --> farm_esg
    farm_esg_compliance --> farm_esg_circular
    farm_esg_compliance --> farm_esg_environmental
    farm_esg_compliance --> farm_esg_risk
    farm_esg_compliance --> farm_financial_core
    farm_esg_compliance --> farm_supply_analytics
    farm_esg_compliance --> farm_supply_logistics
    farm_esg_environmental --> farm_agri_science
    farm_esg_environmental --> farm_ai_decision
    farm_esg_environmental --> farm_core
    farm_esg_environmental --> farm_ecology
    farm_esg_environmental --> farm_esg
    farm_esg_environmental --> farm_iot
    farm_esg_environmental --> farm_operation
    farm_esg_sustainability --> farm_core
    farm_esg_sustainability --> farm_esg
    farm_esg_sustainability --> farm_esg_carbon
    farm_esg_sustainability --> farm_esg_circular
    farm_esg_sustainability --> farm_esg_environmental
    farm_esg_sustainability --> farm_financial_core
    farm_esg_sustainability --> farm_operation
    farm_green_monitor --> farm_core
    farm_green_monitor --> farm_esg
    farm_green_monitor --> farm_esg_report
    farm_green_monitor --> farm_operation
    farm_green_monitor --> farm_supply
    farm_input_reg --> farm_operation
    farm_input_reg --> farm_supply
    farm_live_streaming --> farm_marketing
    farm_live_streaming --> farm_supply
    farm_supply --> farm_core
    farm_supply --> farm_supply_analytics
    farm_supply --> farm_supply
    farm_supply --> farm_supply_procurement
    farm_supply --> farm_supply_quality
    farm_supply_analytics --> farm_ai_decision
    farm_supply_analytics --> farm_core
    farm_supply_analytics --> farm_supply
    farm_winery --> farm_core
    farm_winery --> farm_isl
    farm_winery --> farm_processing
    farm_winery --> farm_viticulture
```
