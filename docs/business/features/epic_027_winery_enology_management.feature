Feature: Epic 027 Winery & Enology Management
  As a Winemaker or Cellar Master
  I want real-time fermentation monitoring and barrel asset tracking
  So that I can ensure the quality of fine wines and provide bottle-level traceability

  @US-027-01 @Winery @Fermentation
  Scenario: Fermentation kinetics monitoring and IoT integration
    Given a wine batch in a fermentation tank
    When the "industrial_iot" sensors record the tank temperature and density (Brix)
    Then the system must plot the sugar-to-alcohol conversion curve
    And calculate the "Potential Alcohol" based on the initial and current Brix

  @US-027-02 @Cellar @Barrels
  Scenario: Oak barrel aging and asset tracking
    Given a cellar with multiple oak barrels ("farm.winery.vessel" proxying "mrp.workcenter")
    When a wine lot is moved into a barrel for aging
    Then the system must track the barrel's material, usage history, and current wine content
    And record the barrel's "historical contribution" via "AgriTraceabilityMixin"

  @US-027-03 @Blending @DNA
  Scenario: Multi-batch blending and DNA marriage
    Given a blending operation involving multiple wine lots from different years or plots
    When the master blend is created
    Then the final product hash must aggregate the DNA fingerprints (Parent Lots) of all source wines
    And the recipe must support multi-level nesting

  @US-027-04 @Quality @Gate
  Scenario: Enological laboratory gate for bottling
    Given a wine lot ready for bottling
    When the lab analyst records free SO2, volatile acidity, and residual sugar via "AgriQualityGateMixin"
    Then the system must block the bottling order if any index exceeds the enological standard
