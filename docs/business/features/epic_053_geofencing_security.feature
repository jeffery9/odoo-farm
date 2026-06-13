Feature: Epic 053 Geofencing & Boundary Security
  As a Farm Owner or Fleet Manager
  I want virtual geographic boundaries for asset monitoring and operation constraints
  So that I can ensure security and prevent unauthorized activity outside designated zones

  @US-053-02 @IOT @Livestock
  Scenario: Real-time alert for livestock crossing a virtual fence
    Given a livestock asset wearing a GPS ear-tag
    And a virtual fence defined as a GIS polygon
    When the asset moves outside the polygon boundary
    Then the system must send an immediate mobile push notification to the technician
    And the crossing event must be recorded in the asset's batch history

  @US-053-04 @Machinery @Audit
  Scenario: Machinery operation range auditing and off-site tracking
    Given a tractor performing an intervention task
    When the system analyzes the GPS trajectory log
    Then it must generate a heatmap of the machine's movement
    And automatically calculate the "Off-site operation duration" for settlement deduction

  @US-053-05 @Quarantine @HardBlock
  Scenario: Automated quarantine buffer zone interception
    Given an epidemic outbreak is reported on a specific lot
    When a virtual quarantine buffer is automatically generated (Epic 031)
    Then the system must mark the associated parcels as "Restricted"
    And block the movement of any other lots into the restricted zone
