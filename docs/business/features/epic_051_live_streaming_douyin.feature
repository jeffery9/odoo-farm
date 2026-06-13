Feature: Epic 051 Live Streaming & Douyin Integration
  As a Marketing Manager or Streamer
  I want to link farm production data with Douyin live streams
  So that I can increase product value through real-time traceability and engagement

  @US-051-01 @Douyin @Auth
  Scenario: Douyin account authorization and token management
    Given I am a marketing manager
    When I link the farm's Douyin enterprise account via OAuth 2.0
    Then the system must implement a "Refresh Token" mechanism to ensure the link remains active
    And allow me to manage multiple accounts (e.g. Official and Influencer)

  @US-051-03 @Marketing @Traceability
  Scenario: Associating products with live streams for traceability
    Given a live stream is active on Douyin
    When the streamer features a specific product
    Then the product detail page in the stream must include a "One-click Traceability" button
    And clicking it must redirect to the "Farm-to-Table" portal (US-08-01) with bilingual content

  @US-051-04 @Ecommerce @Logistics
  Scenario: Automated Douyin order import and address normalization
    Given a customer places an order during a Douyin live stream
    When the system receives the order via Webhook
    Then it must automatically create a "sale.order" in Odoo with the Douyin order ID as reference
    And normalize the customer address to match Odoo's provincial/city data structures

  @US-051-09 @KOL @Attribution
  Scenario: Influencer performance attribution for live sales
    Given a sales order imported from a Douyin influencer channel
    When the order is confirmed
    Then the system must identify the influencer ID from the channel reference
    And automatically tag the influencer in the analytic account for accurate commission calculation
