Feature: Epic 010 Sales & Marketing Zero Waste
  As a Sales Manager or Circular Economy Officer
  I want to maximize the value of all farm produce and by-products
  So that I can minimize waste and create additional revenue streams

  @US-010-02 @Sales @Grading
  Scenario: Graded sales and multi-channel distribution
    Given products are classified by quality (A, B, C, D)
    When a batch of grade "C" products is harvested
    Then the system should automatically suggest the "Catering/Food Service" channel
    And it should apply the corresponding dynamic pricing rule for that grade

  @US-010-05 @Circular @ValueAdded
  Scenario: By-product value-added conversion
    Given a production process that generates "co-products" like fruit peels or straw
    When the production is finished
    Then the system should evaluate the value of these by-products
    And suggest processing routes like "Pectin Extraction" or "Organic Fertilizer"
    And track the conversion into a new high-value product

  @US-010-08 @A2A @Engagement
  Scenario: Immersive bio-asset adoption via Agent-to-Agent (A2A) interaction
    Given a consumer has adopted a specific tree or animal
    When the consumer's AI Agent queries the farm's Digital Twin (Epic 093)
    Then the Farm Agent must push a growth snapshot and environmental report
    And the consumer must be able to trigger a "Special Feeding" or "Photo" task via their agent
