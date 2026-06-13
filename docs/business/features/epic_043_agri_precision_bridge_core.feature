Feature: Epic 043 Agri-Precision Bridge Core
  As a Production Manager or System Architect
  I want a bridge between standard ERP and precision manufacturing logic
  So that I can handle uncertainty, product grading, and IoT-driven interventions

  @US-AGRI-01 @Uncertainty @Yield
  Scenario: Dynamic yield uncertainty handling and calibration
    Given a production order inheriting "agri.precision.mixin"
    When I record a periodic metrology or sampling event
    Then the system must update the "expected_yield_accuracy" and "last_metrology_date"
    And allow me to calibrate the yield estimate via "action_update_yield_estimate()"

  @US-AGRI-02 @Grading @Finance
  Scenario: Product grading and stock lot integration
    Given a production process is finished
    When I record the quality results as "Premium", "Standard", or "Substandard"
    Then the "stock.lot" must inherit the "quality_grade" attribute
    And the UI must display a color-coded ribbon based on the grade

  @US-AGRI-03 @Intervention @Corrective
  Scenario: Intervention mechanism and corrective skill application
    Given a production order in a critical status
    When an anomaly is detected or manually reported
    Then the system must allow the application of a "Corrective Skill" via "agri.intervention"
    And increment the "intervention_count" for the order

  @US-AGRI-04 @IOT @Bridge
  Scenario: IoT integration bridge and sensor-driven intervention
    Given a production order associated with IoT devices
    When a sensor reading deviates from the target range
    Then the system must be able to trigger an automated intervention via the IoT bridge
    And update the "iot_status" in the production interface
