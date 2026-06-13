Feature: Epic 055 Generic Field Evidence
  As a Quality Auditor or Compliance Officer
  I want a universal system for capturing and verifying field evidence
  So that I can provide high-trust documentation for all farm activities and regulatory audits

  @US-055-01 @PWA @Capture
  Scenario: Universal offline evidence capture for any activity
    Given I am a worker inspecting a parcel for disease
    When I capture a photo of the symptoms via the PWA
    Then the system must allow me to link the evidence to any Odoo model (Task, Parcel, Lot)
    And store the image in the local IndexedDB queue if offline

  @US-055-02 @Traceability @Watermark
  Scenario: Automated environmental watermarks for evidence photos
    Given I have captured a piece of field evidence
    When I export or view the evidence record
    Then the image must display an overlaid watermark containing: GPS coordinates, Capture full name, and Server sync time

  @US-055-03 @Audit @GIS
  Scenario: Spatial compliance auditing for evidence capture locations
    Given multiple pieces of evidence captured in the field
    When the auditor runs a compliance check
    Then the system must compare the capture coordinates against the parcel boundaries
    And mark each record with a Red or Green status indicating "Location Compliance"

  @US-055-05 @Security @Hashing
  Scenario: Evidence chain integrity verification via hash summaries
    Given a piece of evidence captured in the field
    When the capture is performed
    Then the system must immediately generate a SHA-256 hash summary of the data
    And after synchronization, the system must re-verify the hash to detect any unauthorized tampering
