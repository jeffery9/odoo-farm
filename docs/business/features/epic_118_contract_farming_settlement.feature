Feature: Epic 118 Contract Farming & Farmer Settlement
  As a Procurement or Financial Manager
  I want contract management and automated input-deduction settlement
  So that I can efficiently manage "Company + Farmer" agreements and ensure fair financial clearing

  @US-118-01 @Contract @Inventory
  Scenario: "Company + Farmer" joint contract and input distribution
    Given an active contract farming agreement with a specific farmer
    When the procurement manager distributes seeds or pesticides to the farmer
    Then the system must record the distribution via a "stock.picking" (Joint Distribution type)
    And automatically generate an "Accounts Receivable Deduction" linked to the contract
    And lock the guaranteed buyback price in the contract terms

  @US-118-02 @Accounting @Settlement
  Scenario: Automated deduction and buyback settlement calculation
    Given a farmer delivering harvested crops back to the company
    When the financial manager initiates the settlement process
    Then the system must calculate: Net Payment = (Quantity * Buyback Price) - Historical Input Costs - Service Fees
    And generate a bilingual settlement statement
    And trigger a "Settlement Anomaly" Activity if the discrepancy exceeds 5%

  @US-118-04 @Finance @Netting
  Scenario: Automated bilateral bill netting for input credit and harvest sales
    Given a farmer with an outstanding debt for inputs bought on credit
    When the farmer sells their harvest to the cooperative
    Then the "Settlement Engine" must apply a bilateral netting model
    And the generated payment voucher must clearly detail: Total Harvest Value - Input Credit - Prepayments = Net Payment
