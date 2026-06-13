Feature: Epic 044 Precision Production Foundation
  As a Production Operator or Quality Supervisor
  I want an ISA-88 compliant execution engine with parameter-driven control
  So that I can achieve high precision in irreversible production processes

  @US-044-01 @Logic @DriveMode
  Scenario: Switch between material-driven and parameter-driven modes
    Given a manufacturing order (MO)
    When I switch the drive mode to "parameter"
    Then the system must hide the standard BoM lines
    And display the "Cockpit" interface with parameter configurations and phase panels

  @US-044-03 @Phase @Inventory
  Scenario: Phase autonomy and atomic inventory transaction
    Given a production phase within an MO
    When I click the "Complete" button for the phase
    Then the system must immediately deduct the raw materials consumed in that phase
    And independent timers for the phase must be stopped

  @US-044-04 @SPC @Hold
  Scenario: Process control (SPC) and execution hold on critical deviation
    Given an MO in the "In Progress" state
    When a quality measurement is recorded as "Out of Control"
    Then the MO status must automatically change to "Hold"
    And all execution buttons must be disabled until a supervisor approves the release

  @US-044-08 @IOT @DataCapture
  Scenario: IIoT integration and automated sensor data capture
    Given an MO linked to "iiot.device" and "iiot.sensor"
    When sensors report data through the IoT bridge
    Then the "iiot.reading" model must automatically store the measurements
    And the system must check for deviations against the target setpoints in real-time
