Feature: Epic 074 Post Harvest Quality Management
  As a Quality Manager or Inventory Manager
  I want real-time quality monitoring and smart preservation control
  So that I can maintain product quality, extend shelf-life, and optimize inventory turnover

  @US-074-01 @Quality @Monitoring
  Scenario: Real-time post-harvest quality monitoring and alerts
    Given harvested products in a controlled environment
    When sensors monitor sugar content, firmness, and color
    Then the system must track the deterioration speed of the batch
    And trigger an "Urgent Preservation Alert" if quality indices deviate from the variety's standard

  @US-074-03 @ShelfLife @FIFO
  Scenario: Shelf-life prediction and optimized FIFO management
    Given a batch of produce with known storage history and environmental logs
    When the system runs the "Shelf-life Prediction Model"
    Then it must estimate the remaining days of freshness
    And enforce a FEFO (First Expired First Out) picking strategy for all sales orders

  @US-074-04 @Grading @Packaging
  Scenario: Automatic product grading and market matching
    Given a batch of produce being prepared for shipping
    When I record the final quality inspection results
    Then the system must automatically assign a quality grade (A, B, C)
    And suggest the most appropriate market channel and packaging material for that grade
