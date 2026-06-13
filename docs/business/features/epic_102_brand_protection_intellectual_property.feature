Feature: Epic 102 Brand Protection Intellectual Property
  As a Brand Manager or Legal Officer
  I want trademark monitoring and geographical indication (GI) branding
  So that I can protect the farm's intellectual property and enhance product value through authenticity

  @US-102-01 @Legal @Trademark
  Scenario: Trademark status monitoring and renewal alerts
    Given a database of farm trademarks and patents
    When a trademark expiry date approaches (e.g. within 3 months)
    Then the system must automatically trigger a renewal Activity for the legal officer
    And maintain a digital archive of all registration certificates

  @US-102-03 @Branding @GI
  Scenario: Linking geographical indication (GI) evidence to the brand
    Given a high-value product with a "Geographical Indication"
    When the system links the lot to the parcel's GIS and soil evidence (Epic 062)
    Then it must automatically generate a "GI Authenticity Certificate" for marketing
    And display the official GI logo on the consumer traceability portal

  @US-102-04 @AI @IP
  Scenario: AI-driven brand infringement monitoring
    Given an AI vision model configured for brand logo recognition
    When the system scans online marketplaces or social media feeds
    Then it must identify potentially infringing products or look-alike brands
    And generate an "IP Violation" alert with evidence screenshots
