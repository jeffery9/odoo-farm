Feature: Epic 045 Agri-Science Base
  As an Agricultural Specialist or Process Engineer
  I want a biology-based reference system with physiological stages and growth models
  So that I can implement adaptive production based on crop science

  @US-045-01 @Science @Variety
  Scenario: Define physiological fingerprints for varieties
    Given a variety defined in "product.product"
    When I configure the "Three-point Temperatures" (T-base, T-opt, T-max)
    Then the system must use these as limits for growth model calculations
    And store NPK sensitivity weights for the variety

  @US-045-02 @GDD @Stages
  Scenario: GDD-driven physiological stage transitions
    Given a variety inheriting "farm.agri.science.mixin"
    When the "Current GDD" reaches the threshold for the next stage (e.g. V1 to V2)
    Then the system must automatically trigger the stage transition
    And display a "Physiological Progress Bar" on the execution interface

  @US-045-03 @SPC @Environmental
  Scenario: Physiological environment matrix and SPC linkage
    Given a specific physiological stage of a crop
    When the actual environment readings deviate from the "Safety Zone" matrix
    Then the "process_status" must be flagged as "Out of Control"
    And the execution must be locked via the SPC mechanism (Epic 044)

  @US-045-06 @AI @Vision
  Scenario: Visual phenology calibration feedback
    Given an AI vision system monitoring the crop (Epic 081)
    When "farm_ai_vision" identifies a specific phenology stage
    Then the system must use the visual stage as the "Ground Truth"
    And override the mathematical GDD prediction if a discrepancy exists
