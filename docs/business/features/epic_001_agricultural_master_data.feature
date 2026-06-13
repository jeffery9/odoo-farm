Feature: Epic 001 Agricultural Master Data
  As a Farm Owner or Technician
  I want to define core agricultural data structures
  So that I can support multi-industry operations and precise tracking

  @US-001-01 @Core
  Scenario: Multi-format activity classification
    Given I am a farm manager
    And the system supports "Planting", "Livestock", and "Aquaculture" activity families
    When I create a new project of family "Planting"
    Then the project should have a sequence starting with "P"
    And the UI should display specific properties for "Planting"
    And if I create a new project of family "Livestock"
    Then the project should have a sequence starting with "L"

  @US-001-03 @GIS
  Scenario: Parcel GIS digitization
    Given I want to define a new parcel
    When I create a location inherited from "stock.location"
    And I provide GeoJSON coordinates for the parcel boundary
    And I record the initial soil N/P/K levels
    Then the parcel should be visible on the GIS map layer
    And the system should store the historical soil analysis trends

  @US-001-04 @BiologicalAsset
  Scenario: Biological Asset Pedigree tracking
    Given a biological asset group managed as "stock.lot"
    When I register a new offspring asset
    And I link its "father_id" and "mother_id"
    Then I should be able to perform a recursive pedigree query
    And the change must be recorded in the "mail.tracking.value" audit log

  @US-001-05 @Compliance
  Scenario: Generation tracking (G0-G3) and sales blocking
    Given a product with breeding generation "G1"
    And a sales order is created for this product
    When the sales order is confirmed
    Then the system must validate the "agri_generation" of all lines
    And if it is a non-commercial generation, the sale must be blocked with a ValidationError
    And an exception review Activity must be created for the "Compliance Manager"
