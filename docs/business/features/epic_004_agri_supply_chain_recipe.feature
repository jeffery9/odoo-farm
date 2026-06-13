Feature: Epic 004 Agri-Supply Chain & Recipe
  As a Production Manager or Technician
  I want to use manufacturing logic for complex agricultural recipes and blending
  So that I can ensure full-chain traceability and efficient input management

  @US-004-01 @Recipe @TankMix
  Scenario: Dynamic Tank Mix recipe calculation
    Given I am a technician defining a fertilization recipe
    And the BoM has a "dilution_ratio" configured
    When I enter the target "Operation Area" in the production interface
    Then the system must automatically calculate the total quantity for each input component
    And it should support the registration of co-products

  @US-004-02 @Traceability @Blending
  Scenario: Blending traceability and lot parentage
    Given multiple input lots are consumed in an "mrp.production" order
    When the production is finished and an output lot is generated
    Then the output lot must record all "parent_lot_ids"
    And the Traceability Tree must show the input proportions and weights for each layer

  @US-004-04 @Warehouse @Safety
  Scenario: Expiry date rolling warning for agricultural inputs
    Given a manufacturing order is in progress
    When a batch of pesticide or fertilizer is selected for consumption
    Then the system must check the expiration date
    And if the batch is expired or within 30 days of expiry, a high-priority warning must be posted in the Chatter

  @US-004-05 @Inputs @Substitution
  Scenario: Input substitution and dosage recalculation
    Given a core input is out of stock
    And a substitute product is defined with a specific nutrient equivalent
    When I select the substitute in the production order
    Then the system must automatically recalculate the required dosage based on nutrient content
