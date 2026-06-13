Feature: Epic 112 AI Driven Predictive Maintenance
  As a Maintenance Engineer or Equipment Manager
  I want AI-driven machinery health monitoring and automated work orders
  So that I can reduce equipment downtime and optimize maintenance costs across the farm and supply chain

  @US-112-01 @AI @Maintenance
  Scenario: Farm machinery health monitoring and anomaly detection
    Given a tractor or harvester equipped with IIoT sensors
    When the system analyzes vibration, oil pressure, and fuel consumption trends
    Then the "ai.decision.engine" must identify early signs of mechanical wear
    And automatically create a "Predictive Maintenance" task before a breakdown occurs

  @US-112-02 @SupplyChain @Maintenance
  Scenario: Predictive maintenance for supply chain infrastructure
    Given critical infrastructure like cold storage units or sorting lines
    When the system identifies a performance drop in a compressor or motor
    Then it must automatically schedule a technician and reserve necessary spare parts
    And notify the supply chain planner of the potential impact on throughput

  @US-112-04 @UX @WorkOrder
  Scenario: Automated smart maintenance work order scheduling
    Given an identified maintenance need
    When the system generates a work order
    Then it must automatically prioritize the task based on the production calendar (Epic 002)
    And assign the most qualified technician based on their "SkillBase" and current location
