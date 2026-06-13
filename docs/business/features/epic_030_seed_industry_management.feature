Feature: Epic 030 Seed Industry Management
  As a Breeding Expert or Quality Inspector
  I want to track parental lineage, manage seed quality gates, and ensure distribution compliance
  So that I can protect variety rights (PVP) and ensure seed vitality for farmers

  @US-030-01 @Traceability @Breeding
  Scenario: Parental lineage and DNA-level hash inheritance
    Given a new seed batch created via "farm.seed.batch"
    When the lot is registered with its Parent 1 (P1) and Parent 2 (P2)
    Then the "AgriTraceabilityMixin" must aggregate the hash fingerprints from both parents
    And create a multi-level genetic hash chain for the lot

  @US-030-02 @Quality @Gate
  Scenario: Seed "Four-Tests" quality gate for vitality and purity
    Given a seed batch being received into inventory
    When the quality inspector records the germination rate, purity, and moisture data
    Then the "AgriQualityGateMixin" must verify the results against national standards (e.g. 85% germination)
    And if the standards are not met, the lot must be blocked from entering the "Available for Sale" state

  @US-030-03 @Recipe @Coating
  Scenario: Seed treatment and coating process recipe
    Given a processing order for seed coating
    When I define the coating recipe via "farm.seed.recipe"
    Then the "NutrientMixin" must calculate the precise amount of active agents and micronutrients
    And the system must ensure the recipe adheres to the BoM standards

  @US-030-04 @Compliance @PVP
  Scenario: Variety rights (PVP) and distribution compliance check
    Given a sales order for a specific seed batch
    When the order confirmation is initiated
    Then the system must call the compliance logic to verify if the variety has distribution authorization for the target region
    And block the sale if the authorization is missing or expired
