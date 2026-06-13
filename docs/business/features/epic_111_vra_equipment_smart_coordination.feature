Feature: Epic 111 VRA Equipment Smart Coordination
  As a Fleet Manager or Dispatcher
  I want multi-machine coordinated scheduling and collision prevention
  So that I can optimize VRA machine utilization and ensure safe field operations

  @US-111-01 @Fleet @Scheduling
  Scenario: Multi-machine coordinated VRA mission scheduling
    Given a list of pending VRA prescriptions for multiple parcels
    When the fleet manager triggers the "Multi-Agent Coordination"
    Then the system must optimize the task allocation across the machine pool
    And provide an integrated path plan that minimizes ferry time between fields

  @US-111-02 @Security @Collision
  Scenario: Automated machinery operation conflict prevention
    Given multiple VRA machines operating in the same or adjacent parcels
    When the system monitors their real-time GPS locations via IIoT
    Then it must automatically detect potential path overlaps or proximity violations
    And trigger a "Proximity Stop" command or path adjustment via the A2A protocol (Epic 092)

  @US-111-03 @Logistics @Optimization
  Scenario: Smart refueling and input replenishment scheduling
    Given a long-running VRA mission
    When the system predicts fuel or pesticide exhaustion based on real-time consumption
    Then it must automatically generate a "Replenishment Task" at the optimal time
    And suggest the most efficient rendezvous point for the service vehicle
