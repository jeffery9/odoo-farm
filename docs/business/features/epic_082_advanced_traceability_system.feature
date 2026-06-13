Feature: Epic 082 Advanced Traceability System
  As a Quality Specialist or Compliance Manager
  I want end-to-end batch tracking and global standards compliance
  So that I can ensure food safety and respond to product recalls in real-time

  @US-082-01 @Traceability @Chain
  Scenario: End-to-end batch genealogy and reverse tracking
    Given a finished product lot
    When I trigger a reverse traceability scan
    Then the system must display the full inheritance chain (Seed -> Harvest -> Processing -> Sale)
    And allow me to drill down from the final product back to the original farm parcel

  @US-082-02 @Compliance @Recall
  Scenario: Global traceability standards compliance and mock recall
    Given a "Mock Recall" dashboard
    When the compliance manager initiates a recall simulation for a contaminated batch
    Then the system must automatically aggregate the supplier lots, production records, and affected customer lists within 2 hours
    And generate a report that meets international export audit standards

  @US-082-03 @Logic @Blending
  Scenario: Proportional batch blending and weighted attribute inheritance
    Given multiple source batches combined into a single processing vessel
    When the system records the blending operation
    Then it must automatically calculate the weight percentage of each source batch
    And the final batch must inherit "Terroir" attributes based on the weighted proportions
