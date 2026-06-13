Feature: Epic 089 AI LLM Integration
  As an Agricultural Specialist or IT Admin
  I want LLM integration and RAG-enhanced agricultural knowledge retrieval
  So that I can receive accurate, context-aware answers to complex farming questions

  @US-089-01 @LLM @Config
  Scenario: LLM service configuration and provider management
    Given I am a system administrator
    When I configure a new LLM provider (e.g. Anthropic, Google, Ollama)
    Then the system must implement a secure "Refresh Token" or API key storage mechanism
    And support multiple model configurations with custom timeout settings

  @US-089-02 @AI @QA
  Scenario: RAG-enhanced agricultural knowledge Q&A
    Given a question about "late blight treatment for tomatoes"
    When the system retrieves the context from "farm.knowledge" via the RAG pipeline
    Then it must provide a professional, expert-level response
    And the response must be anchored to real-time farm data and historical interventions

  @US-089-05 @AI @Embedding
  Scenario: Automated vector embedding for agricultural knowledge
    Given new expert documentation or intervention logs
    When the model inheriting "EmbeddingMixin" is saved
    Then the system must automatically trigger an asynchronous vectorization task
    And store the result in the local PGVector database for semantic search
