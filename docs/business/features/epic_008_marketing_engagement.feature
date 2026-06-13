Feature: Epic 008 Marketing & Engagement
  As a Marketing Manager or Consumer
  I want to see the traceability story of my products and manage subscriptions
  So that I can trust the brand and enjoy fresh farm produce regularly

  @US-008-01 @Traceability @Branding
  Scenario: Farm-to-Table traceability portal with IoT data
    Given I am a consumer scanning a traceability QR code
    And the portal is in "Dual-language" mode
    When I view the traceability page
    Then I should see the dynamic environmental curves from IoT history
    And a "Live Stream" button must be available to view the parcel's video feed

  @US-008-02 @Sales @CSA
  Scenario: Community Supported Agriculture (CSA) subscription management
    Given I am a farm owner offering vegetable box subscriptions
    When a customer subscribes to a weekly delivery
    Then the system must automatically generate "stock.picking" orders according to the frequency
    And it should aggregate harvest forecasts based on the subscription volume

  @US-008-05 @Certification @Organic
  Scenario: International organic certification verification
    Given I am an international consumer
    When I scan the product QR code to verify organic integrity
    Then the system must query the Ecocert API or equivalent international agency
    And it must display the certificate validity, scope, and bilingual agency details
