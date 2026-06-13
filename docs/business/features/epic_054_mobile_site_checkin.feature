Feature: Epic 054 Mobile Site Check-in
  As a Farm Worker or HR Manager
  I want mobile GPS and photo-based check-ins for field operations
  So that I can ensure the authenticity of farm work and automate timesheet recording

  @US-054-01 @PWA @Checkin
  Scenario: Geographic field check-in with offline support
    Given I am a worker at a remote parcel with no signal
    When I perform a "One-tap Check-in" via the PWA
    Then the system must record the GPS coordinates and server time locally
    And the check-in interface must be accessible from the PWA cache

  @US-054-02 @UX @Verification
  Scenario: Automatic parcel boundary matching and verification
    Given a worker has checked into a parcel
    When the system analyzes the GPS location using the "Ray Casting" algorithm
    Then it must provide instant feedback if the worker is outside the assigned parcel boundary
    And this verification must occur locally on the mobile device for offline support

  @US-054-04 @Quality @Evidence
  Scenario: Site photo evidence with GPS and time watermark
    Given I am checking into a field task
    When I capture a required site photo
    Then the photo must automatically include an unmodifiable watermark with GPS and timestamp
    And the photo must be linked to the active production lot (US-25-01)

  @US-054-06 @Security @Biometrics
  Scenario: Mandatory biometric/liveness verification for critical check-ins
    Given a critical check-in point requiring high security
    When I attempt to check in via the PWA
    Then the app must invoke the native biometric interface (or SDK)
    And block the check-in if liveness or identity verification fails
