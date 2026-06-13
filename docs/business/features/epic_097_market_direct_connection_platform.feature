Feature: Epic 097 Market Direct Connection Platform
  As a Sales Director or Channel Buyer
  I want real-time demand matching and production transparency
  So that I can reduce market information asymmetry and drive orders based on real-time yields

  @US-097-01 @Sales @Matching
  Scenario: Global market demand matching with WIP lots
    Given a list of buyer demands for specific varieties and quality grades
    When the sales manager runs the matching engine
    Then it must automatically screen and link matching in-production (WIP) lots
    And provide an estimated availability date based on the growth twin

  @US-097-03 @Branding @Compliance
  Scenario: Premium brand integration for high-compliance lots
    Given a harvest lot with an integrity score > 90
    When the lot passes all compliance audits
    Then the system must automatically tag it as "Premium Brand Ready"
    And enable premium pricing rights in the retail interface

  @US-097-04 @C2M @Feedback
  Scenario: C2M feedback loop via traceability PWA
    Given a consumer scanning a product QR code
    When they provide feedback on flavor or quality via the portal
    Then the system must aggregate this data into the "Consumer Preference Dashboard"
    And provide the producer with direct feedback to optimize future growth models
