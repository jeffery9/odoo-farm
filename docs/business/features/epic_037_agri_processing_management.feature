Feature: Epic 037 Agri-Processing Management
  As a Workshop Supervisor or Factory Manager
  I want to manage processing recipes, track batch ancestry, and monitor energy consumption
  So that I can standardize processing workflows, ensure quality, and optimize costs

  @US-037-01 @Logic @Yield
  Scenario: Primary processing input-output balance and grading
    Given a processing order for vegetable grading
    When I record the input of 100kg of raw vegetables
    Then the system must enforce an output balance (e.g. 60kg Grade A, 30kg Grade B, 10kg Loss)
    And it must allow the simultaneous stock entry of primary and by-products

  @US-037-03 @Traceability @DNA
  Scenario: Full batch ancestry and reverse traceability
    Given a finished product package with a QR code
    When I scan the QR code for traceability
    Then the system must provide a reverse path to all intermediate processing lots
    And ultimately locate the original farm parcel and harvest date

  @US-037-05 @Blocking @Yield
  Scenario: Processing loss tolerance management and blocking
    Given a recipe with a "max_loss_rate" of 5%
    When a manufacturing order (MO) is completed with a 10% loss
    Then the system must automatically hang the MO status and block inventory entry
    And require a supervisor's approval to proceed

  @US-037-11 @Recipe @Correction
  Scenario: Automated recipe correction based on raw material attributes
    Given a raw material lot with a recorded "Sugar Content" from a lab test
    When a processing order is generated for this lot
    Then the system must automatically adjust the additive quantities in the recipe
    And apply a compensation function to maintain consistent product quality
