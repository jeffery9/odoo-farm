Feature: Epic 056 Field Operations Services
  As a Scheduler or Technician
  I want advanced field services like voice input, AR overlays, and remote expert connections
  So that I can improve operational efficiency and handle complex field issues in real-time

  @US-056-01 @UX @Voice
  Scenario: Offline agricultural voice input with terminology recognition
    Given I am a machine operator in the field with no network
    When I record an operation using the voice input feature
    Then the system must accurately recognize agricultural terms with > 90% accuracy
    And store the transcription locally for later sync

  @US-056-05 @WebRTC @Expert
  Scenario: Real-time remote expert connection via WebRTC
    Given a technician encountering an unknown pest in the field
    When the technician initiates a "Remote Expert" video call
    Then the system must establish a high-definition WebRTC connection
    And automatically link the call log and recording to the current intervention task

  @US-056-06 @AR @GIS
  Scenario: AR virtual field stakes for underground asset visualization
    Given I am a worker using the mobile camera in a parcel
    When I point the camera towards a specific location
    Then the system must overlay a virtual stake showing underground pipelines or sensors
    And the coordinate precision of the AR overlay must be within 1 meter

  @US-056-07 @Dispatch @Crowdsourcing
  Scenario: "Grab-mode" for urgent agricultural task response
    Given an urgent intervention task pushed to the public pool
    When the system identifies active workers within 1km using GPS
    Then it must notify those workers and allow them to "Grab" the task
    And upon successful grabbing, automatically generate the assignment and associated Activity
