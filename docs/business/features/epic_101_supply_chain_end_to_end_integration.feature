Feature: Epic 101 Supply Chain End to End Integration
  As an Operations Manager or Quality Specialist
  I want end-to-end integration from procurement to sales
  So that I can achieve total supply chain visibility and respond to anomalies in real-time

  @US-101-01 @Planning @SupplyChain
  Scenario: Production plan optimization based on supply chain status
    Given a production plan (Epic 002)
    When real-time procurement or inventory status changes
    Then the system must automatically suggest adjustments to the production schedule
    And provide an impact analysis on the final harvest date

  @US-101-02 @IOT @Monitoring
  Scenario: IoT-driven end-to-end supply chain monitoring
    Given a product batch moving through the supply chain (Procurement -> Warehouse -> Production -> Sales)
    When IoT sensors monitor critical parameters (e.g. cold-chain temperature)
    Then the system must aggregate these logs into a single "Chain Integrity View"
    And trigger alerts if any segment of the chain deviates from the quality standard

  @US-101-05 @Traceability @EndToEnd
  Scenario: End-to-end multi-stage traceability and root cause analysis
    Given a quality issue detected at the retail stage
    When I perform a "Full-Chain Trace"
    Then the system must provide a backward path through processing, production, and procurement
    And identify the specific supplier batch or field intervention responsible for the issue
