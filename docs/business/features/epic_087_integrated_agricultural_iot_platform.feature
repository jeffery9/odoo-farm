Feature: Epic 087 Integrated Agricultural IoT Platform
  As a Farm Owner or IoT Administrator
  I want multi-source sensor management and automated device control
  So that I can achieve total automation of environmental factors and reduce resource waste

  @US-087-01 @IOT @Network
  Scenario: Multi-source sensor network management and monitoring
    Given a farm with heterogeneous sensors (LoRaWAN, NB-IoT, WiFi)
    When I view the platform dashboard
    Then it must display the status and data quality of all connected devices in a standardized format
    And alert me if any device heartbeat is missed

  @US-087-02 @AI @Control
  Scenario: Automated device control and dynamic scheduling
    Given an automated irrigation or ventilation rule
    When the environment data exceeds the pre-set threshold
    Then the system must automatically execute the device control command
    And allow me to manually adjust the run-time schedule from a mobile device

  @US-087-04 @Security @IOT
  Scenario: IoT system network security and data encryption
    Given data transmission from field sensors to the server
    When the communication occurs
    Then the system must ensure the data is encrypted during transit
    And apply fine-grained access control to the device configuration APIs
