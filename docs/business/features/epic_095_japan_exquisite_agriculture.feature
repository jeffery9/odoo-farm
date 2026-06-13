Feature: Epic 095 Artisan Excellence & Inclusive Operations
  As a Farm Owner or Aging Farmer
  I want inclusive UI modes and precision curing/dehydration monitoring
  So that I can empower diverse farm populations and ensure high-quality artisan produce

  @US-095-01 @UX @Inclusive
  Scenario: Inclusive UX mode for aging agricultural populations
    Given I am an aging farmer operating in high-light conditions
    When I enable the "Inclusive Mode" in system settings
    Then the global UI must scale fonts by 1.5x and increase icon contrast
    And ensure core buttons (Scan, Photo, Voice) occupy at least 40% of the screen area

  @US-095-02 @IOT @Artisan
  Scenario: Precision curing and dehydration process monitoring
    Given a high-value batch of dried fruit or ham
    When IoT sensors monitor the weight loss and moisture percentage
    Then the system must alert if the dehydration rate deviates from the artisan model
    And generate a "Process Bio" to justify the premium quality to consumers

  @US-095-03 @Accounting @Inclusive
  Scenario: Agricultural standard costing for non-financial users
    Given a small-scale farm owner
    When they use the "Costing Wizard"
    Then the system must provide pre-set agricultural categories (Seeds, Labor, Machinery)
    And automatically allocate input consumption to the parcel's center-of-cost without complex accounting jargon
