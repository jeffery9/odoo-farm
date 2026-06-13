Feature: Epic 013 Physical Synergy & Shared Infrastructure
  As a Regional Farm Cluster Manager or Coop Leader
  I want to share physical infrastructure, land, and equipment across farm boundaries
  So that I can achieve economies of scale and optimize resource utilization

  @US-013-01 @GIS @Topology
  Scenario: Cross-boundary contiguous land management
    Given multiple parcels from different companies are physically adjacent
    When I generate a work path for these parcels via PostGIS "ST_Touches"
    Then the path should eliminate redundant U-turns at the boundary
    And the operation costs must be split between companies based on "ST_Area" proportions

  @US-013-03 @Logistics @NFC
  Scenario: Physical logistics handover at designated buffer zones
    Given a designated "Handover Point" defined as a GIS circle buffer
    When two vehicles from different companies enter the buffer zone
    Then the system must trigger a "Ready for Handover" notification
    And the material transfer must be confirmed via NFC or encrypted QR code
    And inter-company PO/SO documents must be generated and confirmed automatically

  @US-013-05 @IOT @Water
  Scenario: Joint water infrastructure and conflict resolution
    Given a shared irrigation network with a "Graph Topology"
    When the water level in the source drops below 20%
    Then the A2A agents must automatically lock non-core irrigation circuits
    And prioritize water allocation to the most "urgent" crops based on the priority algorithm

  @US-013-07 @Biosafety @Security
  Scenario: Shared biosafety buffer zone and entry logic
    Given a shared vehicle disinfection center
    When a vehicle enters for disinfection
    Then the physical gate must only unlock if the spray sensors confirm a successful cycle
    And if any participating farm is marked as a "Pest/Disease Hotspot", the center must switch to "One-way Lock" mode
