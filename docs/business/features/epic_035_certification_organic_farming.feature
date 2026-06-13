Feature: Epic 035 Certification & Organic Farming
  As a Quality Manager or Farm Owner
  I want to manage input blocklists, organic conversion periods, and certification compliance
  So that I can ensure all operations meet organic standards and pass external audits

  @US-035-01 @Organic @Blocking
  Scenario: Hard-blocking of prohibited inputs on organic parcels
    Given an "agri.input.blocklist" is maintained in the system
    When I attempt to record an intervention for an "Organic" parcel
    And I select an input from the blocklist
    Then the system must block the record from being saved
    And display a red high-priority warning

  @US-035-02 @Logic @Conversion
  Scenario: Organic conversion period management and reset
    Given a parcel in the organic conversion phase
    When a prohibited substance is applied to the parcel
    Then the conversion progress must be reset automatically
    And the "Conversion Overview" must show the new remaining days based on the last prohibited application date

  @US-035-05 @GlobalGAP @Audit
  Scenario: GlobalG.A.P. compliance self-assessment and gap analysis
    Given a "GlobalG.A.P. CPCC" knowledge base integrated into the system
    When I trigger a self-assessment for a production cycle
    Then the system must automatically identify missing evidence (e.g., missing water tests or soil analysis)
    And provide a gap analysis report for the quality manager

  @US-035-09 @Security @Audit
  Scenario: Parallel production physical isolation audit
    Given a farm performing both Organic and Conventional production
    When a shared harvester moves from a Conventional plot to an Organic plot
    Then the system must require a "Machine Deep Cleaning" log and photo evidence
    And block the organic task until the cleaning is verified
