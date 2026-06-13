Feature: Epic 081 Computer Vision Analysis
  As a Technician or Workshop Supervisor
  I want AI-based disease diagnosis and automated sorting
  So that I can detect issues early and optimize product grading efficiency

  @US-081-01 @AI @Diagnosis
  Scenario: AI leaf-photo disease diagnosis and severity assessment
    Given I am a field technician
    When I take a photo of a plant leaf via the PWA
    Then the AI model must identify the disease or pest
    And provide a severity grade (Low to Critical) and the affected area percentage
    And automatically create a draft intervention task with priority suggestions

  @US-081-02 @AI @Sorting
  Scenario: Visual intelligent sorting and quality evaluation
    Given a processing line for fruits or vegetables
    When the computer vision system analyzes the product flow
    Then it must accurately classify items based on size, color, and external defects
    And the sorting speed must meet the requirements of real-time pipeline operations

  @US-081-03 @AI @Monitoring
  Scenario: Crop growth monitoring and maturity prediction via imagery
    Given periodic imagery captured from the field
    When the system analyzes the crop density and health index
    Then it must update the growth status in the digital twin
    And provide a predicted harvest date and yield estimate based on multi-factor analysis
