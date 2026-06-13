Feature: Epic 084 ISL Architecture
  As a Developer or System Architect
  I want an Industry Standard Layer (ISL) for specialized agricultural logic
  So that I can extend core Odoo models for specific industries while maintaining data isolation

  @US-084-01 @Architecture @ISL
  Scenario: MRP Production order ISL extension and redirection
    Given a production order for a specific industry (e.g. Winery)
    When the system creates the industry-specific MO
    Then it must use the "_inherits" mechanism for transparent redirection
    And automatically apply industry-specific parameters and workflows

  @US-084-04 @ISL @Traceability
  Scenario: Industry-specific stock lot extension and attributes
    Given a stock lot in a specialized industry (e.g. Seed Industry)
    When I view the lot details
    Then the ISL model must expose industry-specific tracking and attribute requirements
    And maintain a link to the core stock lot while providing specialized quality gates

  @US-084-11 @Logic @Redirection
  Scenario: Transparent ISL model redirection mechanism
    Given a base Odoo model instance (e.g. sale.order)
    When the system identifies it as part of an industry-specific flow
    Then it must automatically redirect to the corresponding ISL extension model
    And the performance overhead for this redirection must not exceed 10%

  @US-084-12 @Developer @Isolation
  Scenario: Industry-specific extension isolation and flexibility
    Given multiple industry extensions active in the same Odoo instance
    When a developer adds a new industry feature
    Then the system must ensure the logic is isolated within the specific ISL layer
    And prevent cross-industry interference or dependency leakage
