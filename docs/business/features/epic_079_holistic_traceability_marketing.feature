Feature: Epic 079 Holistic Traceability Marketing
  As a Consumer or Brand Manager
  I want interactive traceability portals and terroir profiling
  So that I can trust the product brand and understand its environmental impact

  @US-079-01 @PWA @Traceability
  Scenario: Interactive traceability portal with full lifecycle timeline
    Given I am a consumer scanning a product QR code
    When the traceability portal loads (must be < 2.5s)
    Then it must display a dynamic timeline of the product's journey from seed to harvest
    And provide bilingual scientific explanations for indicators like NPK and GDD

  @US-079-02 @GIS @Terroir
  Scenario: Terroir integration and historical year comparison
    Given a traceability page for a specific harvest lot
    When I view the "Terroir" section
    Then it must automatically display the parcel's altitude, slope, and soil minerals
    And compare the current season's weather (light, rain) against historical "Golden Years"

  @US-079-03 @Multimedia @Evidence
  Scenario: Mounting real-world imagery and video to traceability nodes
    Given a consumer viewing the product timeline
    When they click on a "Harvest" or "Packing" node
    Then the portal must automatically load and play associated field photos or short videos (< 10s)
    And support links to live stream replays if available for that specific time

  @US-079-04 @ESG @Carbon
  Scenario: Low-carbon certificate visualization and contribution
    Given a product lot produced via VRA precision methods (Epic 076)
    When I view the sustainability section of the portal
    Then it must display the "Avoided Emissions" compared to traditional methods
    And allow me to download a PDF "Low-carbon Certificate" with a blockchain hash
