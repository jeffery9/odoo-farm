Feature: Epic 021 Apiculture Management
  As a Beekeeper or Farm Manager
  I want to track hive strength, nectar sources, and migration paths
  So that I can maximize honey yield and ensure full-chain traceability

  @US-021-01 @Apiculture @Hive
  Scenario: Hive digital twin and queen life-log
    Given I am a beekeeper
    And the system uses "farm.lot.hive" proxying "stock.lot"
    When I record the hive strength, queen age, and breeding line
    Then the "AgriBiologicalInventoryMixin" should manage the "bee count" as biomass
    And it should maintain the queen's status machine (Good, Queenless, New Queen)

  @US-021-02 @GIS @Nectar
  Scenario: Nectar source mapping and forage radius analysis
    Given I have hives placed at a specific GIS location
    When I view the "GeoSpatialMixin" buffer analysis
    Then the system should display a 3km forage radius
    And it should analyze the coverage of nectar-producing plants within that radius

  @US-021-03 @Logistics @Migration
  Scenario: Migration planning and transhumance tracking
    Given a plan to move hives from Site A to Site B
    When the move is initiated via a "stock.picking" order
    Then the "farm.location" link must be updated automatically
    And completing the migration must trigger a "mortality record" to assess transport stress

  @US-021-04 @Quality @Traceability
  Scenario: Honey grading and physical/chemical evidence
    Given a honey harvest event
    When I record the Baumé degree, color, and nectar type via "AgriQualityGateMixin"
    Then the moisture content must be verified automatically
    And the system must generate a traceability hash including the nectar source fingerprint
