Feature: Epic 077 Biological Growth Intelligence
  As an Agricultural Scientist or Farm Owner
  I want digital variety models and phenology prediction
  So that I can transition from retrospective recording to proactive forecasting of crop growth

  @US-077-01 @Science @DigitalTwin
  Scenario: Digital varietal twin and Logistic growth curve modeling
    Given a variety ("product.template") inheriting "GrowthMixin"
    When the agricultural scientist configures GDD thresholds and Logistic growth parameters (L, k, x0)
    Then the system must support visual fitting of the standard growth curve
    And store critical development constants like Tbase and Topt in the variety library

  @US-077-02 @GDD @Prediction
  Scenario: Dynamic phenology stage prediction and critical window alerts
    Given real-time weather data and an active production cycle
    When the "GDD_Evaluator" runs its daily assessment
    Then it must automatically calculate the cumulative GDD
    And trigger a calendar alert if the crop is predicted to enter a key stage (e.g. flowering) within 3 days

  @US-077-03 @AI @Recommendation
  Scenario: Smart water and nutrient recommendation engine
    Given soil moisture and weather forecast data
    When the "ai.decision.engine" applies the Penman-Monteith formula
    Then it must calculate the "Water Gap" and generate a suggested irrigation task
    And the suggestion must pass a "BasePPOCritic" confidence check before being presented to the user

  @US-077-04 @Risk @Yield
  Scenario: Yield risk modeling and dynamic probability forecasting
    Given ongoing production with recorded biomass and stress data
    When the system analyzes the physical deviation from the variety's baseline
    Then it must provide a dynamic dashboard showing estimated yield probabilities (High/Medium/Low)
    And record the prediction history for seasonal accuracy auditing
