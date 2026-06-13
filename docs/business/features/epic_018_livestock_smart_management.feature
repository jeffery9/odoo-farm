Feature: Epic 018 Livestock Smart Management
  As a Livestock Technician or Financial Director
  I want individual-level life-log tracking and real-time efficiency monitoring
  So that I can optimize FCR and provide financial-grade asset valuation

  @US-018-01 @Livestock @Status
  Scenario: Individual life-log and reproductive state machine
    Given I am a livestock technician
    And the system uses "farm.lot.livestock" proxying "stock.lot"
    When I register a livestock's reproductive status (e.g., Pregnant, Lactating)
    Then the system must track the state transition automatically
    And the biological quantity must be managed via "AgriBiologicalInventoryMixin"

  @US-018-02 @FCR @ADG
  Scenario: Real-time FCR and ADG monitoring with alerts
    Given a livestock lot with weight and feeding records
    When the system calculates the Food Conversion Ratio (FCR) and Average Daily Gain (ADG)
    Then the ADG must be compared against the variety's standard curve
    And if the ADG is 15% lower than standard, an "AgriIncidentAlertMixin" warning must be triggered

  @US-018-03 @Health @Compliance
  Scenario: Dynamic vaccination scheduling and PHI blocking
    Given a livestock lot scheduled for vaccination
    When the vaccination is recorded via "AgriCertificationStatusMixin"
    Then the system must calculate the Post-Harvest Interval (PHI)
    And it must block any "stock.picking" for the lot if the PHI has not ended

  @US-018-04 @Finance @Valuation
  Scenario: Dynamic live-asset valuation for mortgage
    Given a livestock lot with real-time weight and market price data
    When the financial director requests an asset valuation
    Then the system should generate a valuation report via "AgriBiologicalValuationMixin"
    And the report must include a quality fingerprint anchored to the latest weighing evidence
