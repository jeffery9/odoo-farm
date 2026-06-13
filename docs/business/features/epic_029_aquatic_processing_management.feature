Feature: Epic 029 Aquatic Product Processing
  As a Processing Manager or Compliance Officer
  I want to track catch intake, glazing rates, and flash-freezing parameters
  So that I can ensure food safety, weight integrity, and export compliance

  @US-029-01 @Traceability @DNA
  Scenario: Fresh catch intake and aquaculture DNA inheritance
    Given a batch of aquatic products is received for processing
    When the lot is created and linked to the source "farm.lot.aquaculture" batch
    Then it must inherit the water environment history and temperature fingerprints
    And the link must be stored in the "AgriTraceabilityMixin"

  @US-029-02 @Math @Yield
  Scenario: Glazing rate verification and weight integrity audit
    Given a processing order for frozen aquatic products
    When the operator records the "Net Weight" and "Frozen Weight"
    Then the system must calculate the "Glazing Rate" automatically
    And generate a "Glazing Compliance Certificate" as part of the lot's quality fingerprint

  @US-029-03 @IOT @ColdChain
  Scenario: Flash-freezing core temperature monitoring and quality gate
    Given a flash-freezing machine with IoT sensors
    When the sensors record the core temperature curve of a batch
    Then the system must verify that the temperature reaches -18C within the specified time
    And the "AgriQualityGateMixin" must block inventory entry if the curve is non-compliant

  @US-029-04 @Compliance @Export
  Scenario: Microbial index and export compliance verification
    Given a finished aquatic product batch ready for export
    When the compliance officer triggers an export verification
    Then the system must query the "farm.export.compliance" database for the target market (e.g. EU/US)
    And verify that histamine and heavy metal test records are within the permitted limits
