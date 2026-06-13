Feature: Epic 080 Hierarchy View Containers
  As a Group Administrator or Operations Director
  I want logical view containers and cross-model OPE aggregation
  So that I can manage large-scale farm clusters through multiple strategic perspectives

  @US-080-01 @Structure @Hierarchy
  Scenario: Logical management containers for non-physical grouping
    Given I am a group administrator
    When I create a "Logical View Container"
    Then I must be able to link multiple parcels and resources to the container
    And the associations must be non-exclusive (one parcel in multiple containers)

  @US-080-02 @UX @Navigation
  Scenario: Recursive nesting and tree-based navigation
    Given a hierarchy of management containers
    When I view the management dashboard
    Then the system must support infinite recursive nesting (parent_id)
    And provide "Breadcrumbs" or a "Tree Component" for hierarchical navigation

  @US-080-03 @OPE @Aggregation
  Scenario: Cross-model OPE aggregation for logical views
    Given a management container containing several parcels
    When I trigger the "Calculate View Performance" action
    Then the system must aggregate the OPE scores of all linked assets via "farm.ope.mixin"
    And apply area-weighted rolling updates to the container's performance metrics

  @US-080-04 @Security @Permissions
  Scenario: Container-based data access and visibility control
    Given a user authorized to a specific management container
    When the user logs into the system
    Then the system must apply container-level "ir.rule" filters
    And the user should only see data for assets within their authorized container and its children
