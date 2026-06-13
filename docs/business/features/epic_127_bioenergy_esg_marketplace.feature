Feature: Epic 127 BioEnergy ESG Marketplace
  As an Operations Manager or Sustainability Officer
  I want to manage waste-derived products and integrate with external ESG exchanges
  So that I can monetize agricultural waste and seamlessly trade verified carbon credits

  @US-127-01 @Sales @Energy
  Scenario: External trade of waste-derived products and energy equivalence
    Given a surplus of organic fertilizer or biogas produced from farm waste
    When the operations manager creates a sales order for the product
    Then the system must allow the product to be sold from the "Circular Output" catalog
    And automatically calculate and display the "Energy Equivalent" (e.g. Standard Coal/Electricity saved) for the transaction

  @US-127-02 @ESG @Integration
  Scenario: External ESG exchange data integration and carbon credit certification
    Given verified emission reduction data generated from farm operations (Epic 060)
    When the sustainability officer initiates an export to an external ESG exchange
    Then the system must link the "Verified Credit" record to the original operational data and third-party audit certificate
    And format the exported data payload to comply with international standards (e.g. VCS, Gold Standard)
    And retain a mandatory bilingual audit trail for the transaction
