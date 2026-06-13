Feature: Epic 061 Reverse Supply Chain
  As a Quality Director or Customer Service Agent
  I want a "Kill Switch" for unsafe lots and a reverse traceability audit
  So that I can protect consumer safety and respond to product recalls in seconds

  @US-061-01 @Crisis @KillSwitch
  Scenario: Rapid batch "Kill Switch" for safety crises
    Given a major safety hazard is discovered for a product batch
    When the quality director activates the "Kill Switch" for that lot
    Then the system must force all associated "stock.lot" records to "locked" status
    And automatically suspend any confirmed but unshipped sales orders containing that lot

  @US-061-02 @Traceability @Audit
  Scenario: Consumer-level reverse traceability audit
    Given a finished product with a serial number or QR code
    When the customer service agent scans the number
    Then the system must provide a "Reverse Traceability View"
    And show the full path from the end product back to the farm parcel, operator, and input batches

  @US-061-03 @Alerts @CRM
  Scenario: Automated downstream customer alerts for product recalls
    Given a batch recall has been initiated and confirmed
    When the system runs the recall protocol
    Then it must automatically scan all sales orders for the affected lot
    And push a high-priority risk warning to all downstream distributors and customers via bilingual templates
