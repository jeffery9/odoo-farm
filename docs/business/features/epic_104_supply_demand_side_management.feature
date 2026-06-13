Feature: Epic 104 Supply Demand-Side Management
  As a Supply Chain Manager or Market Analyst
  I want multi-dimensional demand forecasting and consumer sentiment analysis
  So that I can achieve precise supply-demand matching and improve customer satisfaction

  @US-104-01 @AI @Forecasting
  Scenario: Multi-dimensional demand forecasting using weather and market trends
    Given historical sales data and seasonal market patterns
    And 24-hour weather forecasts suggesting a heatwave
    When the "ai.decision.engine" runs a demand prediction for cold beverages or fresh fruit
    Then it must increase the predicted demand for the upcoming period
    And provide a "Forecast Confidence Level" for the adjusted quantity

  @US-104-03 @AI @Sentiment
  Scenario: Consumer sentiment analysis for product feedback
    Given a list of customer reviews and feedback from the C2M portal (Epic 097)
    When the NLP engine (Epic 089) performs a sentiment analysis
    Then it must classify the feedback as Positive, Neutral, or Negative
    And identify key "Pain Points" or "Feature Requests" to inform future production plans

  @US-104-08 @Logic @Inventory
  Scenario: Dynamic inventory optimization based on demand spikes
    Given an identified demand spike for a specific variety
    When the inventory engine calculates the safety stock
    Then it must automatically suggest a stock distribution adjustment across warehouse locations
    And visualize the "Optimal vs Current" stock levels to the warehouse manager
