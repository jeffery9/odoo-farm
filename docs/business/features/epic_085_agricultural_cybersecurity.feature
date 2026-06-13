Feature: Epic 085 Agricultural Cybersecurity
  As an IT Admin or Safety Manager
  I want layered network security and IoT device authentication
  So that I can protect farm data privacy and prevent unauthorized access to physical systems

  @US-085-02 @Compliance @GDPR
  Scenario: Data privacy classification and compliance (GDPR)
    Given I am a compliance officer
    When I classify farm data (e.g. employee records, soil data)
    Then the system must implement encryption and access markers based on the classification
    And support defined data retention periods according to privacy regulations

  @US-085-03 @Security @IOT
  Scenario: IoT device authentication and firmware management
    Given a new IoT sensor being connected to the farm network
    When I register the device
    Then the system must record its unique physical UID/MAC for authentication
    And it must track the firmware version and verify that TLS encryption is active for communication
