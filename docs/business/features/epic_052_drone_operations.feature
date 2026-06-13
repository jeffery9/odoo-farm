Feature: Epic 052 Drone Operations
  As a Fleet Manager or Technician
  I want to manage drone missions, pilot licenses, and spray tracking
  So that I can optimize crop protection and provide flight-trace evidence to consumers

  @US-052-02 @HR @Compliance
  Scenario: Automated pilot license verification for drone missions
    Given I am assigning a drone spraying task
    And the system maintains a database of drone operator licenses
    When I select an operator for the task
    Then the system must automatically verify if the operator's license is valid and hasn't expired
    And block the assignment if the operator is unqualified or unlicensed

  @US-052-03 @GIS @Mission
  Scenario: Drone flight path generation and KML export
    Given I am planning a drone mission for a specific parcel
    When I trigger the "GCS Link" mission generation
    Then the system must export a KML file containing the parcel boundaries and no-fly zones
    And allow me to import the "Actual Work Area" report (JSON/CSV) from the ground station after the mission

  @US-052-04 @Inventory @Costing
  Scenario: Automated pesticide consumption and inventory deduction
    Given a completed drone spraying mission with a recorded "Actual Work Area"
    When the operator confirms the mission closure in the field
    Then the system must automatically calculate the pesticide consumption (Area * Dosage)
    And deduct the corresponding quantities from the inventory lot in real-time

  @US-052-07 @Traceability @GIS
  Scenario: Drone flight trace visualization for consumers
    Given a consumer scanning a traceability QR code for a product
    When they view the "Crop Protection" section of the story
    Then the portal must display a de-sensitized flight path thumbnail
    And show a heat-map of the spray uniformity for that specific harvest lot
