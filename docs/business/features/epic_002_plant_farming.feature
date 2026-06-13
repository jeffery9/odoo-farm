Feature: Epic 002 Plant Farming
  As a Farm Manager or Worker
  I want to manage the crop lifecycle from campaign planning to harvest
  So that I can optimize yields and track field operations accurately

  @US-002-01 @Planning
  Scenario: Production Season Campaign planning
    Given I am an agricultural technician
    When I create a new "Campaign"
    And I assign a "Variety", a "Parcel", and a "Time Window"
    Then the system should generate a unique Campaign ID
    And the Gantt view should display the scheduled tasks without conflicts

  @US-002-02 @FieldOps @PWA
  Scenario: Agricultural Intervention Recording with GPS
    Given I am a farm worker using the PWA mobile app
    And I am currently offline
    When I record a fertilization intervention
    And I specify the executor, tools, and consumption
    Then the data must be stored locally in IndexedDB
    And when the network is restored, the data must sync in FIFO order
    And the intervention must include GPS coordinates
    And if the coordinates are > 50m from the parcel boundary, it must be flagged as "Off-site operation"

  @US-002-06 @RiskManagement @Weather
  Scenario: Weather window validation for spraying operations
    Given I am about to start a "Spraying" intervention
    When I click "Start Operation"
    Then the system must fetch the 24-hour weather forecast via API
    And if the wind speed is greater than 4, the operation must be blocked
    And an "Urgent Risk Review" Activity must be created for the "Technical Director"

  @US-002-05 @IOT @Prediction
  Scenario: GDD (Growing Degree Days) yield prediction
    Given IoT temperature sensors are active in the parcel
    When the system aggregates daily "Telemetry" data (Avg Temp - Base Temp)
    Then it should calculate the Cumulative GDD
    And it should update the Predicted Harvest Date based on the crop's GDD requirement
    And the prediction error must be within the preset threshold
