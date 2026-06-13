Feature: Epic 039 Agri-UX Standard
  As a Farm Owner or Worker
  I want a simplified, agricultural-themed user interface
  So that I can operate the system efficiently without industrial ERP jargon

  @US-039-01 @UX @Mapping
  Scenario: Deep term mapping from industrial to agricultural semantics
    Given I am a farm manager using the "Planting" industry context
    When the system loads a form or menu
    Then the "ViewInterceptor" must automatically replace industrial labels (e.g. "Work Order" to "Intervention")
    And any exported PDF report headers must use the mapped agricultural terms

  @US-039-03 @UX @Visual
  Scenario: Visual status indicators with "Traffic Light" principle
    Given a list of tasks in different states
    When I view the mobile card view
    Then the system must use the "Three-color Signal" principle (Red for alerts, Orange for transitions, Green for safe)
    And each card must display at least two key visual badges (e.g. PHI status, GDD progress)

  @US-039-15 @UX @Automation
  Scenario: One-click batch closure for agricultural tasks
    Given a list of selected daily intervention tasks
    When the production manager triggers the "Batch Closure Wizard"
    Then the system must allow bulk entry of executor and date
    And close all selected tasks in a single action

  @US-039-25 @Framework @Interceptor
  Scenario: De-industrialization view interceptor logic
    Given a developer creating a model inheriting from "mrp"
    When the frontend renders the view
    Then the "AgriViewMixin" must override "fields_view_get"
    And filter out non-agricultural UI elements based on the current Industry Context
