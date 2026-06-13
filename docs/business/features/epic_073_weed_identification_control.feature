Feature: Epic 073 Weed Identification & Control
  As an Agronomist or Environmental Specialist
  I want AI-driven weed recognition and precision removal
  So that I can reduce herbicide usage and protect the environment

  @US-073-01 @AI @Weeds
  Scenario: AI-driven weed species recognition and density mapping
    Given I am using the "farm_ai_vision" system in a field
    When the system processes images of the parcel
    Then it must accurately identify common weed species and their growth stages
    And generate a "Weed Density Map" for the parcel to optimize removal timing

  @US-073-02 @PrecisionAg @Weeding
  Scenario: Precision weeding operations and targeted application
    Given a weed density map for a specific parcel
    When a precision weeding operation is executed (manual or mechanical)
    Then the system must track the location of the cleared weeds
    And record the reduction in herbicide usage compared to broadcast spraying

  @US-073-04 @Resistance @PlantProtection
  Scenario: Herbicide resistance monitoring and adaptive treatment
    Given a history of herbicide applications for a specific parcel
    When a weed species shows signs of resistance
    Then the system must alert the plant protection specialist
    And recommend alternative non-chemical weeding methods based on the resistance level
