Feature: Epic 067 Agri OPE Intelligence
  As a Farm Owner or Group Manager
  I want a calculated OPE engine and area-weighted performance rollups
  So that I can quantify production effectiveness and resource utilization efficiency

  @US-067-01 @Logic @OPE
  Scenario: Overall Production Effectiveness (OPE) calculation engine
    Given a finished production unit
    When the system runs the OPE calculation
    Then it must include three dimensions: Availability (land), Performance (growth), and Quality (grade)
    And display the balanced OPE score on the real-time dashboard

  @US-067-02 @Algorithm @Rollup
  Scenario: Area-weighted rollup aggregation for group management
    Given multiple parcels with different sizes and performance scores
    When a group manager views the consolidated performance
    Then the "farm.ope.mixin" must apply a weighted average based on the parcel area
    And ensure larger parcels have a higher impact on the final rollup score

  @US-067-04 @Benchmark @Pivot
  Scenario: Benchmarking OPE across different technical routes
    Given production records using different technical routes (e.g. Drip vs Sprinkle)
    When I view the OPE pivot table
    Then the system must support grouping by "Technical Route"
    And allow me to compare the conversion efficiency of each method

  @US-067-05 @Efficiency @WUE
  Scenario: Water and Nutrient Use Efficiency (WUE/NUE) analysis
    Given a harvested lot with recorded resource inputs (water, fertilizer)
    When the system calculates the efficiency indices
    Then it must provide a ratio of "Total Output / Total Input"
    And link the quality score to the final resource efficiency KPI
