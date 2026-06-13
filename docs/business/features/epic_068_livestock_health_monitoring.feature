Feature: Epic 068 Livestock Health Monitoring
  As a Livestock Manager or Veterinarian
  I want real-time health monitoring and automated disease risk alerts
  So that I can improve animal welfare, reduce mortality, and optimize production efficiency

  @US-068-01 @Health @Monitoring
  Scenario: Real-time vital signs monitoring and behavioral analysis
    Given a livestock unit equipped with wearable health sensors
    When sensors report body temperature, heart rate, and movement patterns
    Then the system must analyze these parameters against the breed's baseline
    And trigger an "Early Warning" alert if symptoms of fever or inactivity are detected

  @US-068-02 @Feeding @Smart
  Scenario: Individualized smart feeding management based on health status
    Given a livestock lot with individual IDs
    When the system receives health data suggesting a nutrient deficiency
    Then it must automatically adjust the individual's feeding plan via the IoT feeder
    And track the nutritional intake compared to the predicted growth curve

  @US-068-03 @Disease @Prevention
  Scenario: Disease prevention and treatment tracking for livestock
    Given a veterinarian recording a medical intervention
    When the treatment is applied to a specific lot
    Then the system must track the recovery progress and update the "Withdrawal Period" (Epic 018)
    And if a potential outbreak is identified, automatically create a "Biosafety Alert" (Epic 031)
