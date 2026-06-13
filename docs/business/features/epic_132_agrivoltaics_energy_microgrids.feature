Feature: Epic 132 Agrivoltaics & Energy Microgrids
  As a Farm Planner or Energy Administrator
  I want GIS-based agrivoltaic mapping and demand-response scheduling
  So that I can balance energy production with agricultural needs and maximize energy self-sufficiency

  @US-132-01 @GIS @Agrivoltaics
  Scenario: Agrivoltaics GIS asset mapping and shadow analysis
    Given a farm parcel designated for agrivoltaics in "farm.location"
    When the farm planner defines the PV array polygons, tilt angles, and height
    Then the system must calculate the effective shading rate on the crops below based on seasonal solar angles
    And register each PV sub-array as an independent node in the IoT monitoring tree

  @US-132-02 @Energy @Monitoring
  Scenario: Real-time power generation and agricultural load aggregation
    Given an operational agrivoltaic microgrid
    When the MQTT broker receives data from inverters and smart meters
    Then the dashboard must display the real-time power surplus or deficit
    And allow multi-dimensional energy efficiency analysis (e.g. PV generation vs Irrigation load)
    And automatically account for Battery Energy Storage System (BESS) charge/discharge losses

  @US-132-03 @Scheduling @DemandResponse
  Scenario: Smart load scheduling based on demand-response and PV generation
    Given a weather forecast predicting a sunny day with high PV surplus
    When the energy administrator enables smart load scheduling
    Then the system must automatically advance "energy-sensitive" tasks (e.g. heavy irrigation or cooling) to the peak generation window
    And support automatic step-down commands to secondary equipment during high tariff periods or low generation

  @US-132-04 @V2G @Machinery
  Scenario: V2G integration for electric agricultural machinery
    Given a fleet of electric tractors equipped with V2G (Vehicle-to-Grid) capabilities
    When the system monitors their State of Charge (SoC) and the microgrid faces a critical power shortage
    Then it must prioritize charging based on electricity prices and task urgency
    And allow automated or manual triggering of "Emergency Discharge Mode" to supply power back to the farm grid
