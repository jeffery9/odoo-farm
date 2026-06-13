Feature: Epic 040 Advanced Industry & Compliance
  As a Fleet Manager or Compliance Officer
  I want to manage farm machinery, subsidies, and export compliance
  So that I can optimize equipment usage and meet regulatory requirements

  @US-040-01 @Maintenance @Costing
  Scenario: Farm machinery asset management and fuel cost allocation
    Given I am a fleet manager
    And the system uses "maintenance.equipment" for farm machinery
    When a worker confirms a field intervention with a specific machine
    Then the system must force the entry of start and end hours
    And automatically allocate fuel and maintenance costs to the parcel's analytic account

  @US-040-03 @Safety @Crisis
  Scenario: Emergency response and one-click crisis mode
    Given a major environmental or biological crisis is detected
    When the safety officer activates the "Crisis Mode"
    Then the system must automatically lock all stock picking operations for the affected parcels
    And provide bilingual emergency guidelines for all staff

  @US-040-06 @Compliance @Export
  Scenario: Cross-border compliance check for target countries
    Given a sales order for a specific batch of produce
    And the destination country has strict pesticide residue limits
    When I attempt to confirm the sales order
    Then the system must scan the batch history for prohibited substances in the target country
    And block the order with a red warning if a violation is found

  @US-040-10 @Weather @Alerts
  Scenario: Meteorological disaster warning and automated evaluation
    Given an integration with a third-party weather API
    When a severe weather warning (e.g. Frost, Gale) is received
    Then the system must generate a "Disaster Check" Activity for the site manager within 5 minutes
    And create a draft damage assessment report with bilingual fields
