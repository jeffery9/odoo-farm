Feature: Epic 017 Tea Industry Management
  As a Tea Garden Manager or Tea Master
  I want to track seasonal flushes and refine processing recipes
  So that I can ensure the quality of high-value tea and provide full traceability

  @US-017-01 @Tea @Flush
  Scenario: Seasonal flush and altitude fingerprint tracking
    Given a tea harvest event
    When the system records the flush type (e.g. Pre-Qingming, Pre-Rain)
    Then the harvest lot must automatically inherit the parcel's altitude and slope fingerprints
    And the "Tea Season" must be recorded as a core quality dimension

  @US-017-02 @Recipe @Processing
  Scenario: Tea processing recipe modeling
    Given a tea master defining a recipe for Green or Oolong tea
    When processing parameters like "fermentation duration" or "rolling pressure" are set
    Then the "farm.tea.recipe" proxy must validate these against the BoM standards
    And provide target moisture levels for each stage

  @US-017-03 @Traceability @DualLanguage
  Scenario: Multi-stage traceability from fresh leaf to finished tea
    Given a consumer scanning a finished tea package
    When the portal displays the traceability info
    Then it must show the full chain from the specific tea garden to the final processing artist
    And include biochemical indices linked via "AgriTraceabilityMixin"
    And support full "Dual-language" display
