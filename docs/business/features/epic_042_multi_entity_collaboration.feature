Feature: Epic 042 Multi-Entity Collaboration & Cooperative
  As a Coop Leader or IT Admin
  I want to manage multiple farm entities and aggregate financial data
  So that I can optimize resource sharing and ensure transparent settlement between members

  @US-042-01 @Structure @MultiCompany
  Scenario: Multi-farm entity relationship modeling
    Given I am a cooperative IT admin
    When I define the organizational structure via "res.company"
    Then the system must support a tree-like hierarchy (Parent/Child)
    And allow me to distinguish between "Franchise" and "Directly-owned" farms

  @US-042-03 @Resources @Scheduling
  Scenario: Cross-farm resource scheduling and settlement
    Given a production manager needs a harvester for Company A
    And a harvester is available at Company B
    When the manager assigns the harvester from Company B to a task in Company A
    Then the system must automatically generate an internal settlement entry for the rental cost
    And track the busy/free status of the machine across both companies

  @US-042-22 @Accounting @Netting
  Scenario: "Zero-Balance" netting settlement for coop members
    Given a member farm with material payables and product receivables
    When the "Netting Settlement Engine" runs
    Then it must automatically offset the payables against the receivables
    And generate a bilingual statement showing the统购 (Consolidated Purchase), 交售 (Sale Delivery), and the net balance

  @US-042-24 @Contract @Farming
  Scenario: "Company + Farmer" contract planting management
    Given a contractual agreement between an agri-enterprise and a farmer ("contract.farming.agreement")
    When the farmer commits to a specific yield and quality standard
    Then the system must track the input prepayments and the actual yield vs commitment
    And apply the pre-defined settlement mechanism (e.g. fixed price, cost-plus) at harvest
