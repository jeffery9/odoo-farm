Feature: Epic 093 Digital Twin Agriculture
  As a Technician or Agronomist
  I want a digital twin model of the farm with real-time IoT synchronization
  So that I can visualize physical operations in a 3D environment and simulate growth scenarios

  @US-093-01 @GIS @3D
  Scenario: Farm digital twin modeling and 3D scene management
    Given I am a technician
    When I define the farm's physical layout using high-precision GIS data
    Then the system must support loading GLB/USDZ models into the "Digital Twin Scene"
    And allow me to place IIoT device markers within the 3D coordinate space

  @US-093-02 @IOT @Simulation
  Scenario: Real-time sensor synchronization and "what-if" simulation
    Given a digital twin scene with active IIoT devices
    When sensors report real-time data from the field
    Then the digital twin must synchronize the status of the virtual components (e.g. moisture level, gate status)
    And support "what-if" simulations to predict the impact of environmental changes on crop growth
