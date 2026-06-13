Feature: Epic 020 Nursery & Breeding
  As a Breeding Expert or Nursery Manager
  I want to track germination, grafting, and pedigree information
  So that I can optimize variety quality and ensure high seedling survival rates

  @US-020-01 @Nursery @Inventory
  Scenario: Nursery factory management and seedling age tracking
    Given a nursery lot is in the "germination" stage
    When the nursery work is finished
    Then the system must trigger a "stock.picking" to move seedlings to the field
    And it should calculate the "Cumulative Seedling Age" as an initial parameter for the field tasks

  @US-020-03 @Quality @Testing
  Scenario: Germination and vigor testing for seed source quality
    Given a batch of seeds is being received
    When a germination test is performed in the lab
    Then the system must use the "Germination %" to update the "Suggested Sowing Rate" in production orders
    And the record must conform to the bilingual quality report standard

  @US-020-04 @Grafting @Production
  Scenario: Grafting and tissue culture loss tracking
    Given a nursery manufacturing order (MO) for grafting
    When the process is complete
    Then the system must record the balance between "Input Scions/Seeds" and "Output Seedlings"
    And it should analyze the economic efficiency of different rootstock combinations

  @US-020-05 @Pedigree @Breeding
  Scenario: Pedigree tracking for genetic diversity
    Given a breeding program with multiple generations
    When I register a new variety or cross
    Then the system must support recording parental combinations and genetic traits
    And it should provide a visualization of the multi-generational pedigree tree
