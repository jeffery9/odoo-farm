Feature: Epic 128 Central Kitchen Operations
  As an Executive Chef or CK Dispatcher
  I want standardized multi-terminal demand aggregation and digital HACCP controls
  So that I can optimize centralized food production and ensure food safety during cold-chain distribution

  @US-128-01 @Production @Aggregation
  Scenario: Multi-terminal demand auto-aggregation and MO triggering
    Given multiple restock requests from direct-operated stores and e-commerce platforms
    When the CK dispatcher runs the "Demand Aggregation Engine"
    Then it must automatically consolidate orders by product category
    And generate summarized Manufacturing Orders (MO) while calculating raw material shortages

  @US-128-02 @Recipe @Scaling
  Scenario: Standardized large-scale recipe and dynamic scale conversion
    Given a standardized meal recipe with a base yield
    When a production batch is scaled up (e.g. from 100 to 5000 servings)
    Then the system must apply a precise scaling factor to all ingredients
    And generate a bilingual picking list aligned with warehouse packaging specifications

  @US-128-03 @Inventory @FEFO
  Scenario: Serialized inventory management for fresh-cut and semi-finished products
    Given a completed batch of semi-finished products
    When the warehouse manager registers the stock lot
    Then the system must lock the production timestamp and calculate the exact expiry time
    And enforce strict FEFO (First-Expired-First-Out) picking logic on the PDA terminal

  @US-128-05 @HACCP @Safety
  Scenario: Digital HACCP critical point management and production blocking
    Given an active production workflow requiring thermal processing
    When the operator records the core temperature of the batch
    Then the system must verify if it meets the HACCP critical limit (Epic 025)
    And strictly block the batch from proceeding to the packaging stage if the limit is not met
