Feature: Epic 019 Aquaculture Smart Management
  As a Farm Manager or Technician
  I want water-quality-aware farming and dynamic biomass prediction
  So that I can control risks in high-density aquaculture and optimize yields

  @US-019-01 @GIS @DigitalTwin
  Scenario: Pond digital twin and volume calculation
    Given I am defining a pond in the system
    When I provide its depth and 3D geospatial coordinates via "GeoSpatialMixin"
    Then the system must calculate the "water_volume_m3" automatically
    And the pond must be mapped as a digital twin

  @US-019-02 @IOT @Feeding
  Scenario: Water-linked dynamic feeding based on dissolved oxygen
    Given IoT sensors are monitoring dissolved oxygen and temperature
    When the oxygen level drops below 3mg/L
    Then the system must generate an agent instruction to "Stop Feeding"
    And it should adjust the feeding coefficient based on the current water parameters

  @US-019-03 @Biomass @Inventory
  Scenario: Biomass sampling and survival rate calibration
    Given a pond with an initial stocking quantity
    When I record a periodic sampling of average weight and survival rate
    Then the system must update the total weight prediction via "AgriBiologicalInventoryMixin"
    And it should calculate the current "stocking_density" (total biomass / water volume)

  @US-019-04 @IOT @Alerts
  Scenario: Real-time water quality defense and aeration trigger
    Given dissolved oxygen levels are monitored in real-time
    When the oxygen level drops below the critical redline
    Then the system must automatically trigger the aerator via "industrial_iot"
    And it must create an emergency "AgriIncidentAlertMixin" task
