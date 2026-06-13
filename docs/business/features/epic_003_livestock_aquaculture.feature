Feature: Epic 003 Livestock & Aquaculture
  As a Livestock Technician or Farm Manager
  I want to track animal health, growth, and feeding
  So that I can optimize production based on physiological models

  @US-003-01 @Feeding @ADG
  Scenario: Feeding plan and ADG model integration
    Given I am a livestock technician
    And the system has an Average Daily Gain (ADG) model configured
    When I record an "Actual Weighing" event for a lot
    Then the system should dynamically update the ADG and predicted weight
    And a feeding task should automatically generate an "mrp.production" order
    And completing the task must deduct feed inventory automatically

  @US-003-02 @Health @PWA
  Scenario: Health and Vaccination tracking with offline support
    Given I am a technician in a no-signal area
    When I perform a vaccination check-in via PWA
    Then the record must include a "device fingerprint" for verification
    And the system must automatically calculate the "Withdrawal Period End Date"
    And the associated lot must be locked for sales until that date

  @US-003-05 @Accounting @Costing
  Scenario: Automated mortality cost redistribution
    Given a lot of livestock with accumulated WIP costs
    When a "stock.scrap" event is triggered for a deceased individual
    Then the system must use "farm.mortality.amortization" to scan analytic lines
    And the costs from the deceased must be redistributed to the surviving individuals in the same lot
    And the total cost balance in the analytic account must remain consistent

  @US-003-06 @AI @Vision
  Scenario: Non-contact biomass measurement via AI vision
    Given a camera or PDA with AI weighing capabilities
    When I take a photo of a pig or fish group
    Then the AI model should estimate the average weight with < 5% error
    And the result should be saved to the "current_weight" field of the "stock.lot"
