Feature: Epic 086 ESG Compliance Management
  As a Sustainability Manager or Financial Director
  I want subsidy tracking, biodiversity monitoring, and export compliance
  So that I can maximize farm revenue and meet international ESG disclosure standards

  @US-086-01 @Subsidy @Finance
  Scenario: Automated agricultural subsidy tracking and verification
    Given an application for a government agricultural subsidy
    When the "farm.subsidy" module processes the claim
    Then it must automatically verify the eligibility based on linked GIS parcels
    And sync the application status with the government portal in real-time

  @US-086-02 @ESG @Biodiversity
  Scenario: Biodiversity metric monitoring and trend analysis
    Given a farm with native plant species and habitats
    When the system analyzes GIS and sensor data
    Then it must generate a "Biodiversity Metric" report for ESG disclosure
    And identify critical factors improving or deteriorating habitat quality

  @US-086-03 @Compliance @Export
  Scenario: Automated export compliance check for international markets
    Given a sales order for export to a specific market (e.g. EU)
    When I attempt to confirm the order
    Then the "farm.export.compliance" engine must verify the lot against the target market's MRL (Maximum Residue Limit) database
    And block the shipment if any compliance risk is detected

  @US-086-05 @ESG @Governance
  Scenario: ESG data governance and quality auditing
    Given a set of ESG metrics reported for the season
    When the data governance engine runs
    Then it must provide a "Data Quality Score" (0-100) based on completeness and audit trails
    And allow me to trace the data lineage back to the original sensors or interventions
