Feature: Epic 091 Agricultural Robotics Automation
  As a Farm Owner or Mission Operator
  I want autonomous task scheduling and robotic A2A coordination
  So that I can achieve zero-human field operations and high-trust physical evidence

  @US-091-01 @Robotics @IOT
  Scenario: Automated device integration and real-time status sync
    Given a new agricultural robot (e.g. harvesting or spraying robot)
    When I register it in "farm.robot"
    Then the system must automatically link its IIoT telemetry data
    And synchronize its battery level, position, and work status in real-time

  @US-091-02 @Mission @GeoJSON
  Scenario: Robotic mission scheduling and path execution
    Given an intervention task needing robotic execution
    When the mission operator triggers the "Mission Dispatch"
    Then the system must generate an optimal GeoJSON work path
    And the robot must automatically transition to the "In Progress" state and follow the path

  @US-091-04 @A2A @Robotics
  Scenario: Robotic neighborhood discovery and A2A negotiation
    Given multiple robots with unique "agent_id" signatures
    When a robot identifies a task in its grid vicinity via "agri.geospatial.mixin"
    Then it must be able to autonomously negotiate for the task via the "agri.a2a.protocol"
    And provide an "Energy-Aware" quote based on its remaining battery and distance

  @US-091-05 @Robotics @Evidence
  Scenario: Automated robotic evidence package and path verification
    Given a completed robotic mission
    When the system triggers "perform_evidence_audit"
    Then it must automatically package the GeoJSON trajectory as immutable evidence
    And sync the path verification into the lot's quality fingerprint
