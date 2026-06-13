Feature: Epic 065 Intensive Livestock
  As a Safety Officer or Farm Manager
  I want biometric access control, real-time environment-linked ventilation, and FCR monitoring
  So that I can ensure biosafety, animal welfare, and optimal feed conversion in intensive farming

  @US-065-01 @Biosafety @IOT
  Scenario: Biometric electronic pass and disinfection lock
    Given a high-density livestock facility
    When a person attempts to enter a building
    Then the system must record their identity and disinfection status
    And only send an "Unlock" command via the IoT bridge if the disinfection time meets the standard

  @US-065-02 @IOT @Environment
  Scenario: Stocking density alerts and automated ventilation
    Given a livestock building with real-time CO2 and ammonia monitoring
    When the gas concentration exceeds the safety threshold
    Then the system must automatically trigger a ventilation command
    And create an "Environmental Anomaly Check" Activity for the technician

  @US-065-03 @FCR @Alerts
  Scenario: Real-time FCR monitoring and health check assignment
    Given a livestock lot with recorded daily feed intake and estimated growth
    When the system calculates the Feed Conversion Ratio (FCR)
    Then it must display the FCR trend on the dashboard
    And if the FCR is abnormally high (e.g. > 3.0), automatically assign a "Health Inspection" task to the veterinarian

  @US-065-04 @Welfare @Compliance
  Scenario: Animal welfare monitoring and bilingual auditing
    Given environment sensors measuring light intensity and activity space
    When the system analyzes the data for animal welfare compliance
    Then it must verify if the "Average Daily Light Duration" standard is met
    And support exporting a bilingual "Animal Welfare Audit Report"
