Feature: Epic 124 Medicinal Herbs Processing
  As a Quality Manager or Factory Supervisor
  I want GMP-compliant processing controls and authenticity (Daodi) verification
  So that I can ensure the medicinal efficacy of herbs and comply with strict TCM regulations

  @US-124-01 @Quality @Daodi
  Scenario: "Daodi" environmental factor verification and efficacy modeling
    Given a harvested batch of medicinal herbs
    When the system analyzes the IoT environmental history for the parcel (e.g. diurnal temperature difference)
    Then it must run the "Active Compound Prediction Model" to estimate the efficacy
    And automatically generate a "Terroir Verification Certificate" to prove the "Daodi" authenticity

  @US-124-02 @GMP @Processing
  Scenario: Standardized TCM processing control and formulation precision
    Given an "mrp.production" order for a TCM processing technique (e.g. vinegar baking)
    When the operator records the processing time and auxiliary materials
    Then the system must enforce strict QC points (e.g. baking duration) as mandatory inputs
    And precisely deduct the inventory of auxiliary materials (e.g. Rice Vinegar) based on the specific "mrp.bom"
    And ensure the final batch certificate includes the "Processing Specification"
