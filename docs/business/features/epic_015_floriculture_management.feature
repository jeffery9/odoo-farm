Feature: Epic 015 Floriculture Management
  As a Horticulturist or Production Supervisor
  I want to control flower growth and bloom stages via environmental intervention
  So that I can maximize flower quality, predict bloom dates, and ensure cold-chain integrity

  @US-015-01 @Horticulture @DIF
  Scenario: DIF-driven bloom control recipe
    Given I am a horticulturist configuring a flower recipe
    When I specify the target "Day Temperature" and "Night Temperature"
    Then the system must calculate the DIF (Day - Night)
    And it should apply positive or negative DIF effects on stem length and bloom timing

  @US-015-02 @GDD @Prediction
  Scenario: Dynamic GDD-based physiological stage migration
    Given a flower batch inheriting "AgriGrowthCycleMixin"
    When the system aggregates the cumulative GDD
    Then it should update the "stage_progress" automatically
    And when progress reaches 100%, it must migrate the lot to the next physiological stage

  @US-015-03 @Quality @ShelfLife
  Scenario: Smart vase-life prediction and quality gate
    Given a flower lot at harvest
    When the system calculates "predicted_vase_life" based on bloom stage and initial cold-core temperature
    Then the result must be embedded in the lot's digital fingerprint
    And if the predicted life is below 3 days, the "AgriQualityGateMixin" must block the lot from entering inventory

  @US-015-04 @IOT @ColdChain
  Scenario: IoT-triggered cold-chain redline interception
    Given a flower batch in transport with IoT monitoring
    When the current temperature exceeds the "max_transport_temp"
    Then the system must automatically flag the batch with a "temperature_violation"
    And freeze the lot status and create a high-priority alert task
