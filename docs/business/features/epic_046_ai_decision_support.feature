Feature: Epic 046 AI Decision Support
  As a Production Manager or Sales Manager
  I want an AI advisor to provide recovery suggestions and yield predictions
  So that I can proactively manage farm production and market commitments

  @US-046-01 @AI @Recovery
  Scenario: Stress-driven active recovery decisions
    Given a biological stress index is monitored for a production order
    When the daily stress increment exceeds the threshold
    Then the "ai.decision.engine" must automatically generate a "Recovery Task"
    And the task must include specific remedial measures (e.g. adjust irrigation)

  @US-046-02 @AI @Prediction
  Scenario: Dynamic harvest window prediction based on stress
    Given an ongoing production cycle with cumulative stress data
    When the system calculates the "Expected Harvest Date"
    Then it must account for physiological delays caused by the recorded stress
    And automatically sync the predicted date to the "farm_marketing" module

  @US-046-03 @AI @Audit
  Scenario: Decision audit and human-in-the-loop closure
    Given an AI-generated decision or suggestion
    When the decision is presented to the manager
    Then it must be associated with the "agri.intervention.basis"
    And the manager must be able to "Accept" or "Reject" the suggestion with feedback to the AI model
