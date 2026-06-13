Feature: Epic 016 Medicinal Plants Management
  As a Medicinal Plant Technician or Base Manager
  I want to track "Daodi" origin and active compound accumulation
  So that I can ensure pharmaceutical grade quality and compliance with GMP standards

  @US-016-01 @Spatial @Daodi
  Scenario: "Daodi" origin geographical fingerprint verification
    Given a new parcel for medicinal plants
    When the system checks the altitude and soil quality via "GeoSpatialMixin"
    Then it must automatically verify if the conditions match the "Daodi" standard for the variety
    And trigger a warning if the parcel does not meet the requirements

  @US-016-02 @Algorithm @Compounds
  Scenario: Active compound dynamic accumulation tracking
    Given a medicinal plant variety with a specific growth model
    When the system tracks the cumulative GDD
    Then it should plot the predicted accumulation curve of active compounds
    And laboratory test results must be automatically linked back to the lot DNA

  @US-016-04 @GMP @Quality
  Scenario: GMP processing and quality gate for medicinal herbs
    Given a processing order for medicinal herbs (e.g. washing, cutting, drying)
    When each stage is performed
    Then the system must verify the Quality Control Points (QCP) via "AgriQualityGateMixin"
    And block the process if temperature or humidity deviate from the GMP standard
