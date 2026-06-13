Feature: Epic 069 Agricultural Weather Station
  As a Farm Manager or Risk Administrator
  I want a hyper-local weather consensus network with high-precision forecasting
  So that I can mitigate weather-related risks and optimize the timing of agricultural interventions

  @US-069-01 @IOT @Monitoring
  Scenario: Real-time multi-parameter environmental data collection
    Given a hyper-local weather station linked to Odoo
    When sensors report temperature, wind speed, and rain intensity every 15 minutes
    Then the data must be transparently mapped to the "Weather Station" model
    And include soil moisture and CO2 readings for a comprehensive environmental profile

  @US-069-02 @Weather @Prediction
  Scenario: Localized weather forecasting and production impact assessment
    Given historical data from local weather stations
    When the "ai.decision.engine" generates a 24-hour forecast
    Then it must automatically evaluate the risk of frost or gale for the current crop stage
    And suggest the optimal time for a planned spraying or harvest intervention

  @US-069-05 @Consensus @Audit
  Scenario: Cross-farm weather data sharing and consensus verification
    Given multiple weather stations within a 5km radius from different farms
    When a single station reports a high-intensity storm event
    Then the system must compare the reading against neighboring stations (Consensus Logic)
    And only trigger a "Regional Disaster Alert" if the綜合 confidence score exceeds 0.8

  @US-069-07 @Finance @Costing
  Scenario: Shared weather asset ownership and maintenance fee allocation
    Given a high-precision weather station co-owned by several farm entities
    When maintenance or calibration costs are recorded for the asset
    Then the system must automatically allocate the fees to the participating farms
    And the allocation weight must be based on their respective GIS beneficiary areas
