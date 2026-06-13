Feature: Epic 022 Mushroom Management
  As a Mushroom Technician or Production Manager
  I want to manage substrate recipes, flush yields, and environmental conditions
  So that I can optimize mushroom production and minimize contamination risks

  @US-022-01 @Mushroom @LifeLog
  Scenario: Mushroom batch digital twin and mycelium tracking
    Given a mushroom batch inheriting "AgriGrowthCycleMixin"
    When I record the inoculation date and mycelium colonization progress
    Then the "farm.mushroom.batch" (proxy of "stock.lot") must track the status
    And it should trigger an alert if the "contamination_rate" exceeds the threshold

  @US-022-02 @Recipe @Sanity
  Scenario: Substrate recipe and sterilization gate
    Given an artisan defining a substrate recipe with specific C/N ratio and moisture
    When the sterilization process is performed
    Then the "AgriQualityGateMixin" must enforce the validation of sterilization temperature and duration
    And the "NutrientMixin" should calculate the total nutrient content of the substrate

  @US-022-03 @Flush @Yield
  Scenario: Multi-flush yield tracking and biological efficiency
    Given a mushroom production order ("farm.mushroom.production" proxying "mrp.production")
    When I record harvests across multiple flushes (1st, 2nd, 3rd)
    Then the system must calculate the "Biological Efficiency" (BE)
    And track the quality and weight for each flush separately

  @US-022-04 @IOT @Defense
  Scenario: Environmental defense for CO2 and humidity in fruiting rooms
    Given IoT sensors are monitoring CO2 levels in the fruiting room
    When the CO2 concentration exceeds the safe threshold
    Then the system must automatically trigger the ventilation equipment via Agent instructions
    And create an "AgriIncidentAlertMixin" notification for the operator
