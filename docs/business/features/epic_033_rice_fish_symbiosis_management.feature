Feature: Epic 033 Rice-Fish Symbiosis Management
  As a Farm Manager or Agronomist
  I want to manage rice-fish symbiotic ecosystems and nutrient cycles
  So that I can optimize symbiotic yields and prevent pesticide toxicity risks

  @US-033-01 @Symbiosis @GIS
  Scenario: Symbiotic plot DNA and water level modeling
    Given I am a farm manager defining a rice-fish parcel
    When I record the planting density and trench-to-field ratio via "GeoSpatialMixin"
    Then the system must map the spatial layout of the field and the peripheral trenches
    And track the required water levels for both rice and fish

  @US-033-02 @Recipe @Nutrient
  Scenario: Symbiotic nutrient conversion in recipes
    Given a symbiotic recipe ("farm.symbiotic.recipe" proxying "mrp.bom")
    When I define the fish waste replacement ratio for nitrogen
    Then the "NutrientMixin" must calculate the "Internal Recycled Nutrients"
    And reduce the required external fertilizer accordingly

  @US-033-03 @Safety @Gate
  Scenario: Pesticide toxicity redline interception for fish safety
    Given a rice field with active fish population
    When I attempt to confirm a "Spraying" intervention
    And the pesticide contains components highly toxic to aquatic life (e.g. Abamectin)
    Then the "AgriQualityGateMixin" must block the "action_confirm" command
    And display a toxicity warning to the operator

  @US-033-04 @Yield @Accounting
  Scenario: Co-harvest tracking and cost allocation for dual outputs
    Given a production cycle in a symbiotic plot
    When I record the harvest of both rice and fish batches
    Then the "farm.symbiotic.order" must support multiple outputs
    And the Rice lot must inherit the "Ecological Fingerprint" from the fish activity
    And common costs must be allocated between the two products
