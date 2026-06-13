Feature: Epic 075 Agricultural Knowledge Management
  As an Agricultural Technician or Knowledge Manager
  I want a structured knowledge base and AI-driven farming recommendations
  So that I can preserve expert experience and provide scientific guidance to farmers

  @US-075-01 @Knowledge @Base
  Scenario: Structured agricultural knowledge base construction
    Given I am a knowledge manager
    When I aggregate scientific literature and expert experience into the system
    Then the system must organize the content in a structured format with tags and indexing
    And support continuous updates and versioning of the knowledge assets

  @US-075-02 @AI @Recommendation
  Scenario: Context-aware AI farming recommendations
    Given a farmer managing a specific crop variety at a certain growth stage
    When the system analyzes the current environment and historical practices
    Then it must provide expert-level, actionable recommendations for the next农事 (agricultural) steps
    And include specific details for each suggested intervention

  @US-075-03 @AI @QA
  Scenario: Multi-lingual agricultural Q&A via natural language
    Given I have a technical question regarding a plant disease
    When I ask the question in natural language (e.g. Mandarin or English)
    Then the AI-driven Q&A system must provide an accurate and reliable response based on the knowledge base
    And provide links to relevant source documents or expert cases
