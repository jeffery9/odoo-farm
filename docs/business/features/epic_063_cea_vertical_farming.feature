Feature: Epic 063 CEA & Vertical Farming
  As an Agricultural Technician or Operator
  I want automated environmental control and spatial inventory management
  So that I can optimize crop growth in factory-style vertical farming environments

  @US-063-01 @IOT @Automation
  Scenario: Automated fertigation and lighting control
    Given I am a technician in a vertical farm
    When soil sensors or light meters report values outside the threshold
    Then the system must execute the control rules (e.g. turn on pump or lights) within 1 minute
    And all automatic commands must be recorded in the "iiot.command.log"

  @US-063-02 @Inventory @Spatial
  Scenario: Spatial location management for vertical plant beds
    Given a vertical farming facility
    When I define the location structure: Parent -> Shelf -> Bin (Tray)
    Then the system must support this three-level hierarchy for inventory tracking
    And the "Position Layout" view must display the maturity level of each tray using color coding
