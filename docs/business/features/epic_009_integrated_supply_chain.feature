Feature: Epic 009 Integrated Supply Chain
  As a Supply Chain Manager or Warehouse Admin
  I want to integrate demand, production, and supply operations
  So that I can optimize inventory levels and ensure compliance

  @US-009-01 @MTO @Production
  Scenario: Demand-driven production (MTO) with growth duration check
    Given a sales order is created for a crop with a specific "growth_duration"
    When the sales order confirmation is attempted with a delivery date too early
    Then the system must block the order with a UserError regarding growth cycle
    And I should be able to drill down into the related production task progress

  @US-009-06 @Procurement @Compliance
  Scenario: Supplier compliance verification and PO locking
    Given a purchase order is created for a supplier
    When the system checks the supplier's certificate validity
    Then if the certificate is expired, the "Confirm" button must be hard-locked
    And an Activity must be created for the "Compliance Officer" to update the credentials

  @US-009-07 @IOT @ShelfLife
  Scenario: Dynamic shelf-life prediction based on IoT temperature logs
    Given a batch of produce in transit with IoT temperature sensors
    When the system detects a cumulative temperature deviation (Arrhenius Equation)
    Then the "Expiry Date" of the lot must be updated automatically
    And if the remaining shelf-life drops to 20%, a "Priority Sale" Activity must be triggered

  @US-009-20 @FEFO @Warehouse
  Scenario: FEFO (First Expired First Out) pick strategy
    Given multiple lots of the same product with different expiry dates
    When the system generates a picking order
    Then it must automatically suggest the lot with the earliest expiry date
    And if a worker scans a later lot on a PDA, a red hard warning must be displayed
