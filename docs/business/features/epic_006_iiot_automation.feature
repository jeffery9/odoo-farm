Feature: Epic 006 IIOT & Automation
  As a Technician or Farm Owner
  I want real-time monitoring and automated control of farm equipment
  So that I can ensure optimal environmental conditions and rapid response to anomalies

  @US-006-01 @MQTT @Monitoring
  Scenario: Real-time environmental telemetry with multi-tenant isolation
    Given I am a technician
    And the system is connected to sensors via MQTT
    When telemetry data is sent to a topic prefixed with "company_id"
    Then the data must be updated in the system with < 10 minutes latency
    And the data must be isolated from other companies

  @US-006-02 @Alerts @PWA
  Scenario: Threshold alerts and PWA notifications
    Given I have configured an environmental threshold for dissolved oxygen
    When the oxygen level drops below the threshold
    Then the system must send a Web Push notification to the PWA within 1 minute
    And a high-priority "Check Environment" Activity must be created automatically

  @US-006-04 @IFTTT @Automation
  Scenario: Autonomous closed-loop control (IFTTT)
    Given I have a rule: "If Oxygen < 4mg/L Then Turn On Aerator"
    When the sensor reports 3.5mg/L
    Then the aerator must be activated automatically
    And if the value does not improve within 5 minutes, an "Escalation" Activity must be created

  @US-006-06 @Security @FourEyes
  Scenario: High-risk command "Four-Eyes" confirmation
    Given a high-risk equipment command is initiated
    When the command is sent for execution
    Then the system must hang the command and push a "Verification Needed" Activity to the supervisor
    And the command must only execute after both the initiator and supervisor provide digital signatures
