Feature: Epic 125 Fungi Multi-Flush Management
  As a Fungi Technician or Farm Worker
  I want to track spawn batches and manage multi-flush harvests
  So that I can optimize biological conversion rates and trace yields back to specific inoculations

  @US-125-01 @Traceability @Inoculation
  Scenario: Mushroom spawn batch tracking and inoculation hierarchy
    Given a new batch of mushroom spawn (Child Lot) inoculated from a master culture (Parent Lot)
    When the technician registers the inoculation
    Then the system must create a "Parent-Child" lot relationship
    And ensure the child lot inherits all genetic attributes from the parent lot
    And provide a heat map showing the incubation status by "Room/Rack" location

  @US-125-02 @Harvest @Flush
  Scenario: "Flush Cycle" harvest recording and biological conversion analysis
    Given an active mushroom production intervention
    When the worker performs a harvest and records the quantity
    Then the system must support multiple stock receipts for the same intervention
    And automatically tag each receipt with the current "Flush No." (e.g. Flush 1, Flush 2)
    And generate a pivot report showing the yield decline curve across successive flushes
