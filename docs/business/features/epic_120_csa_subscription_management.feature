Feature: Epic 120 CSA Subscription Management
  As a CSA Farm Owner or Member
  I want an automated subscription engine and self-service portal
  So that I can manage weekly vegetable bags efficiently and improve member satisfaction

  @US-120-01 @Sales @Subscription
  Scenario: CSA subscription engine and automated renewal
    Given a customer subscribes to a "Seasonal Vegetable Box"
    When the subscription term approaches its end
    Then the system must automatically process the renewal based on the customer's settings
    And generate the required sales orders for the upcoming period

  @US-120-03 @Logistics @Scheduling
  Scenario: Automated delivery schedule generation for CSA members
    Given active CSA subscriptions with specific delivery frequency
    When the delivery manager runs the scheduling engine
    Then the system must automatically generate the delivery timetable and routes
    And send automated notifications to members regarding their delivery window

  @US-120-04 @Portal @SelfService
  Scenario: Member portal for subscription management and preferences
    Given a CSA member accessing the customer portal
    When they update their delivery address or vegetable preferences
    Then the system must instantly apply the changes to their active subscription
    And allow them to view their historical deliveries and billing statements

  @US-120-06 @Planning @Integration
  Scenario: Integrating CSA orders with harvest planning
    Given a set of confirmed CSA orders for the week
    When the farm planner reviews the production dashboard
    Then the system must aggregate the required vegetable quantities
    And match them against the forecasted harvest yield, highlighting any shortages
