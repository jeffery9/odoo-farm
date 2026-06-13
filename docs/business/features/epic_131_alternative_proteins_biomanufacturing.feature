Feature: Epic 131 Alternative Proteins & Bio-conversion
  As a Bio-factory Manager or Formulation Specialist
  I want precise lifecycle tracking and dynamic waste formulation
  So that I can optimize the industrial-scale bio-conversion of waste into alternative proteins

  @US-131-01 @BioConversion @Lifecycle
  Scenario: Black Soldier Fly (BSF) full lifecycle and microclimate management
    Given a BSF breeding facility with IoT integration
    When a batch transitions through lifecycle stages (Egg -> Larva -> Pre-pupa -> Adult)
    Then the system must support stage-specific item codes and automatic inventory transfers
    And enforce phase-specific microclimate curves (Temp/Humidity/CO2) via the IoT module
    And trigger an alert if AI-vision estimates a survival rate below the defined threshold

  @US-131-02 @Recipe @Dynamic
  Scenario: Dynamic organic waste formulation and FCR calculation
    Given a batch of agricultural waste or food scraps with known moisture and nutrient content
    When the feed formulator prepares a substrate recipe
    Then the system must dynamically calculate the required dry additives (e.g. wheat bran) to achieve target moisture
    And strictly isolate human-food grade production from restricted waste inputs
    And upon completion, automatically calculate the Feed Conversion Ratio (FCR) (Input Dry Weight vs Larva Dry Weight)

  @US-131-03 @PBR @Microalgae
  Scenario: Microalgae photobioreactor (PBR) continuous cultivation control
    Given a continuous-flow microalgae PBR system
    When the IoT probes detect a pH deviation
    Then the system must automatically trigger a solenoid valve (e.g. CO2 injection) and log the machine intervention
    And support continuous MRP flow to record daily harvesting without closing the production order
    And utilize the Specific Growth Rate model to predict the next day's harvest volume

  @US-131-04 @Extraction @Traceability
  Scenario: Alternative protein deep processing and multi-product extraction
    Given a processing order to extract protein and oil from BSF larvae or microalgae
    When the extraction process is finalized
    Then the system must handle complex co-products (e.g. 100kg Larvae = 30kg Oil + 65kg Protein Meal + 5kg Loss)
    And ensure the final products trace back to the exact waste batch originally consumed
    And enforce a mandatory Quality Gate (e.g. heavy metals, pathogens) before sales authorization
