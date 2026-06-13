Feature: Epic 023 Essential Oil Management
  As a Production Technologist or Lab Analyst
  I want to control extraction parameters and track batch lineage
  So that I can ensure high extraction yields and provide full traceability for essential oils

  @US-023-01 @Recipe @Extraction
  Scenario: Essential oil extraction protocol modeling
    Given I am a production technologist
    And the system uses "farm.essential_oil.recipe" proxying "mrp.bom"
    When I define the distillation temperature, pressure, and cooling duration
    Then the recipe must store these parameters for production execution
    And it should calculate the "target_yield_percent"

  @US-023-02 @Audit @Yield
  Scenario: Automated extraction yield audit and alerts
    Given a production order for essential oil extraction
    When the production is completed and the output volume is recorded
    Then the system must calculate the "Actual Yield" (Output / Input)
    And if the yield is 20% below the standard value, an "AgriIncidentAlertMixin" must be triggered

  @US-023-03 @Traceability @DNA
  Scenario: Multi-to-one batch DNA lineage inheritance
    Given multiple raw material lots are consumed in an extraction process
    When the essential oil lot is generated
    Then the "AgriTraceabilityMixin" must aggregate the geographical and biochemical DNA from all raw lots
    And the final product hash must include the hash summaries of all source lots

  @US-023-04 @Quality @GCMS
  Scenario: GC-MS chemical composition analysis and quality gate
    Given a finished essential oil lot
    When I record the chemical composition (e.g., Linalool content) via "AgriQualityGateMixin"
    Then the system must verify if the components are within the standard range
    And block the final clearing if the quality standards are not met
