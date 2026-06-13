Feature: Epic 116 Blockchain Traceability & Food Safety
  As a Quality Manager or Consumer
  I want immutable blockchain records and transparent traceability
  So that I can ensure food safety and build brand trust through verifiable data

  @US-116-01 @Blockchain @Traceability
  Scenario: Immutable recording of agricultural traceability data on blockchain
    Given critical production and logistics events occurring on the farm
    When the data is recorded in the system
    Then it must be standardized and sent to the blockchain network in real-time
    And ensure that the records are immutable and cryptographically verifiable

  @US-116-02 @Consumer @Portal
  Scenario: Consumer-facing blockchain traceability query interface
    Given a finished product with a traceability QR code
    When a consumer scans the code
    Then the system must provide a user-friendly interface displaying the full supply chain history
    And include proof of the blockchain transaction for transparency

  @US-116-03 @Safety @Alerts
  Scenario: Food safety monitoring and automated warning integration
    Given HACCP control points linked to the blockchain ledger
    When a contamination event or safety threshold violation is detected
    Then the system must quickly trace the source and affected batches
    And automatically dispatch safety alerts to relevant authorities and stakeholders

  @US-116-04 @Compliance @Audit
  Scenario: Traceability data verification and third-party auditing
    Given a regulatory audit requirement
    When the compliance manager or third-party auditor reviews the records
    Then the system must provide tools to verify the integrity and authenticity of the blockchain data
    And generate compliance reports that meet food safety regulations
