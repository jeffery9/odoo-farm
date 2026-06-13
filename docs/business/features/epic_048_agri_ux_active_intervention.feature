Feature: Epic 048 Agri-UX for Active Intervention
  As a Field Technician or Operator
  I want intuitive UI components for AI-driven decisions
  So that I can quickly recognize risks and execute remedial actions in the field

  @US-048-01 @UX @AI
  Scenario: AI decision dynamic pop-over in intervention form
    Given a pending AI suggestion for a specific parcel
    When I open the intervention form for that parcel
    Then a high-visibility orange banner must pop up with a summary of the AI advice
    And the terminology must be non-industrial (e.g. "Execution Suggestion" instead of "Commit JSON")

  @US-048-02 @UX @OneTap
  Scenario: "One-Tap" execution of complex remedial actions
    Given an AI-suggested remedial action
    When I click the giant "Accept Suggestion" button (at least 48px)
    Then the system must automatically update the relevant "agri.bom.parameter" values
    And synchronize the changes to the MQTT edge devices immediately

  @US-048-03 @UX @Feedback
  Scenario: Decision feedback loop and rejection reasons
    Given an AI-suggested intervention
    When I choose to reject the suggestion
    Then the system must present a quick-selection list of rejection reasons (e.g. "Equipment under repair")
    And feed the reason back into the AI learning model while updating the "Confidence Score"
