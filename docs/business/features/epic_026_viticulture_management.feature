Feature: Epic 026 Viticulture Management
  As a Winemaker or Vineyard Manager
  I want terroir-aware plot management and ripeness prediction
  So that I can optimize grape quality and ensure precise harvest timing

  @US-026-01 @Terroir @GIS
  Scenario: Terroir fingerprint and plot DNA registration
    Given I am defining a vineyard plot via "farm.viticulture.plot"
    When I record the slope, aspect, and soil composition via "GeoSpatialMixin" and "AgriSoilAnalysisMixin"
    Then the system must store these as "Terroir Fingerprints"
    And lock the pH and organic matter data in the plot DNA

  @US-026-03 @GDD @Ripeness
  Scenario: Brix/Acid ratio monitoring and harvest window prediction
    Given a vineyard plot in the ripening stage
    When I record the daily sugar (Brix) and acidity levels
    Then the "AgriGrowthCycleMixin" should track the cumulative GDD and sugar curves
    And it should trigger a "Harvest Alert" when the Brix/Acid ratio reaches the optimal balance point

  @US-026-04 @Traceability @Pressing
  Scenario: Pressing efficiency and juice yield verification
    Given a fresh grape lot harvested from a specific plot
    When the lot is processed in the press room
    Then the system must calculate the "Extraction Yield" (Liters per KG)
    And the juice lot must inherit the fingerprint from the fresh grape lot via "AgriTraceabilityMixin"
