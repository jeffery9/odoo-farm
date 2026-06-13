Feature: Epic 036 HR & Labor Scheduling
  As a Farm Owner or Production Manager
  I want to manage agricultural skills, schedule labor, and track field timesheets
  So that I can optimize workforce utilization and allocate labor costs accurately

  @US-036-01 @HR @Skills
  Scenario: Skill-based labor filtering and assignment
    Given I am assigning a "Harvesting" task
    And employees have skills like "Harvester Operator" or "General Worker"
    When I filter for available personnel
    Then the system must highlight employees with the "Harvester Operator" skill
    And hide or de-prioritize those without the required skill

  @US-036-03 @PWA @Timesheet
  Scenario: Offline field timesheet recording with GPS validation
    Given I am a worker using the PWA in the field
    When I record the start and end of my shift
    Then the system must silently capture GPS coordinates for each punch-in/out
    And automatically generate "hr.timesheet" entries once signal is restored

  @US-036-04 @Accounting @Costing
  Scenario: Automated labor cost allocation to parcels/varieties
    Given a timesheet entry linked to a specific field intervention
    When the "hr.timesheet" is processed
    Then the system must use the "analytic_account_id" to aggregate costs
    And provide a report showing labor costs per parcel and per crop variety

  @US-036-05 @Payroll @Performance
  Scenario: Piece-rate harvesting wages and performance linkage
    Given a piece-rate wage defined for apple harvesting
    When a worker confirms a harvest quantity of "500kg"
    Then the system must automatically calculate the wage (Quantity * Rate)
    And create a "Piece-rate Labor Cost" line in the associated task's analytic account
