Feature: Epic 059 Agri Risk Insurance
  As a Sales Manager or Safety Officer
  I want to monitor market risks and weather indices for insurance
  So that I can mitigate financial losses and automate damage assessment

  @US-059-01 @Finance @Risk
  Scenario: Futures price monitoring and cost-redline alerts
    Given I am monitoring agricultural futures prices
    When the market price for my product drops below the pre-set production cost redline
    Then the system must automatically send a high-priority Red Alert Activity to the sales team

  @US-059-02 @IOT @Insurance
  Scenario: Automated weather index evidence package for insurance claims
    Given IoT sensors detect an extreme weather event (e.g. frost) in a specific parcel
    When the safety officer initiates an insurance claim
    Then the system must automatically package the weather data, geo-watermarked damage photos, and lot history into an evidence bundle
    And allow me to export the claim package in bilingual format
