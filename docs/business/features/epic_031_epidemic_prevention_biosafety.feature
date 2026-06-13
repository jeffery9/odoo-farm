Feature: Epic 031 Epidemic Prevention & Biosafety
  As a Technician or Safety Officer
  I want to manage vaccination schedules, quarantine processes, and biosafety barriers
  So that I can prevent disease outbreaks and ensure a safe production environment

  @US-031-01 @Planning @Alerts
  Scenario: Automated vaccination and pest control scheduling
    Given a biological asset with a recorded birth or planting date
    When the asset reaches a specific growth stage
    Then the system must automatically generate a prevention task from the "Prevention Template"
    And create a pending Activity on the technician's dashboard

  @US-031-02 @Quarantine @PWA
  Scenario: Quarantine process and isolation with photo evidence
    Given a disease outbreak is detected in a specific lot
    When I mark the lot as "Quarantine" via the PWA
    Then the system must move the lot to the "Isolation Zone"
    And I must provide a site photo as evidence which cannot be modified

  @US-031-03 @Logic @PHI
  Scenario: Post-Harvest Interval (PHI) tracking and sales blocking
    Given a lot that has been treated with a specific pesticide or veterinary drug
    When the drug has a defined "withdrawal_period"
    Then the system must calculate the "withdrawal_end_datetime" on the lot
    And it must block any sales order (SO) confirmation for that lot until the date is reached

  @US-031-04 @GIS @Emergency
  Scenario: Automated spatial buffer zone for epidemic hotspots
    Given a major epidemic is reported for a location
    When I mark the hotspot in the system
    Then the system must call the "Geofencing API" (Epic 053) to generate a 500m polygon buffer
    And it must automatically scan for active tasks in the buffer and notify executors to evacuate
    And the buffer zone must be highlighted in red on the map
