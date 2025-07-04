@smoke

Feature: Here you enter feature name, e.g. Create trips and run API simulator
#  Scenario: Here you enter test case ID and name, e.g. RT-T0000 Create Mary Kay Trip and run API simulator
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "mary_kay_trip"
#    When I create stops locations for the trip with test_id "mary_kay_trip"
#    Then I create a new Trip with Monitors for the test_id "mary_kay_trip"
##    Then I process trip for the test_id "mary_kay_trip" using API call
#    Then I process trip for the test_id "mary_kay_trip" using "Command Prompt"
##
#  Scenario: Here you enter test case ID and name, e.g. RT-T0000 Create Mary Kay Trip and run API simulator
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "mary_kay_trip"
#    When I create stops locations for the trip with test_id "mary_kay_trip"
#    Then I create a new Trip with Container for the test_id "mary_kay_trip"
##    Then I process trip for the test_id "mary_kay_trip" using API call
#    Then I process trip for the test_id "mary_kay_trip" using "Command Prompt"
#####
  Scenario: Create Bellevue, WA to Abbotsford, BC trip with monitors
    Given I create access token for "sensitech_admin"
    When I create origin location for the trip with test_id "bellevue_wa_to_abbotsford_bc_trip" from csv
    When I create stops locations for the trip with test_id "bellevue_wa_to_abbotsford_bc_trip" from csv
    Then I create a new Trip with Monitors for the test_id "bellevue_wa_to_abbotsford_bc_trip"
    Then I process trip for the test_id "bellevue_wa_to_abbotsford_bc_trip" using "Command Prompt"
#
#  Scenario: Create Bellevue, WA to Abbotsford, BC trip with container
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "bellevue_wa_to_abbotsford_bc_trip"
#    When I create stops locations for the trip with test_id "bellevue_wa_to_abbotsford_bc_trip"
#    Then I create a new Trip with Container for the test_id "bellevue_wa_to_abbotsford_bc_trip"
#    Then I process trip for the test_id "bellevue_wa_to_abbotsford_bc_trip" using "Command Prompt"
#
#  Scenario: Create VT to MA (Multiple Monitors) trip with container
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "vt_to_ma_multiple_monitors"
#    When I create stops locations for the trip with test_id "vt_to_ma_multiple_monitors"
#    Then I create a new Trip with Container for the test_id "vt_to_ma_multiple_monitors"
##    Then I process trip for the test_id "vt_to_ma_multiple_monitors" using API call
#    Then I process trip for the test_id "vt_to_ma_multiple_monitors" using "Command Prompt"
#
#  Scenario: Create trip with Automation Rule:
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "vt_to_ma_multiple_monitors"
#    When I create stops locations for the trip with test_id "vt_to_ma_multiple_monitors"
#    Then I create a container for the trip with the test_id "vt_to_ma_multiple_monitors"
#    Then I create a new Automation Outbound Rule for Trips(or update if it exist) with "All Containers" container group and the name "Outbound Automation Rule"
##    Then I process trip for the test_id "vt_to_ma_multiple_monitors" using API call
#    Then I process trip for the test_id "vt_to_ma_multiple_monitors" using "Command Prompt"
#
#  Scenario: Create sysco_denver_dc trip with container
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "sysco_denver_dc"
#    When I create stops locations for the trip with test_id "sysco_denver_dc"
#    Then I create a new Trip with Container for the test_id "sysco_denver_dc"
##    Then I process trip for the test_id "sysco_denver_dc" using API call
#    Then I process trip for the test_id "sysco_denver_dc" using "Command Prompt"
#
#  Scenario: Create sysco_denver_dc trip with Automation Rule:
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "sysco_denver_dc"
#    When I create stops locations for the trip with test_id "sysco_denver_dc"
#    Then I create a container for the trip with the test_id "sysco_denver_dc"
#    Then I create a new Automation Outbound Rule for Trips(or update if it exist) with "All Containers" container group and the name "Outbound Automation Rule"
##    Then I process trip for the test_id "sysco_denver_dc" using API call
#    Then I process trip for the test_id "sysco_denver_dc" using "Command Prompt"
#
#  Scenario: Create ozark_fontana_vegas trip
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "ozark_fontana_vegas"
#    When I create stops locations for the trip with test_id "ozark_fontana_vegas"
#    Then I create a new Trip with Monitors for the test_id "ozark_fontana_vegas"
##    Then I process trip for the test_id "ozark_fontana_vegas" using API call
#    Then I process trip for the test_id "ozark_fontana_vegas" using "Command Prompt"
#
#  Scenario: Create Bellevue, WA to Abbotsford, BC trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip"
#    When I create stops locations for the trip with test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip"
#    Then I create a new Trip with Monitors for the test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip"
#    Then I process trip for the test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip" using "Command Prompt"
#
#  Scenario: Create Bellevue, WA to Abbotsford, BC trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip"
#    When I create stops locations for the trip with test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip"
#    Then I create a new Trip with Container for the test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip"
#    Then I process trip for the test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip" using "Command Prompt"
#
#  Scenario: Create Bellev/levue_wa_to_abbotsford_bc_trip_1" using "Command Prompt"
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip_1"
#    When I create stops locations for the trip with test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip_1"
#    Then I create a new Trip with Container for the test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip_1"
#    Then I process trip for the test_id "nohumiditydata_bellevue_wa_to_abbotsford_bc_trip_1" using "Command Prompt"
#
#  Scenario: Create sysco_denver_dc trip with container
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "sysco_denver_dc_short"
#    When I create stops locations for the trip with test_id "sysco_denver_dc_short"
#    Then I create a new Trip with Container for the test_id "sysco_denver_dc_short"
#    Then I process trip for the test_id "sysco_denver_dc_short" using "Command Prompt"
#
#  Scenario: Create sysco_denver_dc trip with Automation Rule:
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "sysco_denver_dc_short"
#    When I create stops locations for the trip with test_id "sysco_denver_dc_short"
#    Then I create a container for the trip with the test_id "sysco_denver_dc_short"
#    Then I create a new Automation Outbound Rule for Trips(or update if it exist) with "All Containers" container group and the name "Outbound Automation Rule"
#    Then I process trip for the test_id "sysco_denver_dc_short" using "Command Prompt"
#####
#  Scenario: Create irland_spain_irland trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "irland_spain_irland"
#    When I create stops locations for the trip with test_id "irland_spain_irland"
#    Then I create a new Trip with Monitors for the test_id "irland_spain_irland"
#    Then I process trip for the test_id "irland_spain_irland" using "Command Prompt"

#  Scenario: Create sw_to_il_geo_x trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "sw_to_il_geo_x"
#    When I create stops locations for the trip with test_id "sw_to_il_geo_x"
#    Then I create a new Trip with Monitors for the test_id "sw_to_il_geo_x"
#    Then I process trip for the test_id "sw_to_il_geo_x" using "Command Prompt"
#
#  Scenario: Create sw_to_il_geo_x trip with container
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "sw_to_il_geo_x"
#    When I create stops locations for the trip with test_id "sw_to_il_geo_x"
#    Then I create a new Trip with Container for the test_id "sw_to_il_geo_x"
#    Then I process trip for the test_id "sw_to_il_geo_x" using "Command Prompt"

#  Scenario: Create sw_to_il_geo_x trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "wa_to_bc_long"
#    When I create stops locations for the trip with test_id "wa_to_bc_long"
#    Then I create a new Trip with Monitors for the test_id "wa_to_bc_long"
#    Then I process trip for the test_id "wa_to_bc_long" using "Command Prompt"
##
#  Scenario: Create sw_to_il_geo_x trip with Container
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "wa_to_bc_long"
#    When I create stops locations for the trip with test_id "wa_to_bc_long"
#    Then I create a new Trip with Container for the test_id "wa_to_bc_long"
#    Then I process trip for the test_id "wa_to_bc_long" using "Command Prompt"
##########
#  Scenario: Beverly Office to Denvers Cell and WiFi trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "bev_to_den_cell_and_wifi"
#    When I create stops locations for the trip with test_id "bev_to_den_cell_and_wifi"
#    Then I create a new Trip with Monitors for the test_id "bev_to_den_cell_and_wifi"
#    Then I process trip for the test_id "bev_to_den_cell_and_wifi" using "Command Prompt"
#
#  Scenario: Beverly Office to Denvers Cell and WiFi Original trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "bev_to_den_cell_and_wifi_original"
#    When I create stops locations for the trip with test_id "bev_to_den_cell_and_wifi_original"
#    Then I create a new Trip with Monitors for the test_id "bev_to_den_cell_and_wifi_original"
#    Then I process trip for the test_id "bev_to_den_cell_and_wifi_original" using "Command Prompt"
#
# Scenario: Beverly Office to Denvers Wifi Only trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "bev_to_den_wifi_only"
#    When I create stops locations for the trip with test_id "bev_to_den_wifi_only"
#    Then I create a new Trip with Monitors for the test_id "bev_to_den_wifi_only"
#    Then I process trip for the test_id "bev_to_den_wifi_only" using "Command Prompt"
#
# Scenario: Beverly Office to Denvers Cell Only trip with monitors
#    Given I create access token for "sensitech_admin"
#    When I create origin location for the trip with test_id "bev_to_den_cell_only"
#    When I create stops locations for the trip with test_id "bev_to_den_cell_only"
#    Then I create a new Trip with Monitors for the test_id "bev_to_den_cell_only"
#    Then I process trip for the test_id "bev_to_den_cell_only" using "Command Prompt"