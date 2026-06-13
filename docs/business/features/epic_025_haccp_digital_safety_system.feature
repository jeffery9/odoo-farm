Feature: Epic 025 HACCP Digital Safety System
  As a Quality Manager or Compliance Officer
  I want a digital HACCP framework with real-time critical control point (CCP) monitoring
  So that I can prevent food safety incidents and ensure full compliance with international standards

  @US-025-01 @HACCP @CCP
  Scenario: Critical Control Point (CCP) and threshold modeling
    Given a production recipe for processed agri-food
    When I define the Critical Control Points (CCP) in the "farm.haccp.point" model
    Then the system must allow me to set the "critical_limit_min" and "critical_limit_max"
    And it should display these points with a red high-visibility marker in the UI

  @US-025-02 @Safety @Blocking
  Scenario: Real-time violation blocking and lot isolation
    Given a manufacturing order with a CCP requirement
    When the recorded detection data (e.g. sterilization temp) is outside the critical limits
    Then the system must block the "Mark as Done" action for the order
    And the lot must be automatically isolated with a "blocked_by_haccp" status

  @US-025-03 @Workflow @Correction
  Scenario: Mandatory corrective action flow for HACCP violations
    Given a lot is blocked due to a HACCP violation
    When the operator initiates a "Corrective Measure" action
    Then the system must require a documented measure and supervisor approval before unlocking the lot
    And the corrective record must be embedded in the "AgriTraceabilityMixin" fingerprint

  @US-025-04 @Reporting @Audit
  Scenario: One-click HACCP audit package generation
    Given a finished product batch
    When the compliance officer requests an "Audit Package"
    Then the system must automatically aggregate CCP records, IoT environment curves, and corrective logs into a single report
    And the report must be signed for authenticity
