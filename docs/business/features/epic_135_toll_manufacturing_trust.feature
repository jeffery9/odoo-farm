Feature: Epic 135 Toll Manufacturing Trust
  As a Cooperative Manager or Brand Protection Officer
  I want strict mass balance validation and branded packaging control
  So that I can prevent raw material substitution and unauthorized brand usage during toll manufacturing

  @US-135-01 @Subcontracting @MassBalance
  Scenario: Toll manufacturing mass balance limit and anomaly blocking
    Given a subcontracting order with a defined "Yield Tolerance" (e.g. Min 25%)
    When the subcontractor returns finished goods falling below the tolerance limit
    Then the system must block the inventory receipt validation
    And trigger a "Mass Balance Anomaly" requiring managerial intervention

  @US-135-02 @Brand @Security
  Scenario: Branded packaging control and 1:1 serial tracking
    Given a subcontracting order involving branded packaging materials with serial numbers
    When the finished goods are received from the subcontractor
    Then the system must force the warehouse operator to scan and verify the specific serial numbers of the returned packaging
    And require a formal "Scrap" process with photographic evidence for any damaged packaging

  @US-135-03 @Quality @Freeze
  Scenario: Toll manufacturing quality freeze on failed lab test
    Given a finished product batch received from a subcontractor
    When an external lab test (e.g. pesticide residue) is recorded as "Failed"
    Then the system must freeze the batch's digital traceability passport
    And instantly block any Odoo POS terminal from scanning or selling the batch
