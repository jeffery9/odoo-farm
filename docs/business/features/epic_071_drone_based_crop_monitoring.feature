Feature: Epic 071 Drone Based Crop Monitoring
  As a Farm Manager or Crop Protection Specialist
  I want multi-spectral monitoring and AI-driven disease recognition via drones
  So that I can detect crop stress early and execute precision field operations

  @US-071-01 @RemoteSensing @Monitoring
  Scenario: Periodic crop growth monitoring via multi-spectral imaging
    Given a scheduled drone monitoring mission
    When the drone captures multi-spectral images of the parcel
    Then the system must analyze the NDVI or equivalent indices to assess crop health
    And identify areas with growth deviations (e.g. nitrogen deficiency or water stress)

  @US-071-02 @AI @Diagnosis
  Scenario: AI-driven pest and disease recognition from drone imagery
    Given high-resolution imagery captured by a drone
    When the "farm_ai_vision" model processes the images
    Then it must automatically identify potential pest hotspots or disease outbreaks
    And trigger a "Scouting" or "Spraying" Activity (Epic 031) if the severity exceeds the threshold

  @US-071-03 @PrecisionAg @Drone
  Scenario: Precision spraying and seeding operations via drones
    Given a VRA prescription (Epic 070) or a identified pest hotspot
    When a drone-based agricultural operation is initiated
    Then the system must automatically plan the flight path for precision application
    And record the actual coverage and consumption in the production lot history (Epic 052)
