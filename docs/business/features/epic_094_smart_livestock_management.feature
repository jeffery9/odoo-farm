Feature: Epic 094 Smart Livestock Management
  As a Livestock Manager or Veterinarian
  I want individual digital logs and AI-driven health monitoring
  So that I can optimize breeding cycles, ensure animal welfare, and maximize yield performance

  @US-094-01 @Individual @Lifecycle
  Scenario: Individual animal life-log and pedigree tracking
    Given a livestock herd
    When I assign a unique RFID or ear-tag to an animal
    Then the system must create an individual digital archive
    And track critical lifecycle events (Birth, Mating, Vaccination, Slaughter) and parent-child pedigree links

  @US-094-02 @AI @Health
  Scenario: AI-driven health monitoring and behavioral risk alerts
    Given real-time video feeds and sensors monitoring a livestock pen
    When the AI agent identifies abnormal behavior or physiological changes
    Then it must automatically generate a health risk alert for the veterinarian
    And calculate a "Comfort Index" based on environmental and activity data

  @US-094-03 @Feeding @Optimization
  Scenario: Precision feeding management based on growth stage
    Given a livestock lot with a known age and weight
    When the system calculates the optimal feed intake
    Then it must automatically adjust the feeding plan and control the IoT feeders
    And track the feed conversion ratio (FCR) in real-time

  @US-094-05 @IOT @Environment
  Scenario: Automated environmental optimization for livestock welfare
    Given ammonia, temperature, and humidity sensors in a barn
    When sensors report gas concentrations above the safety threshold
    Then the system must automatically trigger ventilation and cooling equipment
    And record the activity for animal welfare compliance reporting
