Feature: Epic 041 China Compliance & Policy Adaptation
  As a Farm Owner or Quality Specialist in China
  I want to manage land contracts, pesticide real-name systems, and edible product certificates
  So that I can ensure compliance with Chinese agricultural regulations and apply for subsidies

  @US-041-02 @Compliance @Pesticide
  Scenario: Pesticide and veterinary drug real-name regulatory integration
    Given a purchase of high-toxicity pesticide
    When I record the transaction in the system
    Then I must provide a real-name identification for the buyer
    And the system should generate a compliance report for the agricultural regulatory department

  @US-041-03 @Quality @Certificate
  Scenario: Edible agricultural product certificate management
    Given a batch of produce ready for shipment
    When the quality specialist generates an "Edible Agricultural Product Certificate"
    Then the system must link the certificate to the lot's traceability information
    And support digital verification via QR code

  @US-041-04 @Subsidy @Finance
  Scenario: Agricultural subsidy application and fund management
    Given a list of available government subsidy programs
    When the financial specialist triggers a "Subsidy Application"
    Then the system must automatically pre-fill the application using verified farm data (e.g. parcel area, harvest volume)
    And track the status of the application and the received funds separately

  @US-041-06 @ESG @Reduction
  Scenario: Fertilizer and pesticide reduction monitoring
    Given a target for reducing chemical fertilizer usage by 10%
    When the system analyzes the intervention logs for the production season
    Then it must calculate the actual reduction achieved
    And generate a performance report comparing usage against the target
