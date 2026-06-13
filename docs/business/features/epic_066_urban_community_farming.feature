Feature: Epic 066 Urban Community Farming
  As a Citizen or Community Farm Operator
  I want plot adoption logs, shared tool management, and micro-sensor integration
  So that I can enjoy a transparent farm-to-city experience and optimize community resources

  @US-066-01 @Community @Adoption
  Scenario: "One Square Meter" vegetable plot adoption and digital log
    Given I am a citizen adopting a plot
    When the adoption is confirmed
    Then the system must automatically create a "Land Log" channel for me
    And push a photo report every time an intervention is completed on my plot

  @US-066-02 @PWA @Logistics
  Scenario: Shared tool rental and return via QR scanning
    Given a community farm with shared tools
    When I scan a tool's QR code via the PWA
    Then the system must allow me to register the "Check-out" or "Return"
    And automatically send a SMS/notification if the tool is overdue

  @US-066-03 @IOT @MicroSensor
  Scenario: Micro-sensor integration for adopted assets
    Given an adopted plant lot with a low-power micro-sensor
    When the sensor reports micro-environmental data (e.g. soil temp, light)
    Then the system must associate the data with the "adopted_lot_id"
    And push real-time updates to the adopter's subscription feed
