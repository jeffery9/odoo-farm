Feature: Epic 050 Intelligent Irrigation Management
  As a Farm Owner or Agronomist
  I want precise irrigation based on soil sensors and AI logic
  So that I can optimize water usage and improve crop health

  @US-050-01 @IOT @Monitoring
  Scenario: Real-time soil moisture monitoring and trend visualization
    Given soil moisture sensors are installed in multiple parcels
    When the sensors report data to the system
    Then I should see a visualization of the moisture distribution map and historical trends
    And the system must trigger an alert if the moisture level drops below the variety's T-base threshold

  @US-050-02 @AI @Irrigation
  Scenario: AI-driven irrigation scheduling with weather integration
    Given an integrated weather forecast service
    When the "ai.decision.engine" calculates the irrigation need
    Then it must account for predicted rainfall within the next 24 hours to avoid over-irrigation
    And automatically generate an execution schedule for the irrigation equipment

  @US-050-04 @ESG @Conservation
  Scenario: Water resource optimization and conservation analysis
    Given a production season with recorded irrigation events
    When the sustainability manager requests a "Water Efficiency Report"
    Then the system must calculate the water resource utilization efficiency index
    And compare the water savings against traditional fixed-schedule irrigation methods
