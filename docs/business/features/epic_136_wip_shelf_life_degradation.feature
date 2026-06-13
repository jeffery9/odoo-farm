Feature: Epic 136 WIP Shelf Life Degradation
  As a Quality Assurance Director or Floor Supervisor
  I want dynamic shelf-life degradation tracking based on WIP exposure
  So that I can ensure food safety and prevent spoilage due to production bottlenecks

  @US-136-01 @WIP @TTI
  Scenario: Capture WIP Time-Temperature Indicator (TTI) during processing
    Given a workorder processing temperature-sensitive materials
    When the operator marks the workorder as "Done"
    Then the system must record the exact duration of the operation
    And fetch the average environmental temperature during that period via the IoT gateway

  @US-136-02 @ShelfLife @Penalty
  Scenario: Dynamic expiration date penalty for prolonged WIP exposure
    Given a product with a standard shelf-life of 7 days
    When the TTI data shows the WIP was exposed to high temperatures for a prolonged period
    Then the system must automatically calculate the shelf-life degradation penalty
    And subtract this penalty from the final product lot's "expiration_date"

  @US-136-03 @Alerts @Dashboard
  Scenario: WIP exposure dashboard alerts and meltdown warnings
    Given an active MRP dashboard displaying WIP lots
    When a semi-finished product's exposure time reaches 80% of its degradation threshold
    Then the system must change its visual indicator to orange
    And trigger a red flashing alert and audible warning if it reaches 100%
