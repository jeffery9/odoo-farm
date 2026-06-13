Feature: Epic 007 Mobile-First Field Ops
  As a Farm Worker or Warehouse Admin
  I want a simple, offline-capable mobile interface
  So that I can perform field operations accurately and efficiently

  @US-007-01 @Scan @UX
  Scenario: Rapid asset identification via QR scan
    Given I am a worker using the PWA
    When I scan a QR code of an asset
    Then the response must be within 2 seconds
    And the screen must display the asset's key status metrics
    And active tasks for the asset must be pre-cached for offline access

  @US-007-03 @UX @UI
  Scenario: Simplified field operation interface
    Given I am recording an intervention in the field
    When I navigate through the core workflow
    Then the number of clicks required must not exceed 3
    And all action buttons must have a height of at least 48px

  @US-007-13 @UX @Stepper
  Scenario: Keyboard-less input via "Stepper & Chips"
    Given I am entering the quantity of fertilizer consumed
    When I use the incremental chips (e.g., +1, +5)
    Then the value should increment without triggering the soft keyboard
    And I should be able to complete the input with a giant "Confirm" toggle

  @US-007-17 @Scan @RapidScan
  Scenario: Rapid continuous scanning mode for PDA
    Given I am a warehouse worker with a PDA
    When I activate "Rapid Scan Mode"
    And I scan multiple items sequentially
    Then each scan must be validated and persisted automatically without manual saving
    And if a scan fails, the screen must flash red and sound a continuous alarm
