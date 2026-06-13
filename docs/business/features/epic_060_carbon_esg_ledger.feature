Feature: Epic 060 Carbon ESG Ledger
  As a Farm Owner or Sustainability Specialist
  I want to track carbon emissions and biodiversity credits
  So that I can meet ESG disclosure requirements and monetize environmental assets

  @US-060-01 @ESG @Carbon
  Scenario: Automated carbon footprint calculation for production lots
    Given a series of field interventions (Epic 002) with recorded input usage
    When the system calculates the carbon footprint
    Then it must automatically convert all inputs into CO2 equivalents (CO2e)
    And display the "Carbon Footprint" per KG on the finished product lot page

  @US-060-03 @Procurement @Scope3
  Scenario: Automated capture of Scope 3 embedded carbon from suppliers
    Given I am purchasing farm inputs (e.g. fertilizer)
    And the supplier has a recorded carbon emission density in "product.supplierinfo"
    When the system confirms the PO and receives the products
    Then it must automatically aggregate the Scope 3 emissions into the final product's ledger

  @US-060-05 @Livestock @Methane
  Scenario: Methane emission tracking for ruminants based on IPCC standards
    Given a livestock herd with a recorded feed recipe and weight history
    When the system analyzes the environmental impact
    Then it must calculate the enteric fermentation methane emissions using IPCC standards
    And include the results in the farm's annual ESG report

  @US-060-08 @IOT @MRV
  Scenario: Digital MRV report generation with blockchain anchoring
    Given real-time IoT monitoring data from field sensors
    When the sustainability manager generates a "Digital MRV" report
    Then the system must anchor the raw telemetry fingerprints via a blockchain hash
    And associate the report with the complete production lifecycle evidence
