Feature: Epic 137 Granular Carbon Allocation
  As a Financial Controller or ESG Director
  I want precise energy cost and Scope 2 carbon footprint allocation per workorder
  So that I can accurately calculate product margins and provide verifiable carbon labels

  @US-137-01 @IOT @Energy
  Scenario: Workorder direct integration with IoT smart meters
    Given a high-energy workcenter (e.g. drying machine) bound to an IoT smart meter
    When a workorder is completed on this workcenter
    Then the system must query the IoT gateway for the exact electricity consumption (kWh) during the operation
    And record this value directly on the workorder log

  @US-137-02 @Finance @Costing
  Scenario: Granular landed cost calculation for manufacturing energy
    Given a recorded electricity consumption for a completed workorder
    When the system updates the inventory valuation
    Then it must automatically generate a "stock.valuation.layer" for the specific product batch
    And accurately apply the financial cost based on the configured industrial electricity rate

  @US-137-03 @ESG @Carbon
  Scenario: Lot-level Scope 2 carbon footprint calculation and display
    Given a completed workorder with recorded energy consumption
    When the "agri.carbon.ledger" processes the data
    Then it must calculate the Scope 2 carbon emissions using the local grid's emission factor
    And permanently link this emission record to the final product lot
    And clearly display the carbon footprint on the consumer-facing digital passport
