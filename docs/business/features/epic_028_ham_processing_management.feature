Feature: Epic 028 Dry-Cured Ham Management
  As a Processing Supervisor or Cellar Master
  I want to track ham processing from intake to vintage grading
  So that I can ensure quality, calculate dehydration rates, and optimize asset value

  @US-028-01 @Traceability @DNA
  Scenario: Fresh leg intake and DNA inheritance from livestock
    Given I am a processing supervisor
    And a lot of fresh legs is being received
    When I link the intake lot to the source "farm.lot.livestock" batch
    Then the system must automatically inherit the breed and feeding fingerprints
    And record the link in the "AgriTraceabilityMixin"

  @US-028-02 @Math @Yield
  Scenario: Dehydration tracking and weight loss audit
    Given a batch of hams in the curing process
    When the cellar master records periodic weights
    Then the system must calculate the "Weight Loss %" automatically
    And compare the results against the standard process curve
    And trigger an "AgriIncidentAlertMixin" if the rate deviates significantly

  @US-028-03 @IOT @Environment
  Scenario: Cellar environment monitoring and quality gate
    Given a ham cellar equipped with IoT sensors
    When the temperature or humidity deviates from the safety range
    Then the "AgriQualityGateMixin" must automatically block the lot from moving to the next stage
    And record the environmental logs as part of the quality index

  @US-028-04 @Finance @Valuation
  Scenario: Vintage asset dynamic valuation for hams
    Given a batch of cured hams in the cellar
    When the financial manager calculates the asset value
    Then the system must apply a time-based valuation model via "AgriBiologicalValuationMixin"
    And update the value based on the aging duration (12, 24, 36 months)
