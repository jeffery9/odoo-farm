Feature: Epic 064 Perennial Orchard
  As a Farm Manager or Horticulturist
  I want to track the lifecycle of individual trees and monitor harvest indices
  So that I can optimize pruning, thinning, and orchard renewal strategies

  @US-064-01 @Asset @Lifecycle
  Scenario: Individual tree lifecycle profiling and biological depreciation
    Given an orchard with multiple perennial trees
    When I register an individual tree as a "stock.lot"
    Then the system must link it to an "account.asset" record
    And support biological asset depreciation based on the production cycles

  @US-064-02 @GDD @Ripeness
  Scenario: Dynamic harvest index monitoring (Sugar/Acidity) and prediction
    Given an individual fruit tree lot
    When I record ripeness sampling data (e.g. Brix level)
    Then the system must predict the optimal harvest date based on GDD trends (Epic 002)
    And display a "Harvest Suggestion" icon on the mobile interface

  @US-064-03 @GIS @Renewal
  Scenario: Low-yield asset identification and replacement planning
    Given an orchard with multi-year production records
    When I view the GIS "Yield Distribution Heatmap"
    Then the system should automatically identify low-yield trees that need replacement
    And generate a "Renewal Checklist" for the next production season

  @US-064-04 @Logic @Thinning
  Scenario: Perennial crop load management and thinning guidance
    Given a tree lot at the flowering stage
    When the system calculates the "Target Fruit Count" based on tree age and historical OPE (Epic 067)
    Then it must provide guidance for flower/fruit thinning to prevent biennial bearing
    And allow me to record the thinning ratio via the PWA
