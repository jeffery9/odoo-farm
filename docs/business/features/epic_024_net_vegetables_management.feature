Feature: Epic 024 Net Vegetables Management
  As a Workshop Supervisor or Quality Control Specialist
  I want to track processing yields and manage hierarchical packaging
  So that I can minimize losses and ensure food safety for fresh-cut vegetables

  @US-024-01 @Logic @Yield
  Scenario: Net vegetable yield tracking and biomass auditing
    Given a fresh vegetable processing order
    When I record the "Gross Input Weight" and "Net Output Weight"
    Then the system must calculate the "Net Yield" percentage
    And it should track the biomass flow of non-edible parts via "NutrientMixin" (Epic 057)

  @US-024-02 @Traceability @Packaging
  Scenario: Hierarchical nesting of packaging and labels
    Given multiple single-package lots
    When I scan them into a crate, and scan the crate into a pallet
    Then the system must maintain the parent-child lot hierarchy
    And the pallet label must contain the traceability hash summaries of all included packages

  @US-024-03 @Safety @Gate
  Scenario: Microbial safety gate and disinfectant monitoring
    Given a vegetable washing and disinfection process
    When I record the disinfectant concentration and E. coli test results via "AgriQualityGateMixin"
    Then the system must block the order from being marked "Done" if the parameters are below the safety threshold
    And it must enforce the validation of all Quality Control Points (QCP)

  @US-024-04 @Algorithm @ShelfLife
  Scenario: Rapid shelf-life prediction for fresh-cut products
    Given a finished fresh-cut vegetable lot
    When the system analyzes the processing time and storage temperature via "AgriGrowthCycleMixin"
    Then it should dynamically update the "Suggested Shelf-life Alert"
    And notify the sales manager of the decay risk
