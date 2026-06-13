Feature: Epic 122 Merchant Management Platform
  As an Event Manager or Finance Officer
  I want GIS-based booth planning and joint operation revenue sharing
  So that I can seamlessly manage third-party merchants in an agri-tourism setting

  @US-122-01 @GIS @Planning
  Scenario: GIS space planning for event booths
    Given a farm parcel designated for an agri-tourism event
    When the event manager uses the GIS interface to designate temporary booths
    Then the system must map these booths to "stock.location" records
    And display their real-time occupancy status (Rented/Available) with bilingual labels

  @US-122-02 @Compliance @Workflow
  Scenario: Merchant qualification Activity review flow
    Given a new merchant submitting their business license via the portal
    When the document is uploaded
    Then the system must automatically create an "Initial Review" Activity for the compliance officer
    And strictly block any associated contract confirmations if the license is expired

  @US-122-03 @Accounting @Settlement
  Scenario: Joint operation revenue sharing and automated settlement
    Given a merchant operating under a revenue-sharing agreement
    When the financial engine processes the end-of-month settlement
    Then it must calculate the commission based on the merchant's POS sales
    And automatically deduct utility costs measured by IoT meters
    And generate a bilingual settlement bill

  @US-122-04 @Portal @PWA
  Scenario: Third-party merchant PWA mobile portal
    Given an approved merchant operating a booth
    When they access the Merchant PWA
    Then they must be able to view the "Operational Manual" and their settlement history offline
    And receive important management notifications via Web Push
