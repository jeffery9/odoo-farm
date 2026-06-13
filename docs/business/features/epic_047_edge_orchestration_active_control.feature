Feature: Epic 047 Edge Orchestration & Active Control
  As an Automation Engineer or Process Technologist
  I want bi-directional synchronization between Odoo recipes and MQTT actuators
  So that I can execute production commands on physical devices with low latency

  @US-047-01 @MQTT @Actuator
  Scenario: Define actuator endpoints and MQTT mapping
    Given I am an automation engineer
    When I configure a "iot.device.mapping" for an outbound command
    Then I must be able to specify the MQTT topic and the JSON payload template (e.g. {'setpoint': {{value}} })
    And the mapping should be stored in the "farm_iot" management center

  @US-047-02 @Recipe @Setpoint
  Scenario: Bi-directional setpoint binding and command dispatch
    Given an active "Control Recipe" in Odoo
    When I modify a target value for a process parameter
    Then the system must automatically dispatch an MQTT instruction via the "agri_iot" framework
    And record a Level 2 traceability entry in the "iiot.command.log"

  @US-047-03 @Audit @Traceability
  Scenario: Edge autonomy and command feedback audit
    Given a dispatched control command to an actuator
    When the system tracks the command status
    Then it must record the lifecycle transitions: Dispatched -> ACK -> Success or Failed
    And the audit log must be linked to the specific MO and Phase
