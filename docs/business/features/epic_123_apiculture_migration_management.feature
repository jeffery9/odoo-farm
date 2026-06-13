Feature: Epic 123 Apiculture Migration Management
  As a Beekeeper or Technical Expert
  I want to track bee colony lifecycles, migration paths, and hive micro-environments
  So that I can optimize honey production, prevent swarming, and ensure precise traceability

  @US-123-01 @Apiculture @Lifecycle
  Scenario: Bee colony full lifecycle tracking and queen management
    Given a bee colony managed as "stock.lot"
    When the beekeeper updates the "Queen Age" and "Selection Grade"
    Then the system must record these attributes in the lot's history
    And automatically trigger a "Queen Replacement Check" Activity if the queen's age exceeds the optimal threshold

  @US-123-02 @GIS @Migration
  Scenario: Migration path tracking and nectar source linkage
    Given a migratory beekeeper operating in a remote area
    When they record a "Temporary Apiary" via the offline PWA
    Then the system must sync the GIS coordinates upon network restoration
    And automatically link the harvested honey lots to the corresponding "Nectar Source" (e.g. Acacia, Manuka) at that location

  @US-123-03 @IOT @Environment
  Scenario: Hive internal IoT environment monitoring and theft/swarm alerts
    Given a hive equipped with MQTT weight and temperature sensors
    When the sensor detects a sudden weight drop (> 5kg) within 1 minute
    Then the system must immediately push a "Theft or Swarm Alert" to the beekeeper's mobile device
    And display an environment heat map on the apiary dashboard
