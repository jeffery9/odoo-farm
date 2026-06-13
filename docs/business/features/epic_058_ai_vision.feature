Feature: Epic 058 AI Vision
  As a Farm Worker or Manager
  I want computer vision for disease diagnosis and yield prediction
  So that I can detect issues early and optimize production based on AI insights

  @US-058-01 @AI @Diagnosis
  Scenario: AI-based pest and disease diagnosis from photos
    Given I am a worker in the field
    When I take a photo of a suspicious leaf
    Then the AI model should identify the pest or disease with a confidence score
    And automatically generate a draft intervention task (Epic 002)

  @US-058-02 @AI @Yield
  Scenario: Dynamic yield prediction model based on growth progress
    Given a production season with recorded GDD and historical data
    When the system runs the yield prediction model
    Then it must provide an estimated total harvest weight
    And trigger dynamic alerts for the optimal "Harvest Window"

  @US-058-03 @EdgeAI @PWA
  Scenario: Offline edge AI disease identification on mobile
    Given I am in a remote area with no network signal
    When I use the PWA's integrated TensorFlow.js model to scan a leaf
    Then the system must perform a sub-second inference locally
    And generate a geo-watermarked offline evidence record for later sync
