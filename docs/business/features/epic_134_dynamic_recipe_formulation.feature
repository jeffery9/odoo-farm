Feature: Epic 134 Dynamic Recipe Formulation
  As a Formula R&D Manager or Production Supervisor
  I want dynamic BOM formulas based on raw material properties
  So that I can ensure batch-to-batch consistency and reduce additive waste in food processing

  @US-134-01 @Recipe @AST
  Scenario: Define formulation formula with property-based compensation
    Given a Bill of Materials (BOM) for agricultural processing
    When the R&D manager defines a dynamic compensation formula for an additive (e.g. sugar)
    Then the system must validate the formula using an AST parser
    And enforce the configuration of "Min_Qty" and "Max_Qty" boundary limits

  @US-134-02 @Production @Adjustment
  Scenario: Dynamic adjustment of material consumption during picking
    Given a drafted Manufacturing Order (MO)
    When a specific raw material lot is selected with a known property value (e.g. Brix = 9%)
    Then the system must automatically recalculate the required quantity for the compensating additive
    And display a "Dynamically Compensated" indicator, blocking manual modification by operators

  @US-134-03 @Traceability @Log
  Scenario: Traceability log for dynamic formulation adjustments
    Given a completed Manufacturing Order with dynamic compensation
    When the quality inspector views the final product's "stock.lot" traceability tree
    Then it must include a "Formulation Adjustment Log"
    And explicitly state the original quantity, the adjusted quantity, and the causal raw material property
