Feature: Epic 062 Brand Organic Integrity
  As a Brand Manager or External Auditor
  I want terroir profiling and integrity scoring for organic products
  So that I can maximize product value and provide transparency to consumers and regulators

  @US-062-01 @Traceability @Terroir
  Scenario: Terroir profiling and bilingual reporting
    Given I am an agricultural technician
    When I record the microclimate, slope, and soil minerals for a parcel ("stock.location")
    Then the system must support exporting a bilingual "Terroir Report" for the parcel
    And these attributes must be visible in the consumer-facing brand story

  @US-062-02 @Security @GI
  Scenario: Geographical Indication (GI) anti-counterfeiting integration
    Given a batch of high-value GI protected produce
    When the system generates shipping labels
    Then it must automatically call the GI anti-counterfeiting API to retrieve a unique sequence number
    And print the anti-counterfeit code on the outbound label

  @US-062-04 @Organic @Audit
  Scenario: Real-time organic integrity scoring for farm parcels
    Given an organic parcel with ongoing production
    When the "Integrity Scoring Engine" runs
    Then it must calculate the score: Compliance Rate * 0.4 + Input White-list Rate * 0.4 + QC Pass Rate * 0.2
    And if the score drops below 60, automatically send a "Downgrade Warning" to the quality manager

  @US-062-06 @Portal @Transparency
  Scenario: Remote "Transparency Portal" for third-party auditors
    Given an external organic certification auditor
    When they log into the "Auditor Portal"
    Then they must only see a read-only, de-sensitized "Compliance Ledger"
    And be able to export a "One-click Audit Bundle" for a specific certification cycle
