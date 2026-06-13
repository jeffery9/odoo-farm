Feature: Epic 038 Agri-Quality Inspection
  As a Quality Manager or Lab Technician
  I want a standard process for quality inspection and digital fingerprints
  So that I can ensure product quality and provide an objective basis for community settlement

  @US-038-01 @Inspection @Standard
  Scenario: Define quality inspection points and tolerance ranges
    Given I am a quality manager
    When I define an inspection item for "Sugar Content" with a tolerance of "+/- 0.5%"
    Then the system must support bilingual (Chinese/English) display for the standard
    And allow me to assign this point to a specific harvest task

  @US-038-02 @Workflow @Locking
  Scenario: Automated quality check trigger and lot locking
    Given a harvest manufacturing order (MO) is completed
    When the production is marked as done
    Then the system must automatically generate a "Quality Check" record
    And the resulting "stock.lot" must be locked in a "To be inspected" state until confirmed

  @US-038-04 @HardBlock @Activity
  Scenario: Handling of failed quality inspections and sales blocking
    Given a "Quality Check" result is recorded as "Failed"
    When the inspector submits the results
    Then the system must force the "stock.lot" status to "locked"
    And create an "Exception Disposal Approval" Activity for the quality supervisor
    And prevent manual unlocking until the approval flow is closed

  @US-038-09 @Blockchain @Fingerprint
  Scenario: Digital quality fingerprint generation and valuation link
    Given a successful quality inspection
    When the inspection is finalized
    Then the system must generate a SHA-256 "Quality Fingerprint" hash
    And the fingerprint must include chemical indices and inspector reputation
    And the quality grade must determine the "Quality Factor" for community settlement (Epic 014)
