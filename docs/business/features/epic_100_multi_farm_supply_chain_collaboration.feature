Feature: Epic 100 Multi Farm Supply Chain Collaboration
  As a Cooperative Leader or Warehouse Manager
  I want joint procurement and cross-farm inventory sharing
  So that I can achieve economies of scale and optimize resource utilization within the cooperative

  @US-100-01 @Coop @Procurement
  Scenario: Joint procurement aggregation and bulk-discount negotiation
    Given multiple member farms within a cooperative
    When the system aggregates their fertilizer and seed requirements via "CollaborativeMixin"
    Then it must automatically generate a consolidated RFQ for suppliers
    And support A2A price negotiation based on the "Bulk Buff" volume

  @US-100-02 @A2A @Inventory
  Scenario: Cross-farm inventory discovery and virtual sharing
    Given a shortage of a specific pesticide at Farm A
    When the agent at Farm A publishes a "Demand Signal" via A2A
    Then it must be able to discover surplus inventory at nearby Farm B
    And facilitate a virtual inventory transfer using "AwaitedMutex" for transactional safety

  @US-100-03 @GIS @Logistics
  Scenario: Collaborative logistics handover and route splicing
    Given delivery orders from several adjacent member farms
    When the logistics engine runs the "Route-Splice" optimization
    Then it must generate a single optimal path for the shared vehicle
    And automatically manage the handover of ownership at pre-defined GIS buffer zones (Epic 013)

  @US-100-09 @F2F @互助
  Scenario: Peer-to-peer (F2F) decentralized resource sharing
    Given a farmer needing an extra harvester for a 2-day window
    When the farm agent searches the neighborhood via the A2A protocol
    Then it must match the request with a neighbor's idle machinery based on "SkillBase" attributes
    And conclude a sharing agreement via "SeaTurtleSoup" reasoning (Epic 012)
