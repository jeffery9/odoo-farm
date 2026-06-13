Feature: Epic 005 Agritourism & Experience
  As a Tourist or Farm Admin
  I want to manage bookings, picking activities, and resources
  So that I can enjoy farm-to-service experiences seamlessly

  @US-005-01 @Portal @Booking
  Scenario: Picking garden activity booking and check-in
    Given I am a tourist on the farm portal
    And the portal is in "Dual-language" mode
    When I book a picking activity
    Then the system should generate a QR code for check-in
    And when the QR code is scanned, the "action_checkin" must be triggered successfully

  @US-005-02 @Sales @Inventory
  Scenario: "Pick-to-Sale" integration
    Given I am a farm owner
    And a sales order is created for a picking activity
    When the sales order is confirmed and a lot/parcel is specified
    Then the system must automatically reserve the stock via "stock.move.line"

  @US-005-03 @Resources @Scheduling
  Scenario: Resource capacity and conflict management
    Given I am managing fishing spots or BBQ areas
    When I view the enhanced "Calendar View"
    And I attempt to book a resource that is already at full capacity
    Then the system must block the booking with a "Capacity Check" alert
    And it must prevent any scheduling conflicts

  @US-005-05 @MultiCompany @Tours
  Scenario: Integrated multi-farm community tour booking
    Given a tour spans across multiple farm companies
    When a tourist books the tour
    Then the system must automatically trigger resource confirmation across companies (e.g. A for picking, B for lunch)
    And it should calculate the revenue sharing and settlement between entities
