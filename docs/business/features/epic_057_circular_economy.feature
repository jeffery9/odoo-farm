Feature: Epic 057 Circular Economy
  As a Sustainability Officer or Environmental Specialist
  I want to track waste-to-resource conversion and spatial nutrient cycles
  So that I can minimize external inputs and improve the farm's ESG performance

  @US-057-01 @Nutrient @Lifecycle
  Scenario: Waste resource registration and fermentation status machine
    Given I am an environmental specialist
    And the system uses the "RAW_WASTE" to "MATURE_COMPOST" state machine
    When I record a fermentation task for livestock waste inheriting "NutrientMixin"
    Then the system must pre-estimate the NPK content of the waste
    And automatically link the record to the parcel's "Nutrient Return" ledger

  @US-057-02 @Valuation @SupplyChain
  Scenario: Internal resource conversion and fertilizer procurement deduction
    Given a completed fermentation task yielding organic fertilizer
    When the system performs a value reassessment based on "BasePPOCritic" logic
    Then it must automatically suggest a deduction for future chemical fertilizer purchases based on the NPK content
    And generate the organic fertilizer lot via "mrp.production" mapped as an "Intervention"

  @US-057-05 @A2A @Orchestration
  Scenario: Multi-farm resource coordination via Agent-to-Agent (A2A) protocol
    Given a surplus of organic waste at Farm A and a demand at Farm B
    When the farm agents publish signals on the "Agent Social Network"
    Then they must automatically negotiate and schedule a resource transfer via A2A protocol
    And use the "Internal_Netting_Engine" to settle the cross-farm logistics and resource value

  @US-057-06 @GIS @Logistics
  Scenario: Spatial routing for optimal circular economy nodes
    Given a sustainability officer seeking to minimize carbon footprint for waste transport
    When the system calls PostGIS "ST_Distance" to find the nearest processing node within 10km
    Then it must provide an optimal routing path
    And display a "Nutrient Map Layer" using "ST_Interpolate" to show soil capacity for absorption
