Feature: Epic 126 Germplasm Genetic Bank
  As a Lab Technician or Compliance Officer
  I want ultra-low temperature storage management and genetic material rights tracking
  So that I can secure valuable genetic assets and ensure legal compliance during breeding

  @US-126-01 @Inventory @Storage
  Scenario: Ultra-low temperature sample storage management
    Given a biological sample requiring cryogenic storage
    When the lab technician assigns a storage location
    Then the system must support a 4-level deep location hierarchy (Tank -> Rack -> Box -> Position) via "stock.location"
    And automatically trigger a "Capacity Warning" Activity if the tank's remaining capacity falls below 10%

  @US-126-02 @Compliance @IP
  Scenario: Genetic material rights and authorization management
    Given a germplasm sample with associated intellectual property rights
    When the sample is requested for a breeding task (Epic 020)
    Then the system must verify the validity of the authorization contract
    And block the usage if the rights have expired or are invalid
    And maintain a bilingual (Dual-language) audit log of all ownership changes and access requests
