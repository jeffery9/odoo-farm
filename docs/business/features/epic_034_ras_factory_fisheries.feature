Feature: Epic 034 RAS Factory Fisheries
  As an Operations Supervisor or Farm Manager
  I want to monitor life support system (LSS) components and metabolic loads
  So that I can ensure zero-risk operations in high-density RAS aquaculture

  @US-034-01 @LSS @Maintenance
  Scenario: LSS component lifecycle and UV lamp warning
    Given a Life Support System (LSS) managed as "farm.aquaculture.lss"
    When the system tracks the UV lamp usage hours
    Then it must trigger a replacement warning when the remaining life is < 10%
    And it should monitor the status of circulation pumps and bio-filters

  @US-034-02 @Metabolism @Gate
  Scenario: Ammonia load prediction and feeding gate
    Given a fish tank with a specific biomass
    When I record the feeding quantity
    Then the system must calculate the "Ammonia Load" (Feed * Protein % * 0.05)
    And if the ammonia load exceeds the bio-filter capacity, the "AgriQualityGateMixin" must block further feeding orders

  @US-034-03 @Energy @Efficiency
  Scenario: Power Usage Effectiveness (PUE) and energy cost per KG
    Given an RAS production cycle
    When the system aggregates the total energy consumption (kWh) for pumps, temperature control, and aeration
    Then it must calculate the "Energy Cost per KG" (kWh/kg) of fish output via "AgriResourceConsumptionMixin"

  @US-034-04 @IOT @Defense
  Scenario: Automatic closed-loop defense for water circulation failure
    Given real-time monitoring of circulation flow and power status
    When a flow drop or power interruption is detected via "industrial_iot"
    Then the system must automatically trigger emergency aeration and enter "Survival Mode"
    And create an urgent "AgriIncidentAlertMixin" task
