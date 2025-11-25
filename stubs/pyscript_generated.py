from typing import Any, Literal
from datetime import datetime
from pyscript_builtins import StateVal

class _ai_task_state(StateVal):
    supported_features: int

class ai_task:
    google_ai_task: _ai_task_state

    @staticmethod
    def generate_data(*, task_name: str, instructions: str, entity_id: str | None=None, structure: Any | None=None, attachments=None) -> dict[str, Any]:
        """

        Args:
            task_name:  Example: home summary
            instructions:  Example: Generate a funny notification that the garage door was left open
            structure:  Example: { "name": { "selector": { "text": }, "description": "Name of the user", "required": "True" } } }, "age": { "selector": { "number": }, "description": "Age of the user" } }"""
        ...

    @staticmethod
    def generate_image(*, task_name: str, instructions: str, entity_id: str, attachments=None) -> dict[str, Any]:
        """

        Args:
            task_name:  Example: picture of a dog
            instructions:  Example: Generate a high quality square image of a dog on transparent background"""
        ...

class alarm_control_panel:

    @staticmethod
    def alarm_disarm(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def alarm_arm_home(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def alarm_arm_away(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def alarm_arm_night(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def alarm_arm_vacation(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def alarm_arm_custom_bypass(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def alarm_trigger(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

class _assist_satellite_state(StateVal):
    restored: bool
    supported_features: int

class assist_satellite:
    a1_slwf_03_voice_assistant_assist_satellite: _assist_satellite_state

class _automation_state(StateVal):
    current: int
    id: str
    last_triggered: datetime
    mode: str
    restored: bool
    supported_features: int

    def trigger(self, skip_condition: bool):
        ...

    def toggle(self):
        ...

    def turn_on(self):
        ...

    def turn_off(self, stop_actions: bool):
        ...

class automation:
    login_failure: _automation_state
    home_assistant_stop: _automation_state
    regular_sensor_updates: _automation_state
    entity_states_notifications: _automation_state
    home_assistant_startup_actions_2: _automation_state
    audio_alerts_actualize_timer_trigger: _automation_state
    audio_alerts_announce_trigger: _automation_state
    water_leak_alert: _automation_state
    lights_on_too_long: _automation_state
    home_assistant_startup_samba_shares_mounts: _automation_state
    ac_on_pc_off_office: _automation_state
    ac_on_pc_off_room: _automation_state
    xiaomi_hub_v2_no_internet: _automation_state
    xiaomi_hub_v2_got_internet: _automation_state
    power_outage_1hour: _automation_state
    pyscript_reload_on_startup: _automation_state
    power_grey_1h: _automation_state
    power_outage_ends_in_60min: _automation_state
    power_grey_starts_in_60min: _automation_state
    power_on_off_notification: _automation_state
    water_off_in_45_minutes: _automation_state
    power_outage_starts_in: _automation_state
    water_off_in_45_minutes_2: _automation_state
    power_outage_starts_in_2: _automation_state
    water_off_in_45_minutes_3: _automation_state
    disable_pi_hole_blocking: _automation_state
    enable_pi_hole_blocking: _automation_state
    gaggiuino_heated_up_notification: _automation_state

    @staticmethod
    def trigger(*, entity_id: str, skip_condition: bool=True):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str, stop_actions: bool=True):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def reload():
        ...

class backup:

    @staticmethod
    def create_automatic():
        ...

class battery_notes:

    @staticmethod
    def set_battery_replaced(*, device_id=None, source_entity_id: str | None=None, datetime_replaced: datetime | None=None):
        """Set the battery last replaced.

        Args:
            device_id: Device that has had its battery replaced.
            source_entity_id: Entity that has had its battery replaced (only used for entity associated battery notes).
            datetime_replaced: Date replaced."""
        ...

    @staticmethod
    def check_battery_last_reported(*, days_last_reported: float):
        """Raise events for devices that haven't reported their battery level.

        Args:
            days_last_reported: Number of days since a device last reported its battery level."""
        ...

    @staticmethod
    def check_battery_low():
        """Raise events for devices that have a low battery."""
        ...

class _binary_sensor_state(StateVal):
    after: str
    alarm: bool
    attribution: str
    battery_level: int
    battery_low_threshold: int | float
    battery_quantity: int | str
    battery_type: str
    battery_type_and_quantity: str
    before: str
    days_offset: int
    device_id: str
    device_name: str
    excludes: list
    fault_code: int
    id: str
    integration: str
    next_update: str
    restored: bool
    source_entity_id: str
    state_property: str
    state_updater: str
    supported_features: int
    workdays: list

class binary_sensor:
    mi_window_and_door_sensor_magnet_sensor: _binary_sensor_state
    gateway_motion_sensor: _binary_sensor_state
    water_leak_sensor_submersion_sensor: _binary_sensor_state
    water_leak_sensor2_submersion_sensor: _binary_sensor_state
    water_leak_sensor3_submersion_sensor: _binary_sensor_state
    flood_detector_ad9d_moisture: _binary_sensor_state
    dahua_vto_dahua_button_pressed: _binary_sensor_state
    dahua_vto_dahua_invite: _binary_sensor_state
    dahua_vto_dahua_door_status: _binary_sensor_state
    dahua_vto_dahua_call_no_answered: _binary_sensor_state
    flood_detector_a948_moisture: _binary_sensor_state
    flood_detector_b134_moisture: _binary_sensor_state
    flood_detector_a1e5_moisture: _binary_sensor_state
    audio_alerts: _binary_sensor_state
    workday_sensor: _binary_sensor_state
    flood_1_miot_submersion_sensor: _binary_sensor_state
    flood_2_miot_submersion_sensor: _binary_sensor_state
    flood_3_miot_submersion_sensor: _binary_sensor_state
    flood_4_miot_submersion_sensor: _binary_sensor_state
    quiet_hours: _binary_sensor_state
    alert_is_asleep: _binary_sensor_state
    projector: _binary_sensor_state
    m_kiyiv_unknown: _binary_sensor_state
    m_kiyiv_air: _binary_sensor_state
    m_kiyiv_urban_fights: _binary_sensor_state
    m_kiyiv_artillery: _binary_sensor_state
    m_kiyiv_chemical: _binary_sensor_state
    m_kiyiv_nuclear: _binary_sensor_state
    kyiv_alarm: _binary_sensor_state
    office_window_lt_fault: _binary_sensor_state
    bedroom_window_lt_fault: _binary_sensor_state
    room_window_lt_fault: _binary_sensor_state
    kitchen_window_lt_fault: _binary_sensor_state
    someone_s_home: _binary_sensor_state
    alert_s_home: _binary_sensor_state
    catbird_s_home: _binary_sensor_state
    ping_ap_bedroom: _binary_sensor_state
    ping_ap_office: _binary_sensor_state
    ping_eight: _binary_sensor_state
    ping_one: _binary_sensor_state
    ping_router: _binary_sensor_state
    ping_sw_ubnt: _binary_sensor_state
    ping_vm_win11: _binary_sensor_state
    xiaomi_wireless_button_2_battery_low: _binary_sensor_state
    valve_kitchen_battery_low: _binary_sensor_state
    office_temphum_zb_battery_low: _binary_sensor_state
    catbird_is_asleep: _binary_sensor_state
    someone_is_asleep: _binary_sensor_state
    alert_s_s24_is_charging: _binary_sensor_state
    boiler_heating_status: _binary_sensor_state
    boiler_absence_mode: _binary_sensor_state
    boiler_boost_mode: _binary_sensor_state
    water_leak_group: _binary_sensor_state
    water_leak_zb_1_kitchen_below_battery_plus_low: _binary_sensor_state
    water_leak_zb_2_kitchen_sink_closest_battery_plus_low: _binary_sensor_state
    water_leak_zb_4_laundry_washing_machine_battery_plus_low: _binary_sensor_state
    water_leak_zb_3_laundry_water_filter_battery_plus_low: _binary_sensor_state
    room_window_reed_battery_plus_low: _binary_sensor_state
    zigbee2mqtt_bridge_connection_state_2: _binary_sensor_state
    reed_wardrobe_battery_plus_low: _binary_sensor_state
    valve_kitchen_valve_state: _binary_sensor_state
    valve_kitchen_window: _binary_sensor_state
    zigbee2mqtt_bridge_connection_state_4: _binary_sensor_state
    reed_wardrobe_contact: _binary_sensor_state
    water_leak_zb_4_water_leak: _binary_sensor_state
    water_leak_zb_4_battery_low: _binary_sensor_state
    water_leak_zb_3_water_leak: _binary_sensor_state
    water_leak_zb_3_battery_low: _binary_sensor_state
    water_leak_zb_1_water_leak: _binary_sensor_state
    water_leak_zb_1_battery_low: _binary_sensor_state
    iphone_kateryna_focus: _binary_sensor_state
    electricity_discount_period: _binary_sensor_state
    ping_boiler: _binary_sensor_state
    ping_alert_server: _binary_sensor_state
    power: _binary_sensor_state
    room_window_reed_contact: _binary_sensor_state
    room_window_reed_battery_low: _binary_sensor_state
    bathroom_temphum_battery_plus_low: _binary_sensor_state
    shower_temphum_battery_plus_low: _binary_sensor_state
    temperature_humidity_sensor_ce25_battery_plus_low: _binary_sensor_state
    laundry_mi_battery_plus_low: _binary_sensor_state
    mi_kitchen_battery_plus_low: _binary_sensor_state
    internet: _binary_sensor_state
    slzb_06p10: _binary_sensor_state
    zigbee2mqtt_slzb_running: _binary_sensor_state
    iphone_kateryna_battery_plus_low: _binary_sensor_state
    door: _binary_sensor_state
    remote_ui: _binary_sensor_state
    boiler_manual_mode: _binary_sensor_state
    lolin32_lite_220_5v_presence: _binary_sensor_state
    xiaomi_wireless_button_1_battery_plus_low: _binary_sensor_state
    temperature_humidity_sensor_7360_battery_plus_low: _binary_sensor_state
    power_outage: _binary_sensor_state
    office_ac_ping: _binary_sensor_state
    room_ac_ping: _binary_sensor_state
    becroom_ac_ping: _binary_sensor_state
    kitchen_ac_ping: _binary_sensor_state
    quest3_is_charging: _binary_sensor_state
    quest3_device_locked: _binary_sensor_state
    quest3_device_secure: _binary_sensor_state
    quest3_wifi_state: _binary_sensor_state
    quest3_power_save: _binary_sensor_state
    quest3_in_use: _binary_sensor_state
    quest3_battery_plus_low: _binary_sensor_state
    slzb_06p10_ethernet: _binary_sensor_state
    slzb_06p10_wi_fi: _binary_sensor_state
    slzb_06p10_internet: _binary_sensor_state
    vacuum_service: _binary_sensor_state
    valve_office_window_open: _binary_sensor_state
    valve_office_battery_low: _binary_sensor_state
    valve_room_window_open: _binary_sensor_state
    valve_room_battery_low: _binary_sensor_state
    valve_bedroom_window_open: _binary_sensor_state
    valve_bedroom_battery_low: _binary_sensor_state
    flood_detector_a1e5_battery_plus_low: _binary_sensor_state
    flood_detector_a948_battery_plus_low: _binary_sensor_state
    flood_detector_ad9d_battery_plus_low: _binary_sensor_state
    flood_detector_b134_battery_plus_low: _binary_sensor_state
    motion_cat_toilet_presence: _binary_sensor_state
    motion_cat_toilet_battery_plus_low: _binary_sensor_state
    orbitrack_tl_problem: _binary_sensor_state
    valve_bedroom_battery_plus_low: _binary_sensor_state
    valve_office_battery_plus_low: _binary_sensor_state
    valve_room_battery_plus_low: _binary_sensor_state
    qp_bedroom_bt_8c0c_battery_plus_low: _binary_sensor_state
    qp_office_bt_battery_plus_low: _binary_sensor_state
    motion_office_cat_battery_plus_low: _binary_sensor_state
    reed_office_cabinet_contact: _binary_sensor_state
    reed_office_cabinet_tamper: _binary_sensor_state
    reed_office_cabinet_battery_low: _binary_sensor_state
    reed_office_cabinet_battery_plus_low: _binary_sensor_state
    alert_s_redmi_pad_pro_is_charging: _binary_sensor_state
    alert_s_redmi_pad_pro_wi_fi_state: _binary_sensor_state
    music_assistant_server_running: _binary_sensor_state
    ping_alert_mob: _binary_sensor_state
    ping_catbird_mob: _binary_sensor_state
    ping_catbird_watch: _binary_sensor_state
    grocy_overdue_chores: _binary_sensor_state
    grocy_overdue_tasks: _binary_sensor_state
    washer_child_lock: _binary_sensor_state
    washer_remote_control: _binary_sensor_state
    washer_power: _binary_sensor_state
    telegram_client_alertua_restricted: _binary_sensor_state
    telegram_client_alertua_premium: _binary_sensor_state
    reed_hallway_closet_right_contact: _binary_sensor_state
    reed_hallway_closet_right_tamper: _binary_sensor_state
    reed_hallway_closet_right_battery_low: _binary_sensor_state
    reed_hallway_closet_right_battery_plus_low: _binary_sensor_state
    energy_monitoring_smartplug_problem: _binary_sensor_state
    gaggiuino_availability: _binary_sensor_state
    gaggiuino_brew_switch: _binary_sensor_state
    gaggiuino_steam_switch: _binary_sensor_state
    wine_fridge_temphum_power: _binary_sensor_state
    wine_fridge_temphum_opening: _binary_sensor_state
    wine_fridge_temphum_battery_plus_low: _binary_sensor_state
    a1_slwf_03_voice_assistant_voice: _binary_sensor_state
    pi_hole_status: _binary_sensor_state
    alert_s_s24_battery_plus_low: _binary_sensor_state
    office_vitamins_temphum_battery_plus_low: _binary_sensor_state
    co2_temp_rh_2cf6_battery_plus_low: _binary_sensor_state
    lumi_cn_blt_3_15uta0cjolo00_bmcn01_submersion_state_p_2_1: _binary_sensor_state
    lumi_cn_blt_3_15utbdl8clk00_bmcn01_submersion_state_p_2_1: _binary_sensor_state
    lumi_cn_blt_3_15utcieasec00_bmcn01_submersion_state_p_2_1: _binary_sensor_state
    lumi_cn_blt_3_15utcv1agec00_bmcn01_submersion_state_p_2_1: _binary_sensor_state
    bedroom_window_reed_contact: _binary_sensor_state
    bedroom_window_reed_tamper: _binary_sensor_state
    bedroom_window_reed_battery_low: _binary_sensor_state
    motion_office_sun_presence: _binary_sensor_state
    bedroom_window_reed_battery_plus_low_2: _binary_sensor_state
    everybody_asleep: _binary_sensor_state
    ghcr_io: _binary_sensor_state
    water_leak_laundry_washing_machine_battery_low: _binary_sensor_state
    water_leak_laundry_washing_machine_occupancy: _binary_sensor_state
    water_leak_laundry_washing_machine_battery_plus_low: _binary_sensor_state
    water_leak_zb_2_water_leak: _binary_sensor_state
    water_leak_zb_2_battery_low: _binary_sensor_state
    office_motion_cat_mat_presence: _binary_sensor_state
    office_motion_cat_mat_battery_plus_low: _binary_sensor_state
    delta_pro_estimated_discharge_ok: _binary_sensor_state

class blueprint:
    ...

class _button_state(StateVal):
    alarm: int | bool
    app_link: str
    available: bool
    battery_level: int
    converters: list
    customizes: dict
    did: str
    home_room: str
    info: Any
    lan_ip: str
    mac: str
    miot_type: str
    model: str
    restored: bool
    state_property: str
    state_updater: str
    supported_features: int
    updated_at: str
    updater: str

    def press(self):
        ...

class button:
    u6_lite_restart: _button_state
    usw_flex_mini_restart: _button_state
    u6_pro_restart: _button_state
    office_window_lt_upper_limit_reset: _button_state
    office_window_lt_intermediate_limit_reset: _button_state
    office_window_lt_lower_limit_reset: _button_state
    office_window_lt_remote_pairing: _button_state
    office_window_lt_all_limits_reset: _button_state
    bedroom_window_lt_upper_limit_reset: _button_state
    bedroom_window_lt_intermediate_limit_reset: _button_state
    bedroom_window_lt_lower_limit_reset: _button_state
    bedroom_window_lt_remote_pairing: _button_state
    bedroom_window_lt_all_limits_reset: _button_state
    room_window_lt_upper_limit_reset: _button_state
    room_window_lt_intermediate_limit_reset: _button_state
    room_window_lt_lower_limit_reset: _button_state
    room_window_lt_remote_pairing: _button_state
    room_window_lt_all_limits_reset: _button_state
    kitchen_window_lt_upper_limit_reset: _button_state
    kitchen_window_lt_intermediate_limit_reset: _button_state
    kitchen_window_lt_lower_limit_reset: _button_state
    kitchen_window_lt_remote_pairing: _button_state
    kitchen_window_lt_all_limits_reset: _button_state
    xiaomi_wireless_button_1_battery_replaced: _button_state
    xiaomi_wireless_button_2_battery_replaced: _button_state
    water_leak_sensor_battery_replaced: _button_state
    water_leak_sensor_battery_replaced_2: _button_state
    water_leak_sensor_battery_replaced_3: _button_state
    valve_kitchen_battery_replaced: _button_state
    valve_bedroom_battery_replaced: _button_state
    valve_office_battery_replaced: _button_state
    valve_room_battery_replaced: _button_state
    google_assistant_synchronize_devices: _button_state
    homeassistant_restart: _button_state
    homeassistant_reload: _button_state
    ignore_all_issues: _button_state
    unignore_all_issues: _button_state
    water_leak_zb_1_kitchen_below_battery_replaced: _button_state
    water_leak_zb_2_kitchen_sink_closest_battery_replaced: _button_state
    water_leak_zb_4_laundry_washing_machine_battery_replaced: _button_state
    water_leak_zb_3_laundry_water_filter_battery_replaced: _button_state
    room_window_reed_battery_replaced: _button_state
    reed_wardrobe_battery_replaced: _button_state
    zigbee2mqtt_bridge_restart_2: _button_state
    ikea_tradfri_identify: _button_state
    iphone_kateryna_battery_replaced: _button_state
    bathroom_temphum_battery_replaced: _button_state
    shower_temphum_battery_replaced: _button_state
    temperature_humidity_sensor_ce25_battery_replaced: _button_state
    laundry_mi_battery_replaced: _button_state
    mi_kitchen_battery_replaced: _button_state
    usw_lite_16_poe_port_1_power_cycle: _button_state
    usw_lite_16_poe_port_2_power_cycle: _button_state
    usw_lite_16_poe_port_3_power_cycle: _button_state
    usw_lite_16_poe_port_4_power_cycle: _button_state
    usw_lite_16_poe_port_5_power_cycle: _button_state
    usw_lite_16_poe_port_6_power_cycle: _button_state
    usw_lite_16_poe_port_7_power_cycle: _button_state
    usw_lite_16_poe_port_8_power_cycle: _button_state
    usw_lite_16_poe_restart: _button_state
    temperature_humidity_sensor_7360_battery_replaced: _button_state
    quest3_battery_replaced: _button_state
    ijai_v3_4619_info: _button_state
    lumi_v3_0661_info: _button_state
    cleargrass_dk1_3904_info: _button_state
    cleargrass_dk1_3c69_info: _button_state
    lumi_bmcn01_ad9d_info: _button_state
    lumi_bmcn01_a1e5_info: _button_state
    lumi_bmcn01_b134_info: _button_state
    lumi_bmcn01_a948_info: _button_state
    miaomiaoce_t2_b99d_info: _button_state
    miaomiaoce_t2_ce25_info: _button_state
    miaomiaoce_t2_7360_info: _button_state
    miaomiaoce_t2_b5ef_info: _button_state
    slzb_06p10_core_restart: _button_state
    slzb_06p10_zigbee_restart: _button_state
    ijai_de_1027836802_v3_start_only_sweep_a_2_3: _button_state
    ijai_de_1027836802_v3_start_sweep_mop_a_2_5: _button_state
    ijai_de_1027836802_v3_start_mop_a_2_6: _button_state
    ijai_de_1027836802_v3_start_charge_a_3_1: _button_state
    ijai_de_1027836802_v3_set_calibration_a_7_2: _button_state
    ijai_de_1027836802_v3_get_a_8_3: _button_state
    ijai_de_1027836802_v3_start_point_clean_a_9_1: _button_state
    ijai_de_1027836802_v3_start_zone_clean_a_9_3: _button_state
    ijai_de_1027836802_v3_get_map_list_a_10_1: _button_state
    ijai_de_1027836802_v3_reset_map_a_10_10: _button_state
    ijai_de_1027836802_v3_reset_map_ii_a_10_16: _button_state
    ijai_de_1027836802_v3_get_download_status_a_14_2: _button_state
    ijai_v3_4619_start_sweep: _button_state
    ijai_v3_4619_stop_sweeping: _button_state
    ijai_v3_4619_start_only_sweep: _button_state
    ijai_v3_4619_start_sweep_mop: _button_state
    ijai_v3_4619_start_mop: _button_state
    ijai_v3_4619_start_charge: _button_state
    flood_detector_a1e5_battery_replaced: _button_state
    flood_detector_a948_battery_replaced: _button_state
    flood_detector_ad9d_battery_replaced: _button_state
    flood_detector_b134_battery_replaced: _button_state
    motion_cat_toilet_battery_replaced: _button_state
    wol_beelink_wifi: _button_state
    wol_alert_server_eth1: _button_state
    wol_alert_server: _button_state
    wol_beelink_lan: _button_state
    wol_mini_eth0: _button_state
    wol_mini_eth1: _button_state
    qp_bedroom_bt_8c0c_battery_replaced: _button_state
    qp_office_bt_battery_replaced: _button_state
    motion_office_cat_battery_replaced: _button_state
    reed_office_cabinet_battery_replaced_2: _button_state
    ijai_v3_4619_reset_consumable: _button_state
    ijai_v3_4619_reset_map: _button_state
    ijai_v3_4619_reset_map_ii: _button_state
    reed_hallway_closet_right_battery_replaced: _button_state
    wine_fridge_temphum_battery_replaced: _button_state
    a1_slwf_03_voice_assistant_factory_reset: _button_state
    alert_s_s24_battery_replaced: _button_state
    office_vitamins_temphum_battery_replaced: _button_state
    co2_temp_rh_2cf6_battery_replaced: _button_state
    mijia_de_56078868_v1_stop_stream_a_3_2: _button_state
    mijia_de_56078868_v1_get_stream_configuration_a_3_3: _button_state
    mijia_de_56078868_v1_stop_stream_a_4_2: _button_state
    mijia_de_56078868_v1_start_p2p_stream_a_5_1: _button_state
    mijia_de_56078868_v1_stop_stream_a_5_2: _button_state
    mijia_de_56078868_v1_format_a_6_1: _button_state
    mijia_de_56078868_v1_pop_up_a_6_2: _button_state
    u7_pro_restart: _button_state
    bedroom_window_reed_battery_replaced_2: _button_state
    water_leak_laundry_washing_machine_battery_replaced: _button_state
    lolin32lite220_restart_device: _button_state
    nestaudio0831_favorite_current_song: _button_state
    bedroom_speaker_favorite_current_song: _button_state
    nestaudio9023_favorite_current_song: _button_state
    music_speakers_favorite_current_song: _button_state
    all_favorite_current_song: _button_state
    kitchen_speaker_favorite_current_song: _button_state
    nestmini8659_favorite_current_song: _button_state
    bathroom_speaker_favorite_current_song: _button_state
    broadcast_favorite_current_song: _button_state
    relax_favorite_current_song: _button_state
    all_speakers_favorite_current_song: _button_state
    room_audio_favorite_current_song: _button_state
    shower_speaker_favorite_current_song: _button_state
    mini_favorite_current_song: _button_state
    socket_random_cloud_reset_consumption: _button_state
    delta_2_plug_reset_consumption: _button_state
    laundry_optional_reset_consumption: _button_state
    smart_energy_meter_at2pl_gr2p_reset_consumption: _button_state
    orbitrack_reset_consumption: _button_state
    projector_custom_register_new_ir_key: _button_state
    projector_custom_on: _button_state
    projector_custom_off: _button_state
    kitchen_vents_register_new_ir_key: _button_state
    kitchen_vents: _button_state
    kitchen_vents_2: _button_state
    kitchen_vents_light: _button_state
    kitchen_vents_on_off: _button_state
    office_motion_cat_mat_battery_replaced: _button_state
    projector_register_new_ir_key: _button_state
    projector_power: _button_state
    projector_mode: _button_state
    projector_ok: _button_state
    projector_menu: _button_state
    projector_navigate_up: _button_state
    projector_navigate_down: _button_state
    projector_navigate_left: _button_state
    projector_navigate_right: _button_state
    projector_volume_up: _button_state
    projector_volume_down: _button_state
    projector_mute: _button_state
    projector_input: _button_state
    projector_back: _button_state
    projector_exit: _button_state
    projector_play: _button_state
    projector_pause: _button_state
    projector_page_up: _button_state
    projector_page_down: _button_state
    projector_info: _button_state
    projector_freeze: _button_state
    projector_auto: _button_state
    projector_help: _button_state
    projector_digital_zoom: _button_state
    projector_digital_zoom_2: _button_state
    projector_teaching_template: _button_state
    projector_3d_settings: _button_state
    projector_quick_install: _button_state
    projector_smart_eco: _button_state
    projector_blank: _button_state
    projector_zoom_up: _button_state
    projector_zoom_down: _button_state
    projector_aspect: _button_state
    projector_auto_sync: _button_state
    projector_capture: _button_state
    projector_keystone: _button_state
    projector_keystone_2: _button_state
    projector_menu_lock: _button_state
    projector_timer_on: _button_state
    projector_timer_set_up: _button_state
    projector_source: _button_state
    projector_power_on: _button_state
    projector_power_off: _button_state
    bw_rc1_add_ir_device: _button_state

    @staticmethod
    def press(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class _calendar_state(StateVal):
    all_day: bool
    description: str
    end_time: str
    location: str
    message: str
    start_time: str

    def create_event(self, *, summary: str, description: str | None=None, start_date_time: datetime | None=None, end_date_time: datetime | None=None, start_date: datetime | None=None, end_date: datetime | None=None, location: str | None=None):
        """

        Args:
            summary:  Example: Department Party
            description:  Example: Meeting to provide technical review for 'Phoenix' design.
            start_date_time:  Example: 2022-03-22 20:00:00
            end_date_time:  Example: 2022-03-22 22:00:00
            start_date:  Example: 2022-03-22
            end_date:  Example: 2022-03-23
            location:  Example: Conference Room - F123, Bldg. 002"""
        ...

    def get_events(self, *, start_date_time: datetime | None=None, end_date_time: datetime | None=None, duration=None) -> dict[str, Any]:
        """

        Args:
            start_date_time:  Example: 2022-03-22 20:00:00
            end_date_time:  Example: 2022-03-22 22:00:00"""
        ...

class calendar:
    workday_sensor_calendar: _calendar_state
    kiiv_dtek_3_1_planned_outages: _calendar_state

    @staticmethod
    def create_event(*, entity_id: str, summary: str, description: str | None=None, start_date_time: datetime | None=None, end_date_time: datetime | None=None, start_date: datetime | None=None, end_date: datetime | None=None, location: str | None=None):
        """

        Args:
            entity_id: Entity ID
            summary:  Example: Department Party
            description:  Example: Meeting to provide technical review for 'Phoenix' design.
            start_date_time:  Example: 2022-03-22 20:00:00
            end_date_time:  Example: 2022-03-22 22:00:00
            start_date:  Example: 2022-03-22
            end_date:  Example: 2022-03-23
            location:  Example: Conference Room - F123, Bldg. 002"""
        ...

    @staticmethod
    def get_events(*, entity_id: str, start_date_time: datetime | None=None, end_date_time: datetime | None=None, duration=None) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID
            start_date_time:  Example: 2022-03-22 20:00:00
            end_date_time:  Example: 2022-03-22 22:00:00"""
        ...

class _camera_state(StateVal):
    access_token: str
    entity_picture: str
    id: str
    integration: str
    supported_features: int

    def enable_motion_detection(self):
        ...

    def disable_motion_detection(self):
        ...

    def turn_off(self):
        ...

    def turn_on(self):
        ...

    def snapshot(self, filename: str):
        """

        Args:
            filename:  Example: /tmp/snapshot_{{ entity_id.name }}.jpg"""
        ...

    def play_stream(self, *, media_player: str, format: Literal['', 'hls']='hls'):
        ...

    def record(self, *, filename: str, duration: int=30, lookback: int=0):
        """

        Args:
            filename:  Example: /tmp/snapshot_{{ entity_id.name }}.mp4"""
        ...

class camera:
    dahua_vto_dahua_main: _camera_state
    dahua_vto_dahua_sub: _camera_state

    @staticmethod
    def enable_motion_detection(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def disable_motion_detection(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def snapshot(*, entity_id: str, filename: str):
        """

        Args:
            entity_id: Entity ID
            filename:  Example: /tmp/snapshot_{{ entity_id.name }}.jpg"""
        ...

    @staticmethod
    def play_stream(*, entity_id: str, media_player: str, format: Literal['', 'hls']='hls'):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def record(*, entity_id: str, filename: str, duration: int=30, lookback: int=0):
        """

        Args:
            entity_id: Entity ID
            filename:  Example: /tmp/snapshot_{{ entity_id.name }}.mp4"""
        ...

class _climate_state(StateVal):
    current_temperature: float
    hvac_action: str
    hvac_modes: list
    max_temp: float
    min_temp: float
    preset_mode: str
    preset_modes: list
    restored: bool
    supported_features: int
    target_temp_step: float
    temperature: float

    def turn_on(self):
        ...

    def turn_off(self):
        ...

    def toggle(self):
        ...

    def set_hvac_mode(self, hvac_mode: str | None):
        ...

    def set_preset_mode(self, preset_mode: str):
        """

        Args:
            preset_mode:  Example: away"""
        ...

    def set_temperature(self, *, temperature: float | None=None, target_temp_high: float | None=None, target_temp_low: float | None=None, hvac_mode: Literal['', 'off', 'auto', 'cool', 'dry', 'fan_only', 'heat_cool', 'heat'] | None=None):
        ...

    def set_humidity(self, humidity: int):
        ...

    def set_fan_mode(self, fan_mode: str):
        """

        Args:
            fan_mode:  Example: low"""
        ...

    def set_swing_mode(self, swing_mode: str):
        """

        Args:
            swing_mode:  Example: on"""
        ...

    def set_swing_horizontal_mode(self, swing_horizontal_mode: str):
        """

        Args:
            swing_horizontal_mode:  Example: on"""
        ...

class climate:
    shower_floor: _climate_state
    valve_kitchen: _climate_state
    valve_office: _climate_state
    valve_room: _climate_state
    valve_bedroom: _climate_state
    bathroom_floor_cl: _climate_state

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_hvac_mode(*, entity_id: str, hvac_mode: str | None=None):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_preset_mode(*, entity_id: str, preset_mode: str):
        """

        Args:
            entity_id: Entity ID
            preset_mode:  Example: away"""
        ...

    @staticmethod
    def set_temperature(*, entity_id: str, temperature: float | None=None, target_temp_high: float | None=None, target_temp_low: float | None=None, hvac_mode: Literal['', 'off', 'auto', 'cool', 'dry', 'fan_only', 'heat_cool', 'heat'] | None=None):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_humidity(*, entity_id: str, humidity: int):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_fan_mode(*, entity_id: str, fan_mode: str):
        """

        Args:
            entity_id: Entity ID
            fan_mode:  Example: low"""
        ...

    @staticmethod
    def set_swing_mode(*, entity_id: str, swing_mode: str):
        """

        Args:
            entity_id: Entity ID
            swing_mode:  Example: on"""
        ...

    @staticmethod
    def set_swing_horizontal_mode(*, entity_id: str, swing_horizontal_mode: str):
        """

        Args:
            entity_id: Entity ID
            swing_horizontal_mode:  Example: on"""
        ...

class cloud:

    @staticmethod
    def remote_connect():
        ...

    @staticmethod
    def remote_disconnect():
        ...

class command_line:

    @staticmethod
    def reload():
        ...

class _conversation_state(StateVal):
    supported_features: int

class conversation:
    google_ai_conversation: _conversation_state

    @staticmethod
    def process(*, text: str, language: str | None=None, agent_id=None, conversation_id: str | None=None) -> dict[str, Any]:
        """

        Args:
            text:  Example: Turn all lights on
            language:  Example: NL
            agent_id:  Example: homeassistant
            conversation_id:  Example: my_conversation_1"""
        ...

    @staticmethod
    def reload(*, language: str | None=None, agent_id=None):
        """

        Args:
            language:  Example: NL
            agent_id:  Example: homeassistant"""
        ...

class counter:

    @staticmethod
    def increment(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def decrement(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def reset(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_value(*, entity_id: str, value: float):
        """

        Args:
            entity_id: Entity ID"""
        ...

class _cover_state(StateVal):
    current_position: int
    supported_features: int
    unreliable_action: Any

    def open_cover(self):
        ...

    def close_cover(self):
        ...

    def set_cover_position(self, position: int):
        ...

    def stop_cover(self):
        ...

    def toggle(self):
        ...

    def open_cover_tilt(self):
        ...

    def close_cover_tilt(self):
        ...

    def stop_cover_tilt(self):
        ...

    def set_cover_tilt_position(self, tilt_position: int):
        ...

    def toggle_cover_tilt(self):
        ...

class cover:
    kitchen_window_tl: _cover_state
    bedroom_window_tl: _cover_state
    office_window_tl: _cover_state
    room_window_tl: _cover_state
    office_window_cloud_curtain: _cover_state
    room_window_cloud_curtain: _cover_state
    bedroom_window_cloud_curtain: _cover_state
    kitchen_window_cloud_curtain: _cover_state

    @staticmethod
    def open_cover(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def close_cover(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_cover_position(*, entity_id: str, position: int):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def stop_cover(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def open_cover_tilt(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def close_cover_tilt(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def stop_cover_tilt(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_cover_tilt_position(*, entity_id: str, tilt_position: int):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle_cover_tilt(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class dahua:

    @staticmethod
    def set_video_profile_mode(*, entity_id: str, mode: Literal['', 'Day', 'Night'] | None=None):
        """Sets the video profile mode to day or night

        Args:
            entity_id: Entity ID
            mode: The profile: Day, Night Example: Day"""
        ...

    @staticmethod
    def set_focus_zoom(*, entity_id: str, focus: str='0.758333', zoom: str='0.898502'):
        """Sets the camera's focus and zoom

        Args:
            entity_id: Entity ID
            focus: Decimal Value for Focus Example: 0.758333
            zoom: Decimal value for zoom Example: 0.898502"""
        ...

    @staticmethod
    def set_privacy_masking(*, entity_id: str, index: float=0, enabled: bool=True):
        """Enables or disabled the cameras privacy masking

        Args:
            entity_id: Entity ID
            index: The mask index. 0 is the first mask
            enabled: If true enables the mask, otherwise disables it Example: True"""
        ...

    @staticmethod
    def enable_channel_title(*, entity_id: str, enabled: bool=True):
        """Enables or disable the channel title video overaly

        Args:
            entity_id: Entity ID
            enabled: If the overlay is enabled or not Example: True"""
        ...

    @staticmethod
    def enable_time_overlay(*, entity_id: str, enabled: bool=True):
        """Enables or disable the channel time video overaly

        Args:
            entity_id: Entity ID
            enabled: If the overlay is enabled or not Example: True"""
        ...

    @staticmethod
    def enable_text_overlay(*, entity_id: str, group: float=1, enabled: bool=False):
        """Enables or disable the channel text video overaly

        Args:
            entity_id: Entity ID
            group: Multiple text overlay groups can exist. The default 1 should be used in most cases Example: 1
            enabled: If the overlay is enabled or not Example: True"""
        ...

    @staticmethod
    def enable_custom_overlay(*, entity_id: str, group: float=0, enabled: bool=False):
        """Enables or disable the channel custom text video overaly

        Args:
            entity_id: Entity ID
            group: Multiple custom text groups can exist. The default 0 should be used in most cases
            enabled: If the overlay is enabled or not Example: True"""
        ...

    @staticmethod
    def enable_all_ivs_rules(*, entity_id: str, enabled: bool=True):
        """Enables of disables all IVS rules based on the supplied 'enabled' param

        Args:
            entity_id: Entity ID
            enabled: If true all IVS rules are enabled. If false, all are disabled Example: True"""
        ...

    @staticmethod
    def enable_ivs_rule(*, entity_id: str, index: float=1, enabled: bool=True):
        """Enables of disable a single IVS rule based on the supplied 'enabled' param

        Args:
            entity_id: Entity ID
            index: The rule index. 0 is a hidden rule, so usually the first rule is rule 1 Example: 1
            enabled: If true enables the IVS rule, otherwise disables it Example: True"""
        ...

    @staticmethod
    def vto_open_door(*, entity_id: str, door_id: float=1):
        """Open a door via a VTO (Doorbell) for supported devices

        Args:
            entity_id: Entity ID
            door_id: The door ID. Default is 1 Example: 1"""
        ...

    @staticmethod
    def vto_cancel_call(*, entity_id: str):
        """Cancels a VTO call

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_channel_title(*, entity_id: str, text1: str='', text2: str=''):
        """Sets a title on the video

        Args:
            entity_id: Entity ID
            text1: The first title Example: Front Porch
            text2: The second title Example: House"""
        ...

    @staticmethod
    def set_text_overlay(*, entity_id: str, group: float=1, text1: str='', text2: str='', text3: str='', text4: str=''):
        """Sets a text overlay on the video

        Args:
            entity_id: Entity ID
            group: Multiple custom text groups can exist. The default 1 should be used in most cases Example: 1
            text1: Text overlay 1 Example: Text 1
            text2: Text overlay 2 Example: Text 2
            text3: Text overlay 3 Example: Text 3
            text4: Text overlay 4 Example: Text 4"""
        ...

    @staticmethod
    def set_custom_overlay(*, entity_id: str, group: float=0, text1: str='', text2: str=''):
        """Sets a custom text overlay on the video

        Args:
            entity_id: Entity ID
            group: Multiple custom text groups can exist. The default 0 should be used in most cases
            text1: Custom overlay 1 Example: Text 1
            text2: Custom overlay 2 Example: Text 2"""
        ...

    @staticmethod
    def set_video_in_day_night_mode(*, entity_id: str, config_type: Literal['', 'general', 'day', 'night']='general', mode: Literal['', 'Auto', 'Color', 'BlackWhite']='Auto'):
        """Set the camera's Day/Night Mode. For example, Color, BlackWhite, or Auto

        Args:
            entity_id: Entity ID
            config_type: The config type: general, day, night Example: general
            mode: The mode: Auto, Color, BlackWhite. Note Auto is also known as Brightness by Dahua Example: Auto"""
        ...

    @staticmethod
    def reboot(*, entity_id: str):
        """Reboots the device

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_record_mode(*, entity_id: str, mode: Literal['', 'Auto', 'On', 'Off']='Auto'):
        """Sets the record mode (on/off or auto). On is always on recording. Off is always off. Auto based on motion settings, etc.

        Args:
            entity_id: Entity ID
            mode: The mode: Auto, On, Off Example: Auto"""
        ...

    @staticmethod
    def set_infrared_mode(*, entity_id: str, mode: Literal['', 'Auto', 'On', 'Off']='Auto', brightness: int=100):
        """Set the infrared light settings on a Dahua camera

        Args:
            entity_id: Entity ID
            mode: The infrared mode: Auto, On, Off Example: Auto
            brightness: The infrared brightness, from 0 to 100 inclusive. 100 is the brightest Example: 100"""
        ...

    @staticmethod
    def goto_preset_position(*, entity_id: str, position: float=1):
        """Go to a position already preset

        Args:
            entity_id: Entity ID
            position: Position number, from 1 to 10 inclusive. Example: 1"""
        ...

class dahua_vto:

    @staticmethod
    def send_command(*, entity_id: str, method: Any, params: Any | None=None, event: bool=True, tag: Any | None=None, timeout: int=5):
        """Send the command

        Args:
            entity_id: Entity ID of the Dahua VTO sensor Example: sensor.dahua_vto
            method: Method name, example: magicBox.getBootParameter Example: system.listService
            params: Method parameters, example: {names: ['serverip', 'ver']} Example: {names: ['serverip', 'ver']}
            event: Fire event with result Example: True
            tag: Tag, will be present in event data, example: 1 or {name: tag} Example: {name: tag}
            timeout: Command execution timeout Example: 5"""
        ...

    @staticmethod
    def send_instance_command(*, entity_id: str, method: Any, params: Any | None=None, event: bool=True, tag: Any | None=None, timeout: int=5, instance_params: Any | None=None):
        """Send the command to the instance, sequential call to service.factory.instance, service.method with object returned by factory.instance, service.destroy

        Args:
            entity_id: Entity ID of the Dahua VTO sensor Example: sensor.dahua_vto
            method: Method name, example: magicBox.getBootParameter Example: system.listService
            params: Method parameters, example: {names: ['serverip', 'ver']} Example: {names: ['serverip', 'ver']}
            event: Fire event with result Example: True
            tag: Tag, will be present in event data, example: 1 or {name: tag} Example: {name: tag}
            timeout: Command execution timeout Example: 5
            instance_params: Instance method parameters, for service.factory.instance call, example: {'name': 'VideoTalkMissedLog'} Example: {'name': 'VideoTalkMissedLog'}"""
        ...

    @staticmethod
    def open_door(*, entity_id: str, channel: int, timeout: int=5, short_number: str='HA'):
        """Open the door

        Args:
            entity_id: Entity ID of the Dahua VTO sensor Example: sensor.dahua_vto
            channel: Number of channel starting from 1 Example: 1
            timeout: Command execution timeout Example: 5
            short_number: Short number to show in the log as Room No. Example: HA"""
        ...

class _device_tracker_state(StateVal):
    _is_guest_by_uap: bool
    altitude: int | float
    ap_mac: str
    authorized: bool
    battery_level: int
    course: int
    essid: str
    gps_accuracy: int
    host_name: str
    ip: str
    is_11r: bool
    is_guest: bool
    latitude: float
    longitude: float
    mac: str
    major: int
    minor: int
    name: str
    note: str
    oui: str
    qos_policy_applied: bool
    radio: str
    radio_proto: str
    restored: bool
    source: str
    source_type: str
    speed: int
    supported_features: int
    uuid: str
    vertical_accuracy: int

class device_tracker:
    esp_e6b3a7: _device_tracker_state
    speaker_kitchen: _device_tracker_state
    esp_8c6957: _device_tracker_state
    unifi_10_d5_61_16_51_7b_default: _device_tracker_state
    thermostat_shower: _device_tracker_state
    bathroom_speaker: _device_tracker_state
    qingping_air_monitor: _device_tracker_state
    esp_fa9672: _device_tracker_state
    speaker_shower: _device_tracker_state
    speaker_office: _device_tracker_state
    esp_3297d5: _device_tracker_state
    speaker_bedroom: _device_tracker_state
    esp_2918bd: _device_tracker_state
    ty_wr: _device_tracker_state
    thermostat_bathroom: _device_tracker_state
    speaker_room: _device_tracker_state
    humidifier_office: _device_tracker_state
    esp_35fc9f: _device_tracker_state
    meizu_m2_note: _device_tracker_state
    esp_bfacaa: _device_tracker_state
    esp_c0a4cb: _device_tracker_state
    esp_ea781a: _device_tracker_state
    esp_350556: _device_tracker_state
    esp_fa04dd: _device_tracker_state
    ty_wr_2: _device_tracker_state
    esp_fe9bc6: _device_tracker_state
    esp_e5aead: _device_tracker_state
    esp_2d2e58: _device_tracker_state
    unifi_10_d5_61_16_51_e5_default: _device_tracker_state
    speaker_hallway: _device_tracker_state
    ual6: _device_tracker_state
    uap6mp: _device_tracker_state
    esp_e6b3f7: _device_tracker_state
    oculus: _device_tracker_state
    unifi_9e_99_e4_15_ef_67_default: _device_tracker_state
    unifi_d8_ce_3a_8a_17_04_default: _device_tracker_state
    wlan0: _device_tracker_state
    catbird_laptop: _device_tracker_state
    unifi_52_c1_63_b2_8f_f5_default: _device_tracker_state
    ua1_wl_925: _device_tracker_state
    espressif: _device_tracker_state
    unifi_b0_e4_d5_c2_7d_20_default: _device_tracker_state
    unifi_ce_c7_00_eb_c5_e9_default: _device_tracker_state
    esp_c71e2a: _device_tracker_state
    washer: _device_tracker_state
    lwip_2: _device_tracker_state
    rk3308_robot32: _device_tracker_state
    unifi_a2_ef_65_10_2d_8c_default: _device_tracker_state
    unifi_60_ab_67_fb_42_cc_default: _device_tracker_state
    unifi_f4_92_bf_ad_2e_6d_default: _device_tracker_state
    usmini: _device_tracker_state
    unifi_18_e8_29_b5_51_73_default: _device_tracker_state
    unifi_52_54_00_d5_97_65_default: _device_tracker_state
    unifi_9c_5c_8e_c1_ff_55_default: _device_tracker_state
    unifi_60_63_4c_9e_6d_7a_default: _device_tracker_state
    unifi_00_e0_4c_68_06_27_default: _device_tracker_state
    unifi_b4_2e_99_34_cd_c6_default: _device_tracker_state
    unifi_b6_c2_8b_e9_3d_17_default: _device_tracker_state
    unifi_04_bf_1b_32_bd_60_default: _device_tracker_state
    unifi_40_a1_08_6a_25_77_default: _device_tracker_state
    lwip_3: _device_tracker_state
    unifi_6e_7a_aa_35_90_ed_default: _device_tracker_state
    unifi_06_bd_43_3c_d9_f2_default: _device_tracker_state
    catbird_pc: _device_tracker_state
    unifi_bc_df_58_49_a0_bc_default: _device_tracker_state
    unifi_a2_78_fe_e4_25_cf_default: _device_tracker_state
    unifi_80_f3_ef_1e_9c_5b_default: _device_tracker_state
    unifi_b6_14_84_31_fe_92_default: _device_tracker_state
    unifi_76_f0_fc_b0_f9_3f_default: _device_tracker_state
    iphone_kateryna: _device_tracker_state
    unifi_86_61_2f_6f_cb_b7_default: _device_tracker_state
    meta_quest_3: _device_tracker_state
    unifi_8a_05_6c_da_67_99_default: _device_tracker_state
    unifi_72_31_c7_eb_9d_20_default: _device_tracker_state
    unifi_da_3e_d7_d6_16_1b_default: _device_tracker_state
    unifi_82_65_f4_6d_3a_bd_default: _device_tracker_state
    unifi_c6_6d_8f_98_f3_be_default: _device_tracker_state
    wlan0_2: _device_tracker_state
    alert_legion7: _device_tracker_state
    unifi_default_5a_7d_5a_5f_0b_db: _device_tracker_state
    kitchen_tv: _device_tracker_state
    unifi_default_52_c1_63_b2_8f_f5: _device_tracker_state
    unifi_default_06_10_1a_32_cd_c9: _device_tracker_state
    meizu_m2_note_2: _device_tracker_state
    unifi_default_60_ab_67_fb_42_cc: _device_tracker_state
    qingping_co2_temp_rh: _device_tracker_state
    blitzwolf_rc1: _device_tracker_state
    unifi_default_3e_41_b7_9b_fc_fb: _device_tracker_state
    unifi_default_0a_87_86_fb_5d_c4: _device_tracker_state
    ping_ap_office: _device_tracker_state
    ping_dahua_vth: _device_tracker_state
    ping_dahua_vto: _device_tracker_state
    ping_eight: _device_tracker_state
    ping_one: _device_tracker_state
    ping_router: _device_tracker_state
    ping_sw_ubnt: _device_tracker_state
    ping_vm_win11: _device_tracker_state
    tasmota_4f2678_1656: _device_tracker_state
    unifi_default_34_ce_00_f5_7d_a5: _device_tracker_state
    tasmota_38f268_4712: _device_tracker_state
    door_1f18fc_6396: _device_tracker_state
    galaxy_s24: _device_tracker_state
    alert_s_s24: _device_tracker_state
    tasmota_56268c_7766: _device_tracker_state
    unifi_default_96_a7_8a_12_6c_b1: _device_tracker_state
    painometer_s9_3: _device_tracker_state
    unifi_default_66_41_96_02_ee_8a: _device_tracker_state
    unifi_default_36_4d_84_de_bd_38: _device_tracker_state
    unifi_default_b2_9d_d4_9e_34_36: _device_tracker_state
    desktop_074e2s7: _device_tracker_state
    unifi_default_22_d2_29_e5_99_65: _device_tracker_state
    meizu_pro_5_2: _device_tracker_state
    unifi_default_a6_32_7a_71_da_18: _device_tracker_state
    unifi_default_0e_92_95_c8_57_e1: _device_tracker_state
    unifi_default_02_6d_9f_44_c8_da: _device_tracker_state
    wled_slwf_03: _device_tracker_state
    qingping_co2_temp_rh_2: _device_tracker_state
    unifi_default_ee_72_c9_1f_f6_da: _device_tracker_state
    bt_proxy_c6_man8: _device_tracker_state
    unifi_default_02_42_c0_a8_01_05: _device_tracker_state
    unifi_default_f4_92_bf_ad_2e_6d: _device_tracker_state
    unifi_default_02_42_c0_a8_01_07: _device_tracker_state
    unifi_default_52_54_00_d5_97_65: _device_tracker_state
    unifi_default_02_47_48_39_76_0b: _device_tracker_state
    usw_lite_16_poe: _device_tracker_state
    unifi_default_60_63_4c_9e_6d_7a: _device_tracker_state
    unifi_default_04_bf_1b_32_bd_60: _device_tracker_state
    unifi_default_02_42_c0_a8_01_0a: _device_tracker_state
    unifi_default_02_42_c0_a8_01_32: _device_tracker_state
    unifi_default_02_dd_f0_24_8e_16: _device_tracker_state
    unifi_default_02_42_c0_a8_01_06: _device_tracker_state
    unifi_default_52_54_00_79_ea_27: _device_tracker_state
    unifi_default_00_e0_4c_68_06_27: _device_tracker_state
    unifi_default_08_ed_ed_6c_cb_a7: _device_tracker_state
    unifi_default_a0_bd_1d_c2_5a_c3: _device_tracker_state
    slzb_06p10: _device_tracker_state
    unifi_default_9c_2d_cd_87_74_0d: _device_tracker_state
    unifi_default_aa_a1_59_6f_32_f7: _device_tracker_state
    unifi_default_02_90_9e_9d_d7_76: _device_tracker_state
    unifi_default_02_35_9f_7c_7e_3e: _device_tracker_state
    unifi_default_f4_92_bf_ad_2e_69: _device_tracker_state
    iphone_kateryna_unifi: _device_tracker_state
    unifi_default_52_54_00_7c_7b_0d: _device_tracker_state
    unifi_default_74_5d_22_25_68_99: _device_tracker_state
    wlan0_3: _device_tracker_state
    esp32c3_85bb6c: _device_tracker_state
    boiler: _device_tracker_state
    door: _device_tracker_state
    ecoflow_delta_pro: _device_tracker_state
    ibeacon_alert_s24: _device_tracker_state
    unifi_default_16_ec_ac_8e_7f_3c: _device_tracker_state
    katerynaslaptop: _device_tracker_state
    unifi_default_4e_d1_6b_79_07_76: _device_tracker_state
    unifi_default_00_00_19_21_6a_0d: _device_tracker_state
    unifi_default_00_e0_4c_07_f1_7b: _device_tracker_state
    wlan0_4: _device_tracker_state
    s24_koristuvaca_lesa: _device_tracker_state
    unifi_default_e2_7f_5b_c6_d9_69: _device_tracker_state
    unifi_default_2a_a0_3f_e9_48_42: _device_tracker_state
    unifi_default_46_10_60_2f_10_e7: _device_tracker_state
    iphone: _device_tracker_state
    iphone_2: _device_tracker_state
    s22_koristuvaca_slowersise: _device_tracker_state
    unifi_default_7e_18_1c_38_ca_34: _device_tracker_state
    unifi_default_a2_7e_c0_e8_c8_fc: _device_tracker_state
    unifi_default_0a_cc_fa_b9_70_46: _device_tracker_state
    unifi_default_92_07_48_0d_1b_eb: _device_tracker_state
    slowersise_s_s22: _device_tracker_state
    unifi_default_84_e3_42_a7_b8_3d: _device_tracker_state
    unifi_default_52_54_00_da_3d_b2: _device_tracker_state
    unifi_default_a6_25_a1_36_33_4a: _device_tracker_state
    unifi_default_3e_eb_30_76_8b_89: _device_tracker_state
    unifi_default_b6_a6_71_cf_2c_4d: _device_tracker_state
    kitchen_ac: _device_tracker_state
    quest3: _device_tracker_state
    unifi_default_8a_15_ee_80_ab_d8: _device_tracker_state
    unifi_default_76_31_aa_4f_96_e9: _device_tracker_state
    win_5paghd9npqa: _device_tracker_state
    unifi_default_00_13_25_00_0f_f5: _device_tracker_state
    catbird_pc_2: _device_tracker_state
    unifi_default_62_05_db_8d_d6_a3: _device_tracker_state
    iphone_3: _device_tracker_state
    nest_audio: _device_tracker_state
    nest_audio_2: _device_tracker_state
    nest_audio_3: _device_tracker_state
    unifi_default_52_ac_00_74_4c_23: _device_tracker_state
    s24_koristuvaca_lesa_2: _device_tracker_state
    unifi_default_b4_2e_99_34_cd_c6: _device_tracker_state
    unifi_default_8a_66_45_9a_81_df: _device_tracker_state
    watch: _device_tracker_state
    watch_2: _device_tracker_state
    desktop_at77f7u: _device_tracker_state
    alert_server_eth1: _device_tracker_state
    alert_server_eth0: _device_tracker_state
    beelink_lan: _device_tracker_state
    mini_eth0: _device_tracker_state
    watch_3: _device_tracker_state
    iphone_4: _device_tracker_state
    unifi_default_62_04_ef_50_29_78: _device_tracker_state
    unifi_default_9c_5c_8e_c1_ff_55: _device_tracker_state
    unifi_default_02_42_c0_a8_01_a7: _device_tracker_state
    unifi_default_ba_2e_fe_1d_c8_b4: _device_tracker_state
    redmi_pad_pro: _device_tracker_state
    alert_s_redmi_pad_pro: _device_tracker_state
    katerynplewatch: _device_tracker_state
    xiaomi_11_lite_5g_ne: _device_tracker_state
    iphone_5: _device_tracker_state
    unifi_default_1a_20_fc_92_cb_88: _device_tracker_state
    watch_4: _device_tracker_state
    esp_597cfe: _device_tracker_state
    unifi_default_e4_60_17_9a_82_47: _device_tracker_state
    air_ipad: _device_tracker_state
    unifi_default_fa_a2_40_50_dc_9a: _device_tracker_state
    watch_5: _device_tracker_state
    lolin32_lite_220: _device_tracker_state
    unifi_default_78_90_9e_9d_d7_76: _device_tracker_state
    unifi_default_52_54_00_50_0b_9e: _device_tracker_state
    unifi_default_22_43_49_ea_05_bf: _device_tracker_state
    watch_6: _device_tracker_state
    unifi_default_82_e0_94_c5_96_9c: _device_tracker_state
    unifi_default_30_52_53_02_c0_d3: _device_tracker_state
    unifi_default_72_a4_f4_a4_15_ef: _device_tracker_state
    slzb_mr1: _device_tracker_state
    s2a87ff082a76aa9dc_6afc: _device_tracker_state
    watch_7: _device_tracker_state
    unifi_default_ea_41_2a_81_28_98: _device_tracker_state
    unifi_default_bc_24_11_7d_7e_ee: _device_tracker_state
    unifi_default_bc_24_11_ee_89_f1: _device_tracker_state
    watch_8: _device_tracker_state
    unifi_default_ec_71_db_35_54_1b: _device_tracker_state
    unifi_default_f4_0f_24_6f_68_04: _device_tracker_state
    unifi_default_d6_4d_74_4a_72_8d: _device_tracker_state
    unifi_default_f4_92_bf_ad_2e_68: _device_tracker_state
    unifi_default_6e_ae_f9_4c_57_3b: _device_tracker_state
    unifi_default_c0_dd_8a_49_f9_59: _device_tracker_state
    unifi_default_04_d9_f5_52_b9_f0: _device_tracker_state
    watch_9: _device_tracker_state
    esp_bbc0e7: _device_tracker_state
    unifi_default_bc_24_11_98_4f_1d: _device_tracker_state
    unifi_default_bc_24_11_cf_c3_06: _device_tracker_state
    unifi_default_c2_f1_4a_3f_3d_3e: _device_tracker_state
    unifi_default_02_42_c0_a8_01_03: _device_tracker_state
    unifi_default_02_42_c0_a8_01_04: _device_tracker_state
    watch_10: _device_tracker_state
    esp32s3_fcf280: _device_tracker_state
    esp32s3_eed1ac: _device_tracker_state
    n1u_011982: _device_tracker_state
    unifi_default_9e_a6_1c_7e_27_53: _device_tracker_state
    unifi_default_7a_7e_79_5d_9c_e3: _device_tracker_state
    unifi_default_6e_9c_ff_e2_5f_91: _device_tracker_state
    unifi_default_52_54_00_83_a9_73: _device_tracker_state
    s57c97f77153dcf28c_9cf3: _device_tracker_state
    unifi_default_0a_75_29_33_3c_09: _device_tracker_state
    unifi_default_bc_24_11_61_5c_1b: _device_tracker_state
    unifi_default_bc_24_11_64_1f_5e: _device_tracker_state
    s2ef73d665717bbfdc_e7c6: _device_tracker_state
    mi_9_se: _device_tracker_state
    unifi_default_9c_05_d6_37_84_9b: _device_tracker_state
    u7_pro: _device_tracker_state
    esp_2dcc9e: _device_tracker_state
    light_shower_led: _device_tracker_state
    unifi_default_4a_5f_00_c2_46_ed: _device_tracker_state
    unifi_default_6a_3a_85_c3_1b_cb: _device_tracker_state
    unifi_default_42_46_d4_48_81_f6: _device_tracker_state
    unifi_default_1c_4b_d6_fc_f4_ba: _device_tracker_state
    unifi_default_00_22_19_e7_d2_1f: _device_tracker_state
    unifi_default_66_0d_cc_dd_c8_fa: _device_tracker_state
    desktop_1lsst13: _device_tracker_state
    unifi_default_52_70_f2_51_bb_b5: _device_tracker_state
    unifi_default_f6_0b_44_19_3b_1e: _device_tracker_state
    watch_11: _device_tracker_state
    unifi_default_7c_92_9e_9d_d7_76: _device_tracker_state
    unifi_default_ba_5b_f8_39_41_d0: _device_tracker_state
    unifi_default_3a_bf_d4_88_cf_ce: _device_tracker_state
    unifi_default_04_8d_38_59_d2_9c: _device_tracker_state
    unifi_default_42_32_a6_fe_65_c8: _device_tracker_state
    unifi_default_a4_30_7a_8c_ba_fe: _device_tracker_state
    unifi_default_e4_fa_c4_77_7a_8c: _device_tracker_state
    unifi_default_08_10_74_00_00_01: _device_tracker_state
    unifi_default_aa_c4_b8_47_14_60: _device_tracker_state
    unifi_default_4a_fa_ee_fe_9b_a0: _device_tracker_state
    unifi_default_5a_e1_b8_ed_92_49: _device_tracker_state
    watch_12: _device_tracker_state
    sd3523776c5f01c53c_73ef: _device_tracker_state
    unifi_default_ae_58_ea_a4_ae_67: _device_tracker_state
    unifi_default_82_f5_4b_4a_fa_14: _device_tracker_state
    unifi_default_8a_77_40_83_c3_58: _device_tracker_state
    unifi_default_46_67_4c_88_72_7e: _device_tracker_state
    watch_13: _device_tracker_state
    unifi_default_3e_fc_92_7f_03_d2: _device_tracker_state
    unifi_default_00_00_00_00_00_00: _device_tracker_state

    @staticmethod
    def see(*, mac: str | None=None, dev_id: str | None=None, host_name: str | None=None, location_name: str | None=None, gps: Any | None=None, gps_accuracy: float | None=None, battery: int | None=None):
        """

        Args:
            mac:  Example: FF:FF:FF:FF:FF:FF
            dev_id:  Example: phonedave
            host_name:  Example: Dave
            location_name:  Example: home
            gps:  Example: [51.509802, -0.086692]"""
        ...

class _event_state(StateVal):
    backup_stage: Any
    bot: dict
    chat_id: int
    domain: str
    event_type: str
    event_types: list
    failed_reason: Any
    issue_id: str
    message_id: int
    timestamp: int

class event:
    repair: _event_state
    ijai_de_1027836802_v3_low_battery_e_3_1: _event_state
    ijai_de_1027836802_v3_low_battery_e_3_2: _event_state
    ijai_de_1027836802_v3_clean_end_e_7_1: _event_state
    ijai_de_1027836802_v3_clean_end_lite_e_7_2: _event_state
    ijai_de_1027836802_v3_build_end_lite_e_7_3: _event_state
    ijai_de_1027836802_v3_clean_end_ii_e_7_4: _event_state
    ijai_de_1027836802_v3_map_change_e_10_1: _event_state
    ijai_de_1027836802_v3_global_push_e_10_2: _event_state
    ijai_de_1027836802_v3_arrange_end_e_10_3: _event_state
    ijai_de_1027836802_v3_upload_verify_e_10_4: _event_state
    ijai_de_1027836802_v3_cleaning_path_e_10_5: _event_state
    ijai_de_1027836802_v3_test_upload_map_e_10_6: _event_state
    ijai_de_1027836802_v3_clear_path_e_10_7: _event_state
    backup_automatic_backup: _event_state
    sleep_as_android_sleep_tracking: _event_state
    sleep_as_android_alarm_clock: _event_state
    sleep_as_android_smart_wake_up: _event_state
    sleep_as_android_user_notification: _event_state
    sleep_as_android_sleep_phase: _event_state
    sleep_as_android_sound_recognition: _event_state
    sleep_as_android_lullaby: _event_state
    sleep_as_android_sleep_health: _event_state
    alert_ha_update_event: _event_state

class extended_openai_conversation:

    @staticmethod
    def query_image(*, config_entry: str, prompt: str, images: Any, model: str | None=None, max_tokens: float=300) -> dict[str, Any]:
        """

        Args:
            prompt:  Example: What’s in this image?
            images:  Example: {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}
            model:  Example: gpt-4-vision-preview
            max_tokens:  Example: 300"""
        ...

class _fan_state(StateVal):
    supported_features: int

    def turn_on(self, *, percentage: int | None=None, preset_mode: str | None=None):
        """

        Args:
            preset_mode:  Example: auto"""
        ...

    def turn_off(self):
        ...

    def toggle(self):
        ...

    def increase_speed(self, percentage_step: int | None):
        ...

    def decrease_speed(self, percentage_step: int | None):
        ...

    def oscillate(self, oscillating: bool):
        ...

    def set_direction(self, direction: Literal['', 'forward', 'reverse']):
        ...

    def set_percentage(self, percentage: int):
        ...

    def set_preset_mode(self, preset_mode: str):
        """

        Args:
            preset_mode:  Example: auto"""
        ...

class fan:
    laundry: _fan_state
    bathroom: _fan_state

    @staticmethod
    def turn_on(*, entity_id: str, percentage: int | None=None, preset_mode: str | None=None):
        """

        Args:
            entity_id: Entity ID
            preset_mode:  Example: auto"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def increase_speed(*, entity_id: str, percentage_step: int | None=None):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def decrease_speed(*, entity_id: str, percentage_step: int | None=None):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def oscillate(*, entity_id: str, oscillating: bool):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_direction(*, entity_id: str, direction: Literal['', 'forward', 'reverse']):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_percentage(*, entity_id: str, percentage: int):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_preset_mode(*, entity_id: str, preset_mode: str):
        """

        Args:
            entity_id: Entity ID
            preset_mode:  Example: auto"""
        ...

class ffmpeg:

    @staticmethod
    def start(*, entity_id: str | None=None):
        ...

    @staticmethod
    def stop(*, entity_id: str | None=None):
        ...

    @staticmethod
    def restart(*, entity_id: str | None=None):
        ...

class file:

    @staticmethod
    def read_file(*, file_name: str | None=None, file_encoding: Literal['', 'JSON', 'YAML'] | None=None) -> dict[str, Any]:
        """

        Args:
            file_name:  Example: www/my_file.json
            file_encoding:  Example: JSON"""
        ...

class frontend:

    @staticmethod
    def set_theme(*, name, mode: Literal['', 'dark', 'light']='light'):
        """

        Args:
            name:  Example: default"""
        ...

    @staticmethod
    def reload_themes():
        ...

class google_assistant:

    @staticmethod
    def request_sync(*, agent_user_id: str | None=None):
        ...

class google_generative_ai_conversation:

    @staticmethod
    def generate_content(*, prompt: str, filenames: str | None=None) -> dict[str, Any]:
        ...

class grocy:

    @staticmethod
    def add_product_to_stock(*, product_id: str, amount: float=1, price: str | None=None):
        """Adds a given amount of a product to the stock

        Args:
            product_id: The id of the product to add to stock Example: 3
            amount: The amount to add to stock Example: 3
            price: The purchase price per purchase quantity unit of the added product Example: 1.99"""
        ...

    @staticmethod
    def open_product(*, product_id: str, amount: float, allow_subproduct_substitution: bool=False):
        """Opens a given amount of a product in stock

        Args:
            product_id: The id of the product to open Example: 3
            amount: The amount to open Example: 1
            allow_subproduct_substitution: If subproduct substitution is allowed"""
        ...

    @staticmethod
    def consume_product_from_stock(*, product_id: str, amount: float, transaction_type: Literal['', 'CONSUME', 'PURCHASE', 'INVENTORY_CORRECTION', 'PRODUCT_OPENED']='CONSUME', spoiled: bool=False, allow_subproduct_substitution: bool=False):
        """Consumes a given amount of a product to the stock

        Args:
            product_id: The id of the product to consume Example: 3
            amount: The amount to consume Example: 3
            transaction_type: The type of the transaction. Example: CONSUME
            spoiled: If the product was removed because of spoilage
            allow_subproduct_substitution: If subproduct substitution is allowed"""
        ...

    @staticmethod
    def execute_chore(*, chore_id: str, done_by: str, track_execution_now: bool=False, skipped: bool=False):
        """Executes the given chore with an optional timestamp and executor

        Args:
            chore_id: The id of the chore to execute Example: 3
            done_by: The id of the user who executed the chore Example: 0
            track_execution_now: If the chore execution should be tracked with the time now
            skipped: Skip next chore schedule"""
        ...

    @staticmethod
    def complete_task(*, task_id: str):
        """Completes the given task

        Args:
            task_id: The id of the task to complete Example: 3"""
        ...

    @staticmethod
    def add_generic(*, entity_type: Literal['', 'products', 'chores', 'product_barcodes', 'batteries', 'locations', 'quantity_units', 'quantity_unit_conversions', 'shopping_list', 'shopping_lists', 'shopping_locations', 'recipes', 'recipes_pos', 'recipes_nestings', 'tasks', 'task_categories', 'product_groups', 'equipment', 'userfields', 'userentities', 'userobjects', 'meal_plan']='tasks', data: Any):
        """Adds a single object of the given entity type

        Args:
            entity_type: The type of entity you like to add. Example: tasks
            data: JSON object with what data you want to add (yaml format also works). See Grocy api documentation on Generic entity interactions: https://demo.grocy.info/api"""
        ...

    @staticmethod
    def update_generic(*, entity_type: Literal['', 'products', 'chores', 'product_barcodes', 'batteries', 'locations', 'quantity_units', 'quantity_unit_conversions', 'shopping_list', 'shopping_lists', 'shopping_locations', 'recipes', 'recipes_pos', 'recipes_nestings', 'tasks', 'task_categories', 'product_groups', 'equipment', 'userfields', 'userentities', 'userobjects', 'meal_plan']='tasks', object_id: str, data: Any):
        """Edits a single object of the given entity type

        Args:
            entity_type: The type of entity you like to update. Example: tasks
            object_id: The ID of the entity to update. Example: 1
            data: JSON object with what data you want to update (yaml format also works). See Grocy api documentation on Generic entity interactions: https://demo.grocy.info/api"""
        ...

    @staticmethod
    def delete_generic(*, entity_type: Literal['', 'products', 'chores', 'product_barcodes', 'batteries', 'locations', 'quantity_units', 'quantity_unit_conversions', 'shopping_list', 'shopping_lists', 'shopping_locations', 'recipes', 'recipes_pos', 'recipes_nestings', 'tasks', 'task_categories', 'product_groups', 'equipment', 'userfields', 'userentities', 'userobjects', 'meal_plan']='tasks', object_id: str):
        """Deletes a single object of the given entity type

        Args:
            entity_type: The type of entity to be deleted. Example: tasks
            object_id: The ID of the entity to delete. Example: 1"""
        ...

    @staticmethod
    def consume_recipe(*, recipe_id: str):
        """Consumes the given recipe

        Args:
            recipe_id: The id of the recipe to consume Example: 3"""
        ...

    @staticmethod
    def track_battery(*, battery_id: str):
        """Tracks the given battery

        Args:
            battery_id: The id of the battery Example: 1"""
        ...

    @staticmethod
    def add_missing_products_to_shopping_list(*, list_id: str | None=None):
        """Adds currently missing products to the given shopping list.

        Args:
            list_id: The id of the shopping list to be added to. Example: 1"""
        ...

    @staticmethod
    def remove_product_in_shopping_list(*, product_id: str, amount: float, list_id: str | None=None):
        """Removes a product in the given shopping list.

        Args:
            product_id: The id of the product to remove Example: 3
            amount: The amount to remove Example: 3
            list_id: The id of the shopping list to be added to. Example: 1"""
        ...

class group:

    @staticmethod
    def reload():
        ...

    @staticmethod
    def set(*, object_id: str, name: str | None=None, icon: str | None=None, entities: str | None=None, add_entities: str | None=None, remove_entities: str | None=None, all: bool | None=None):
        """

        Args:
            object_id:  Example: test_group
            name:  Example: My test group
            icon:  Example: mdi:camera
            entities:  Example: domain.entity_id1, domain.entity_id2
            add_entities:  Example: domain.entity_id1, domain.entity_id2
            remove_entities:  Example: domain.entity_id1, domain.entity_id2"""
        ...

    @staticmethod
    def remove(*, object_id: Any):
        """

        Args:
            object_id:  Example: test_group"""
        ...

class hassio:

    @staticmethod
    def addon_start(*, addon):
        """

        Args:
            addon:  Example: core_ssh"""
        ...

    @staticmethod
    def addon_stop(*, addon):
        """

        Args:
            addon:  Example: core_ssh"""
        ...

    @staticmethod
    def addon_restart(*, addon):
        """

        Args:
            addon:  Example: core_ssh"""
        ...

    @staticmethod
    def addon_stdin(*, addon):
        """

        Args:
            addon:  Example: core_ssh"""
        ...

    @staticmethod
    def host_shutdown():
        ...

    @staticmethod
    def host_reboot():
        ...

    @staticmethod
    def backup_full(*, name: str | None=None, password: str | None=None, compressed: bool=True, location=None, homeassistant_exclude_database: bool=False):
        """

        Args:
            name:  Example: Backup 1
            password:  Example: password
            location:  Example: my_backup_mount"""
        ...

    @staticmethod
    def backup_partial(*, homeassistant: bool | None=None, homeassistant_exclude_database: bool=False, addons: Any | None=None, folders: Any | None=None, name: str | None=None, password: str | None=None, compressed: bool=True, location=None):
        """

        Args:
            addons:  Example: ['core_ssh', 'core_samba', 'core_mosquitto']
            folders:  Example: ['homeassistant', 'share']
            name:  Example: Partial backup 1
            password:  Example: password
            location:  Example: my_backup_mount"""
        ...

    @staticmethod
    def restore_full(*, slug: str, password: str | None=None):
        """

        Args:
            password:  Example: password"""
        ...

    @staticmethod
    def restore_partial(*, slug: str, homeassistant: bool | None=None, folders: Any | None=None, addons: Any | None=None, password: str | None=None):
        """

        Args:
            folders:  Example: ['homeassistant', 'share']
            addons:  Example: ['core_ssh', 'core_samba', 'core_mosquitto']
            password:  Example: password"""
        ...

class homeassistant:

    @staticmethod
    def save_persistent_states():
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def stop():
        ...

    @staticmethod
    def check_config():
        ...

    @staticmethod
    def update_entity(*, entity_id: str):
        ...

    @staticmethod
    def reload_core_config():
        ...

    @staticmethod
    def set_location(*, latitude: float, longitude: float, elevation: float | None=None):
        """

        Args:
            latitude:  Example: 32.87336
            longitude:  Example: 117.22743
            elevation:  Example: 120"""
        ...

    @staticmethod
    def reload_custom_templates():
        ...

    @staticmethod
    def reload_config_entry(*, entity_id: str, entry_id: str | None=None):
        """

        Args:
            entity_id: Entity ID
            entry_id:  Example: 8955375327824e14ba89e4b29cc3ec9a"""
        ...

    @staticmethod
    def reload_all():
        ...

    @staticmethod
    def remove_label_from_area(*, label_id, area_id):
        """Removes a label to an area. If multiple labels or multiple areas are provided, all combinations will be removed.

        Args:
            label_id: The ID(s) of the label(s) to remove from the area(s).
            area_id: The ID(s) of the area(s) to remove the label(s) from."""
        ...

    @staticmethod
    def add_label_to_device(*, label_id, device_id):
        """Adds a label to a device. If multiple labels or multiple devices are provided, all combinations will be added.

        Args:
            label_id: The ID(s) of the label(s) to add the device(s).
            device_id: The ID(s) of the device(s) to add the label(s) to."""
        ...

    @staticmethod
    def delete_floor(*, floor_id):
        """Deletes a floor on the fly.

        Args:
            floor_id: The ID of the floor to delete."""
        ...

    @staticmethod
    def hide_entity(*, entity_id: str):
        """Hides an entity (or entities) on the fly.

        Args:
            entity_id: The entity/entities to hide."""
        ...

    @staticmethod
    def ignore_all_discovered(*, domain: str | None=None):
        """Ignore all currently discovered devices that are shown on the integrations dashboard. This will not ignore devices that are discovered after this.

        Args:
            domain: The integration domain to ignore all discovered devices for. If not provided, all domains will be considered to be ignored."""
        ...

    @staticmethod
    def remove_device_from_area(*, device_id):
        """Removes a device from an area. As a device can only be in one area, this call doesn't need to specify the area.

        Args:
            device_id: The ID of the device to remove the area from."""
        ...

    @staticmethod
    def enable_polling(*, config_entry_id: str):
        """Enables polling for updates for an integration configuration entry.

        Args:
            config_entry_id: The integration configuration entry to enable polling for."""
        ...

    @staticmethod
    def disable_config_entry(*, config_entry_id: str):
        """Disables an integration configuration entry.

        Args:
            config_entry_id: The integration configuration entry to disable."""
        ...

    @staticmethod
    def delete_area(*, area_id):
        """Deletes a new area on the fly.

        Args:
            area_id: The ID of the area to delete."""
        ...

    @staticmethod
    def disable_entity(*, entity_id: str):
        """Disables an entity (or entities) on the fly.

        Args:
            entity_id: The entity/entities to disable."""
        ...

    @staticmethod
    def remove_alias_from_floor(*, floor_id, alias: Any):
        """Removes an alias from a floor.

        Args:
            floor_id: The ID of the floor to remove the alias from.
            alias: The alias (or list of aliasses) to remove from the floor."""
        ...

    @staticmethod
    def set_area_aliases(*, area_id, aliases: Any):
        """Sets aliases for an area. Overwrite and removed any existing aliases, fully replacing them with the new ones.

        Args:
            area_id: The ID of the area to set the aliases for.
            aliases: The aliases to set for the area."""
        ...

    @staticmethod
    def add_label_to_area(*, label_id, area_id):
        """Adds a label to an area. If multiple labels or multiple areas are provided, all combinations will be added.

        Args:
            label_id: The ID(s) of the label(s) to add the area(s).
            area_id: The ID(s) of the area(s) to add the label(s) to."""
        ...

    @staticmethod
    def remove_entity_from_area(*, entity_id: str):
        """Removes an entity from an area. As an entity can only be in one area, this call doesn't need to specify the area. Please note, the entity will still be in the area of the device that provides it after this call.

        Args:
            entity_id: The ID of the entity (or entities) to remove the area from."""
        ...

    @staticmethod
    def remove_area_from_floor(*, area_id):
        """Removes an area from a floor. As an area can only be on one floor, this call doesn't need to specify the floor.

        Args:
            area_id: The ID of the area to remove the floor from."""
        ...

    @staticmethod
    def remove_label_from_device(*, label_id, device_id):
        """Removes a label from a device. If multiple labels or multiple devices are provided, all combinations will be removed.

        Args:
            label_id: The ID(s) of the label(s) to remove from the device(s).
            device_id: The ID(s) of the device(s) to remove the label(s) from."""
        ...

    @staticmethod
    def enable_config_entry(*, config_entry_id: str):
        """Enables an integration configuration entry.

        Args:
            config_entry_id: The integration configuration entry to enable."""
        ...

    @staticmethod
    def disable_device(*, device_id):
        """Disables a device on the fly.

        Args:
            device_id: The device(s) to disable."""
        ...

    @staticmethod
    def add_alias_to_area(*, area_id, alias: Any):
        """Adds an alias to an area.

        Args:
            area_id: The ID of the area to add the alias to.
            alias: The alias (or list of aliasses) to add to the area."""
        ...

    @staticmethod
    def add_area_to_floor(*, floor_id, area_id):
        """Adds an area to a floor. Please note, if the area is already on a floor, it will be removed from the previous floor.

        Args:
            floor_id: The ID of the floor to add the area on.
            area_id: The ID of the area(s) to add to the floor."""
        ...

    @staticmethod
    def add_label_to_entity(*, label_id, entity_id: str):
        """Adds a label to an entity. If multiple labels or multiple entities are provided, all combinations will be added.

        Args:
            label_id: The ID(s) of the label(s) to add the entity/entities.
            entity_id: The ID(s) of the entity/entities to add the label(s) to."""
        ...

    @staticmethod
    def enable_device(*, device_id):
        """Enables a device on the fly.

        Args:
            device_id: The device(s) to enable."""
        ...

    @staticmethod
    def enable_entity(*, entity_id: str):
        """Enables an entity (or entities) on the fly.

        Args:
            entity_id: The entity/entities to enable."""
        ...

    @staticmethod
    def add_alias_to_floor(*, floor_id, alias: Any):
        """Adds an alias to a floor.

        Args:
            floor_id: The ID of the floor to add the alias to.
            alias: The alias (or list of aliasses) to add to the floor."""
        ...

    @staticmethod
    def update_entity_id(*, entity_id: str, new_entity_id: str):
        """Updates an entity's ID on the fly.

        Args:
            entity_id: The entity/entities to update.
            new_entity_id: The new ID for the entity"""
        ...

    @staticmethod
    def restart(*, safe_mode: bool | None=None, force: bool | None=None):
        """Restart the Home Assistant action.

        Args:
            safe_mode: If the restart should be done in safe mode. This will disable all custom integrations and frontend modules.
            force: Force the restart. WARNING! This will not gracefully shutdown Home Assistant, it will skip configuration checks and ignore running database migrations. Only use this if you know what you are doing."""
        ...

    @staticmethod
    def add_device_to_area(*, area_id, device_id):
        """Adds an device to an area. Please note, if the device is already in an area, it will be removed from the previous area.

        Args:
            area_id: The ID of the area to add the device to.
            device_id: The ID of the device(s) to add to the area."""
        ...

    @staticmethod
    def delete_label(*, label_id):
        """Deletes a label on the fly.

        Args:
            label_id: The ID of the label to delete."""
        ...

    @staticmethod
    def delete_all_orphaned_entities():
        """Deletes all orphaned entities that no longer have an integration that claim/provide them. Please note, if the integration was just removed, it might need a restart for Home Assistant to realize they are orphaned.
**WARNING** Entities might have been marked orphaned because an integration is offline or not working since Home Assistant started. Calling this action will delete those entities as well."""
        ...

    @staticmethod
    def create_area(*, name: str, icon: str | None=None, aliases: Any | None=None):
        """Creates a new area on the fly.

        Args:
            name: The name of the area to create.
            icon: Icon to use for the area.
            aliases: A list of aliases for the area. This is useful if you want to use the area in a different language or different nickname."""
        ...

    @staticmethod
    def rename_entity(*, entity_id: str, name: str):
        """Renames an entity (or entities) on the fly.

        Args:
            entity_id: The entity/entities to rename.
            name: The new name for the entity/entities."""
        ...

    @staticmethod
    def remove_label_from_entity(*, label_id, entity_id: str):
        """Removes a label from an entity. If multiple labels or multiple entities are provided, all combinations will be removed.

        Args:
            label_id: The ID(s) of the label(s) to remove from the entity/entities.
            entity_id: The ID(s) of the entity/entities to remove the label(s) from."""
        ...

    @staticmethod
    def create_floor(*, name: str, icon: str | None=None, level: float | None=None, aliases: Any | None=None):
        """Creates a new floor on the fly.

        Args:
            name: The name of the floor to create.
            icon: Icon to use for the floor.
            level: The level the floor is on in your home.
            aliases: A list of aliases for the floor. This is useful if you want to use the floor in a different language or different nickname."""
        ...

    @staticmethod
    def unhide_entity(*, entity_id: str):
        """Unhides an entity (or entities) on the fly.

        Args:
            entity_id: The entity/entities to unhide."""
        ...

    @staticmethod
    def create_label(*, name: str, description: str, icon: str | None=None, color: Literal['', 'primary', 'accent', 'disabled', 'red', 'pink', 'purple', 'deep_purple', 'indigo', 'blue', 'light_blue', 'cyan', 'teal', 'green', 'light_green', 'lime', 'yellow', 'orange', 'deep_orange', 'brown', 'grey', 'blue_grey', 'black', 'white'] | None=None):
        """Creates a new label on the fly.

        Args:
            name: The name of the label to create.
            description: Description for the label.
            icon: Icon to use for the label.
            color: Color to use for the label. Can be a color name from the list, or a hex color code (like #FF0000)."""
        ...

    @staticmethod
    def set_floor_aliases(*, floor_id, aliases: Any):
        """Sets aliases for a floor. Overwrite and removed any existing aliases, fully replacing them with the new ones.

        Args:
            floor_id: The ID of the floor to set the aliases for.
            aliases: The aliases to set for the floor."""
        ...

    @staticmethod
    def list_orphaned_database_entities() -> dict[str, Any]:
        """Lists all orphaned database entities unclaimed by any integration."""
        ...

    @staticmethod
    def add_entity_to_area(*, area_id, entity_id: str):
        """Adds an entity to an area. Please note, if the enity is already in an area, it will be removed from the previous area. This will override the area the device, that provides this entity, is in.

        Args:
            area_id: The ID of the area to add the entity to.
            entity_id: The ID of the entity (or entities) to add to the area."""
        ...

    @staticmethod
    def remove_alias_from_area(*, area_id, alias: Any):
        """Removes an alias from an area.

        Args:
            area_id: The ID of the area to remove the alias from.
            alias: The alias (or list of aliasses) to remove from the area."""
        ...

    @staticmethod
    def disable_polling(*, config_entry_id: str):
        """Disables polling for updates for an integration configuration entry.

        Args:
            config_entry_id: The integration configuration entry to disable polling for."""
        ...

class humidifier:

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_mode(*, entity_id: str, mode: str):
        """

        Args:
            entity_id: Entity ID
            mode:  Example: away"""
        ...

    @staticmethod
    def set_humidity(*, entity_id: str, humidity: int):
        """

        Args:
            entity_id: Entity ID"""
        ...

class ifttt:

    @staticmethod
    def trigger(*, event: str, value1: str | None=None, value2: str | None=None, value3: str | None=None):
        """

        Args:
            event:  Example: MY_HA_EVENT
            value1:  Example: Hello World
            value2:  Example: some additional data
            value3:  Example: even more data"""
        ...

class _image_state(StateVal):
    access_token: str
    entity_picture: str

    def snapshot(self, filename: str):
        """

        Args:
            filename:  Example: /tmp/image_snapshot.jpg"""
        ...

class image:
    music_assistant_jukebox_internal_access_qr_code: _image_state
    music_assistant_jukebox_external_access_qr_code: _image_state

    @staticmethod
    def snapshot(*, entity_id: str, filename: str):
        """

        Args:
            entity_id: Entity ID
            filename:  Example: /tmp/image_snapshot.jpg"""
        ...

class _input_boolean_state(StateVal):
    editable: bool

    def turn_on(self):
        ...

    def turn_off(self):
        ...

    def toggle(self):
        ...

class _input_button_state(StateVal):
    editable: bool

    def press(self):
        ...

class _input_datetime_state(StateVal):
    day: int
    editable: bool
    has_date: bool
    has_time: bool
    hour: int
    minute: int
    month: int
    second: int
    timestamp: float
    year: int

    def set_datetime(self, *, date: str | None=None, time: str | None=None, datetime: str | None=None, timestamp: float | None=None):
        '''

        Args:
            date:  Example: "2019-04-20"
            time:  Example: "05:04:20"
            datetime:  Example: "2019-04-20 05:04:20"'''
        ...

class _input_number_state(StateVal):
    editable: bool
    initial: Any
    max: float
    min: float
    mode: str
    step: float
    unit_of_measurement: str

    def set_value(self, value: float):
        ...

    def min(self):
        """Set an input number entity to its minimum value."""
        ...

    def max(self):
        """Set an input number entity to its maximum value."""
        ...

    def decrement(self, amount: float | None):
        """Decrease an input number entity value by a certain amount.

        Args:
            amount: The amount to decrease the input number with. If not provided, the step of the number entity will be used."""
        ...

    def increment(self, amount: float | None):
        """Increase an input number entity value by a certain amount.

        Args:
            amount: The amount to increase the input number with. If not provided, the step of the number entity will be used."""
        ...

class _input_select_state(StateVal):
    editable: bool
    options: list

    def select_first(self):
        ...

    def select_last(self):
        ...

    def select_next(self, cycle: bool):
        ...

    def select_option(self, option: str):
        '''

        Args:
            option:  Example: "Item A"'''
        ...

    def select_previous(self, cycle: bool):
        ...

    def set_options(self, options: str):
        """

        Args:
            options:  Example: ["Item A", "Item B", "Item C"]"""
        ...

    def shuffle(self):
        """Shuffles the list of selectable options for an `input_select` entity. This is not persistent and will be undone once reloaded or Home Assistant restarts."""
        ...

    def random(self, options: Any | None):
        """Select an random option for an input_select entity.

        Args:
            options: Limits the options to select from. If not provided, all options will be considered."""
        ...

    def sort(self):
        """Sorts the list of selectable options for an `input_select` entity. This is not persistent and will be undone once reloaded or Home Assistant restarts."""
        ...

class _input_text_state(StateVal):
    editable: bool
    max: int
    min: int
    mode: str
    pattern: Any

    def set_value(self, value: str):
        """

        Args:
            value:  Example: This is an example text"""
        ...

class input_boolean:
    test_boolean: _input_boolean_state
    shower_vents_night_auto_off: _input_boolean_state
    xiaomi_gateway_autolight: _input_boolean_state
    dahua_vto_ring_announce: _input_boolean_state
    humidifier_empty_notification: _input_boolean_state
    humidifier_humidity_too_high_auto_off: _input_boolean_state
    water_leak_alert: _input_boolean_state
    sun_office_autowindow: _input_boolean_state
    battery_low_notification: _input_boolean_state
    humidifier_auto_on: _input_boolean_state
    kitchen_window_auto_positioning: _input_boolean_state
    speedtest_autocheck: _input_boolean_state
    sun_kitchen_autowindow: _input_boolean_state
    shower_humidity_auto_fan_on: _input_boolean_state
    shower_humidity_auto_fan_off: _input_boolean_state
    bathroom_humidity_auto_fan_on: _input_boolean_state
    bathroom_humidity_auto_fan_off: _input_boolean_state
    laundry_vents_auto_on: _input_boolean_state
    laundry_vents_auto_off: _input_boolean_state
    router_autoreboot: _input_boolean_state
    ping_world_notification: _input_boolean_state
    power_outage_calendar: _input_boolean_state
    office_auto_ac: _input_boolean_state
    fake_ac: _input_boolean_state
    bedroom_auto_ac: _input_boolean_state
    room_auto_ac: _input_boolean_state
    kitchen_auto_ac: _input_boolean_state
    cat_feed_notification: _input_boolean_state
    audio_alerts: _input_boolean_state
    vacuum_autolight: _input_boolean_state
    sun_bedroom_autowindow: _input_boolean_state
    bedroom_reed_window_block: _input_boolean_state
    bedroom_reed_ac_block: _input_boolean_state
    vacuum_stuck_notif: _input_boolean_state
    cat_mat_motion_auto_on: _input_boolean_state
    bedroom_ac_emergency_heat: _input_boolean_state
    auto_shower_floor: _input_boolean_state
    tv_turns_on_projector: _input_boolean_state
    kyiv_alarm_actions: _input_boolean_state
    office_auto_valve: _input_boolean_state
    bedroom_auto_valve: _input_boolean_state
    room_auto_valve: _input_boolean_state
    kitchen_auto_valve: _input_boolean_state
    shower_speaker_autovolume: _input_boolean_state
    sun_room_autowindow: _input_boolean_state
    room_reed_window_block: _input_boolean_state
    sun_autowindow_pause: _input_boolean_state
    power_grey_calendar: _input_boolean_state
    ecoflow_dynamic_charging_speed: _input_boolean_state
    air_raid_summary: _input_boolean_state
    power_outage_actions: _input_boolean_state
    noone_home_autoactions: _input_boolean_state
    alert_server_availability_actions: _input_boolean_state
    auto_turn_off_alert_server_on_power_outage: _input_boolean_state
    auto_turn_on_alert_server_after_power_outage: _input_boolean_state
    last_seen_monitor: _input_boolean_state
    humidity_notification_office: _input_boolean_state
    temperature_notification_office: _input_boolean_state
    someone_home_autoactions: _input_boolean_state
    air_quality_notification: _input_boolean_state
    asleep_actions: _input_boolean_state
    dahua_vto_door_unlock: _input_boolean_state
    catbird_asleep: _input_boolean_state
    awake_bed_light: _input_boolean_state
    fake_boolean: _input_boolean_state
    office_hourly_checks: _input_boolean_state
    boiler_temp_notif: _input_boolean_state
    cat_toilet_notification: _input_boolean_state
    scene_helper_movie_time: _input_boolean_state
    coffee_machine_heatup_notification: _input_boolean_state
    guests: _input_boolean_state
    pihole_blocking: _input_boolean_state
    chore_notifier: _input_boolean_state
    hallway_closet_reed_autolight: _input_boolean_state
    scene_helper_music_time: _input_boolean_state
    scene_helper_music_shower: _input_boolean_state
    scene_helper_music_relax: _input_boolean_state
    scene_helper_music_funky: _input_boolean_state
    scene_helper_coffee: _input_boolean_state
    scene_helper_music_next: _input_boolean_state
    morning_greeting: _input_boolean_state
    bedroom_led_controls: _input_boolean_state
    rain_incoming: _input_boolean_state
    scene_helper_music_album: _input_boolean_state
    scene_helper_music_artist: _input_boolean_state
    led_smooth_control: _input_boolean_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class input_button:
    vacuum_service_p_update: _input_button_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def press(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class input_datetime:
    next_outage_datetime: _input_datetime_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def set_datetime(*, entity_id: str, date: str | None=None, time: str | None=None, datetime: str | None=None, timestamp: float | None=None):
        '''

        Args:
            entity_id: Entity ID
            date:  Example: "2019-04-20"
            time:  Example: "05:04:20"
            datetime:  Example: "2019-04-20 05:04:20"'''
        ...

class input_number:
    fake_temp: _input_number_state
    office_wanted_temperature: _input_number_state
    bedroom_wanted_temperature: _input_number_state
    kitchen_wanted_temperature: _input_number_state
    room_wanted_temperature: _input_number_state
    fake_number: _input_number_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def set_value(*, entity_id: str, value: float):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def min(*, entity_id: str):
        """Set an input number entity to its minimum value.

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def max(*, entity_id: str):
        """Set an input number entity to its maximum value.

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def decrement(*, entity_id: str, amount: float | None=None):
        """Decrease an input number entity value by a certain amount.

        Args:
            entity_id: Entity ID
            amount: The amount to decrease the input number with. If not provided, the step of the number entity will be used."""
        ...

    @staticmethod
    def increment(*, entity_id: str, amount: float | None=None):
        """Increase an input number entity value by a certain amount.

        Args:
            entity_id: Entity ID
            amount: The amount to increase the input number with. If not provided, the step of the number entity will be used."""
        ...

class input_select:
    office_auto_ac_allowed_modes: _input_select_state
    bedroom_auto_ac_allowed_modes: _input_select_state
    room_auto_ac_allowed_modes: _input_select_state
    kitchen_auto_ac_allowed_modes: _input_select_state
    boiler_control_mode: _input_select_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def select_first(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def select_last(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def select_next(*, entity_id: str, cycle: bool=True):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def select_option(*, entity_id: str, option: str):
        '''

        Args:
            entity_id: Entity ID
            option:  Example: "Item A"'''
        ...

    @staticmethod
    def select_previous(*, entity_id: str, cycle: bool=True):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_options(*, entity_id: str, options: str):
        """

        Args:
            entity_id: Entity ID
            options:  Example: ["Item A", "Item B", "Item C"]"""
        ...

    @staticmethod
    def shuffle(*, entity_id: str):
        """Shuffles the list of selectable options for an `input_select` entity. This is not persistent and will be undone once reloaded or Home Assistant restarts.

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def random(*, entity_id: str, options: Any | None=None):
        """Select an random option for an input_select entity.

        Args:
            entity_id: Entity ID
            options: Limits the options to select from. If not provided, all options will be considered."""
        ...

    @staticmethod
    def sort(*, entity_id: str):
        """Sorts the list of selectable options for an `input_select` entity. This is not persistent and will be undone once reloaded or Home Assistant restarts.

        Args:
            entity_id: Entity ID"""
        ...

class input_text:
    wemos_wroom32_oled_text: _input_text_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def set_value(*, entity_id: str, value: str):
        """

        Args:
            entity_id: Entity ID
            value:  Example: This is an example text"""
        ...

class iperf3:

    @staticmethod
    def speedtest(*, host: str='None'):
        """

        Args:
            host:  Example: iperf.he.net"""
        ...

class _light_state(StateVal):
    brightness: int
    color_mode: str
    effect: str
    effect_list: list
    hs_color: tuple
    max_color_temp_kelvin: int
    max_mireds: int
    min_color_temp_kelvin: int
    min_mireds: int
    rgb_color: tuple
    supported_color_modes: list
    supported_features: int
    xy_color: tuple

    def turn_on(self, *, transition: int | None=None, rgb_color: tuple[int, int, int] | None=None, color_temp_kelvin: int | None=None, brightness_pct: int | None=None, brightness_step_pct: int | None=None, effect: str | None=None, rgbw_color: Any | None=None, rgbww_color: Any | None=None, color_name: Literal['', 'homeassistant', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'navyblue', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'] | None=None, hs_color: Any | None=None, xy_color: Any | None=None, color_temp: int | None=None, brightness: int | None=None, brightness_step: int | None=None, white=None, profile: str | None=None, flash: Literal['', 'long', 'short'] | None=None):
        """

        Args:
            rgb_color:  Example: [255, 100, 100]
            rgbw_color:  Example: [255, 100, 100, 50]
            rgbww_color:  Example: [255, 100, 100, 50, 70]
            hs_color:  Example: [300, 70]
            xy_color:  Example: [0.52, 0.43]
            profile:  Example: relax"""
        ...

    def turn_off(self, *, transition: int | None=None, flash: Literal['', 'long', 'short'] | None=None):
        ...

    def toggle(self, *, transition: int | None=None, rgb_color: tuple[int, int, int] | None=None, color_temp_kelvin: int | None=None, brightness_pct: int | None=None, effect: str | None=None, rgbw_color: Any | None=None, rgbww_color: Any | None=None, color_name: Literal['', 'homeassistant', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'navyblue', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'] | None=None, hs_color: Any | None=None, xy_color: Any | None=None, color_temp: int | None=None, brightness: int | None=None, white=None, profile: str | None=None, flash: Literal['', 'long', 'short'] | None=None):
        """

        Args:
            rgb_color:  Example: [255, 100, 100]
            rgbw_color:  Example: [255, 100, 100, 50]
            rgbww_color:  Example: [255, 100, 100, 50, 70]
            hs_color:  Example: [300, 70]
            xy_color:  Example: [0.52, 0.43]
            profile:  Example: relax"""
        ...

class light:
    main_switch: _light_state
    gateway_light: _light_state
    office: _light_state
    bathroom: _light_state
    bedroom: _light_state
    bedroom_led_top: _light_state
    couch: _light_state
    couch_led: _light_state
    couch_reading: _light_state
    entrance: _light_state
    hallway: _light_state
    kitchen: _light_state
    kitchen_led: _light_state
    room: _light_state
    shower: _light_state
    wardrobe: _light_state
    door_led: _light_state
    iets_pwm: _light_state
    c6_man8_led: _light_state
    shower_led: _light_state
    bedroom_entrance: _light_state
    laundry: _light_state
    xiaomi_gateway_light: _light_state
    xiaomi_gateway: _light_state
    bathroom_led: _light_state
    bedroom_led_bottom: _light_state
    bedroom_led_top_future: _light_state
    sonoff_1000f26724: _light_state
    miboxer_cloud_2: _light_state

    @staticmethod
    def turn_on(*, entity_id: str, transition: int | None=None, rgb_color: tuple[int, int, int] | None=None, color_temp_kelvin: int | None=None, brightness_pct: int | None=None, brightness_step_pct: int | None=None, effect: str | None=None, rgbw_color: Any | None=None, rgbww_color: Any | None=None, color_name: Literal['', 'homeassistant', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'navyblue', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'] | None=None, hs_color: Any | None=None, xy_color: Any | None=None, color_temp: int | None=None, brightness: int | None=None, brightness_step: int | None=None, white=None, profile: str | None=None, flash: Literal['', 'long', 'short'] | None=None):
        """

        Args:
            entity_id: Entity ID
            rgb_color:  Example: [255, 100, 100]
            rgbw_color:  Example: [255, 100, 100, 50]
            rgbww_color:  Example: [255, 100, 100, 50, 70]
            hs_color:  Example: [300, 70]
            xy_color:  Example: [0.52, 0.43]
            profile:  Example: relax"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str, transition: int | None=None, flash: Literal['', 'long', 'short'] | None=None):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str, transition: int | None=None, rgb_color: tuple[int, int, int] | None=None, color_temp_kelvin: int | None=None, brightness_pct: int | None=None, effect: str | None=None, rgbw_color: Any | None=None, rgbww_color: Any | None=None, color_name: Literal['', 'homeassistant', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'navyblue', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'] | None=None, hs_color: Any | None=None, xy_color: Any | None=None, color_temp: int | None=None, brightness: int | None=None, white=None, profile: str | None=None, flash: Literal['', 'long', 'short'] | None=None):
        """

        Args:
            entity_id: Entity ID
            rgb_color:  Example: [255, 100, 100]
            rgbw_color:  Example: [255, 100, 100, 50]
            rgbww_color:  Example: [255, 100, 100, 50, 70]
            hs_color:  Example: [300, 70]
            xy_color:  Example: [0.52, 0.43]
            profile:  Example: relax"""
        ...

class _lock_state(StateVal):
    supported_features: int

    def unlock(self, code: str | None):
        """

        Args:
            code:  Example: 1234"""
        ...

    def lock(self, code: str | None):
        """

        Args:
            code:  Example: 1234"""
        ...

    def open(self, code: str | None):
        """

        Args:
            code:  Example: 1234"""
        ...

class lock:
    door: _lock_state
    orbitrack_tl_child_lock: _lock_state
    energy_monitoring_smartplug_child_lock: _lock_state

    @staticmethod
    def unlock(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def lock(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

    @staticmethod
    def open(*, entity_id: str, code: str | None=None):
        """

        Args:
            entity_id: Entity ID
            code:  Example: 1234"""
        ...

class logbook:

    @staticmethod
    def log(*, name: str, message: str, entity_id: str | None=None, domain: str | None=None):
        """

        Args:
            name:  Example: Kitchen
            message:  Example: is being used
            domain:  Example: light"""
        ...

class logger:

    @staticmethod
    def set_default_level(*, level: Literal['', 'debug', 'info', 'warning', 'error', 'fatal', 'critical'] | None=None):
        ...

    @staticmethod
    def set_level():
        ...

class lovelace:

    @staticmethod
    def reload_resources():
        ...

class matter:

    @staticmethod
    def water_heater_boost(*, entity_id: str, duration: float=3600, emergency_boost: bool=False, temporary_setpoint: int=65):
        """

        Args:
            entity_id: Entity ID"""
        ...

class _media_player_state(StateVal):
    active_queue: str
    app_id: str
    assumed_state: bool
    entity_picture_local: Any
    is_volume_muted: bool
    mass_player_type: str
    media_artist: str
    media_content_id: str
    media_content_type: str
    media_duration: int
    media_position: int
    media_position_updated_at: datetime
    media_title: str
    repeat: str
    shuffle: bool
    supported_features: int
    volume_level: float

    def turn_on(self):
        ...

    def turn_off(self):
        ...

    def toggle(self):
        ...

    def volume_up(self):
        ...

    def volume_down(self):
        ...

    def media_play_pause(self):
        ...

    def media_play(self):
        ...

    def media_pause(self):
        ...

    def media_stop(self):
        ...

    def media_next_track(self):
        ...

    def media_previous_track(self):
        ...

    def clear_playlist(self):
        ...

    def volume_set(self, volume_level: int):
        ...

    def volume_mute(self, is_volume_muted: bool):
        ...

    def media_seek(self, seek_position: float):
        ...

    def join(self, group_members: str):
        """

        Args:
            group_members:  Example: - media_player.multiroom_player2
                - media_player.multiroom_player3
                """
        ...

    def select_source(self, source: str):
        """

        Args:
            source:  Example: video1"""
        ...

    def select_sound_mode(self, sound_mode: str | None):
        """

        Args:
            sound_mode:  Example: Music"""
        ...

    def play_media(self, *, media, enqueue: Literal['', 'play', 'next', 'add', 'replace'] | None=None, announce: bool | None=None):
        """

        Args:
            media:  Example: {"media_content_id": "https://home-assistant.io/images/cast/splash.png", "media_content_type": "music"}
            announce:  Example: true"""
        ...

    def browse_media(self, *, media_content_type: str | None=None, media_content_id: str | None=None) -> dict[str, Any]:
        """

        Args:
            media_content_type:  Example: music
            media_content_id:  Example: A:ALBUMARTIST/Beatles"""
        ...

    def search_media(self, *, search_query: str, media_content_type: str | None=None, media_content_id: str | None=None, media_filter_classes: str | None=None) -> dict[str, Any]:
        """

        Args:
            search_query:  Example: Beatles
            media_content_type:  Example: music
            media_content_id:  Example: A:ALBUMARTIST/Beatles
            media_filter_classes:  Example: ['album', 'artist']"""
        ...

    def shuffle_set(self, shuffle: bool):
        ...

    def unjoin(self):
        ...

    def repeat_set(self, repeat: Literal['', 'off', 'all', 'one']):
        ...

class media_player:
    mini: _media_player_state
    kitchen_tv_wifi: _media_player_state
    mass_kitchen_audio: _media_player_state
    mass_bedroom_speaker: _media_player_state
    mass_office_audio: _media_player_state
    mass_music_speakers: _media_player_state
    mass_all: _media_player_state
    mass_kitchen_speaker: _media_player_state
    mass_office_speaker: _media_player_state
    mass_bathroom_speaker: _media_player_state
    mass_broadcast: _media_player_state
    mass_relax: _media_player_state
    mass_all_speakers: _media_player_state
    mass_room_audio: _media_player_state
    mass_shower_speaker: _media_player_state
    mass_mini: _media_player_state

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def volume_up(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def volume_down(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def media_play_pause(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def media_play(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def media_pause(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def media_stop(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def media_next_track(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def media_previous_track(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def clear_playlist(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def volume_set(*, entity_id: str, volume_level: int):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def volume_mute(*, entity_id: str, is_volume_muted: bool):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def media_seek(*, entity_id: str, seek_position: float):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def join(*, entity_id: str, group_members: str):
        """

        Args:
            entity_id: Entity ID
            group_members:  Example: - media_player.multiroom_player2
                - media_player.multiroom_player3
                """
        ...

    @staticmethod
    def select_source(*, entity_id: str, source: str):
        """

        Args:
            entity_id: Entity ID
            source:  Example: video1"""
        ...

    @staticmethod
    def select_sound_mode(*, entity_id: str, sound_mode: str | None=None):
        """

        Args:
            entity_id: Entity ID
            sound_mode:  Example: Music"""
        ...

    @staticmethod
    def play_media(*, entity_id: str, media, enqueue: Literal['', 'play', 'next', 'add', 'replace'] | None=None, announce: bool | None=None):
        """

        Args:
            entity_id: Entity ID
            media:  Example: {"media_content_id": "https://home-assistant.io/images/cast/splash.png", "media_content_type": "music"}
            announce:  Example: true"""
        ...

    @staticmethod
    def browse_media(*, entity_id: str, media_content_type: str | None=None, media_content_id: str | None=None) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID
            media_content_type:  Example: music
            media_content_id:  Example: A:ALBUMARTIST/Beatles"""
        ...

    @staticmethod
    def search_media(*, entity_id: str, search_query: str, media_content_type: str | None=None, media_content_id: str | None=None, media_filter_classes: str | None=None) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID
            search_query:  Example: Beatles
            media_content_type:  Example: music
            media_content_id:  Example: A:ALBUMARTIST/Beatles
            media_filter_classes:  Example: ['album', 'artist']"""
        ...

    @staticmethod
    def shuffle_set(*, entity_id: str, shuffle: bool):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def unjoin(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def repeat_set(*, entity_id: str, repeat: Literal['', 'off', 'all', 'one']):
        """

        Args:
            entity_id: Entity ID"""
        ...

class mqtt:

    @staticmethod
    def publish(*, topic: str, payload=None, evaluate_payload: bool=False, qos: Literal['', '0', '1', '2']=0, retain: bool=False):
        """

        Args:
            topic:  Example: /homeassistant/hello
            payload:  Example: The temperature is {{ states('sensor.temperature') }}"""
        ...

    @staticmethod
    def dump(*, topic: str | None=None, duration: int=5):
        """

        Args:
            topic:  Example: OpenZWave/#"""
        ...

    @staticmethod
    def reload():
        ...

class music_assistant:

    @staticmethod
    def search(*, config_entry_id: str, name: str, media_type: Literal['', 'artist', 'album', 'audiobook', 'playlist', 'podcast', 'track', 'radio'] | None=None, artist: str | None=None, album: str | None=None, limit: int=5, library_only: bool=False) -> dict[str, Any]:
        """

        Args:
            name:  Example: We Are The Champions
            media_type:  Example: playlist
            artist:  Example: Queen
            album:  Example: News of the world
            limit:  Example: 25
            library_only:  Example: true"""
        ...

    @staticmethod
    def get_library(*, config_entry_id: str, media_type: Literal['', 'artist', 'album', 'audiobook', 'playlist', 'podcast', 'track', 'radio'], favorite: bool=False, search: str | None=None, limit: int=25, offset: int=0, order_by: Literal['', 'name', 'name_desc', 'sort_name', 'sort_name_desc', 'timestamp_added', 'timestamp_added_desc', 'last_played', 'last_played_desc', 'play_count', 'play_count_desc', 'year', 'year_desc', 'position', 'position_desc', 'artist_name', 'artist_name_desc', 'random', 'random_play_count'] | None=None, album_type: Literal['', 'album', 'single', 'compilation', 'ep', 'unknown'] | None=None, album_artists_only: bool=False) -> dict[str, Any]:
        """

        Args:
            media_type:  Example: playlist
            favorite:  Example: true
            search:  Example: We Are The Champions
            limit:  Example: 25
            offset:  Example: 25
            order_by:  Example: random
            album_type:  Example: single
            album_artists_only:  Example: true"""
        ...

    @staticmethod
    def play_media(*, entity_id: str, media_id: Any, media_type: Literal['', 'artist', 'album', 'audiobook', 'folder', 'playlist', 'podcast', 'track', 'radio'] | None=None, artist: str | None=None, album: str | None=None, enqueue: Literal['', 'play', 'replace', 'next', 'replace_next', 'add'] | None=None, radio_mode: bool | None=None):
        """

        Args:
            entity_id: Entity ID
            media_id:  Example: spotify://playlist/aabbccddeeff
            media_type:  Example: playlist
            artist:  Example: Queen
            album:  Example: News of the world"""
        ...

    @staticmethod
    def play_announcement(*, entity_id: str, url: str, use_pre_announce: bool | None=None, announce_volume: int | None=None):
        """

        Args:
            entity_id: Entity ID
            url:  Example: http://someremotesite.com/doorbell.mp3
            use_pre_announce:  Example: true
            announce_volume:  Example: 75"""
        ...

    @staticmethod
    def transfer_queue(*, entity_id: str, source_player: str | None=None, auto_play: bool | None=None):
        """

        Args:
            entity_id: Entity ID
            auto_play:  Example: true"""
        ...

    @staticmethod
    def get_queue(*, entity_id: str) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID"""
        ...

class _notify_state(StateVal):
    supported_features: int

    def send_message(self, *, message: str, title: str | None=None):
        ...

class notify:
    ijai_de_1027836802_v3_start_room_sweep_a_2_7: _notify_state
    ijai_de_1027836802_v3_reset_consumable_a_7_1: _notify_state
    ijai_de_1027836802_v3_set_room_clean_a_7_3: _notify_state
    ijai_de_1027836802_v3_set_preference_clean_a_7_4: _notify_state
    ijai_de_1027836802_v3_get_preference_clean_a_7_5: _notify_state
    ijai_de_1027836802_v3_set_preference_type_a_7_6: _notify_state
    ijai_de_1027836802_v3_set_go_charging_a_7_7: _notify_state
    ijai_de_1027836802_v3_erase_preference_a_7_8: _notify_state
    ijai_de_1027836802_v3_set_preference_ii_a_7_9: _notify_state
    ijai_de_1027836802_v3_get_preference_ii_a_7_10: _notify_state
    ijai_de_1027836802_v3_add_a_8_1: _notify_state
    ijai_de_1027836802_v3_del_a_8_2: _notify_state
    ijai_de_1027836802_v3_add_ii_a_8_4: _notify_state
    ijai_de_1027836802_v3_get_map_order_count_a_8_5: _notify_state
    ijai_de_1027836802_v3_pause_point_clean_a_9_2: _notify_state
    ijai_de_1027836802_v3_pause_zone_clean_a_9_4: _notify_state
    ijai_de_1027836802_v3_set_virtual_wall_a_9_6: _notify_state
    ijai_de_1027836802_v3_set_zone_point_a_9_8: _notify_state
    ijai_de_1027836802_v3_start_point_clean_ii_a_9_9: _notify_state
    ijai_de_1027836802_v3_upload_by_mapid_a_10_2: _notify_state
    ijai_de_1027836802_v3_set_cur_map_a_10_3: _notify_state
    ijai_de_1027836802_v3_del_map_a_10_4: _notify_state
    ijai_de_1027836802_v3_rename_map_a_10_5: _notify_state
    ijai_de_1027836802_v3_upload_by_maptype_a_10_6: _notify_state
    ijai_de_1027836802_v3_rename_room_a_10_7: _notify_state
    ijai_de_1027836802_v3_arrange_room_a_10_8: _notify_state
    ijai_de_1027836802_v3_split_room_a_10_9: _notify_state
    ijai_de_1027836802_v3_build_new_map_a_10_11: _notify_state
    ijai_de_1027836802_v3_get_cur_path_a_10_12: _notify_state
    ijai_de_1027836802_v3_get_map_room_list_a_10_13: _notify_state
    ijai_de_1027836802_v3_upload_by_mapid_ii_a_10_14: _notify_state
    ijai_de_1027836802_v3_upload_by_maptype_ii_a_10_15: _notify_state
    ijai_de_1027836802_v3_build_map_ii_a_10_17: _notify_state
    ijai_de_1027836802_v3_set_mijia_room_list_a_10_18: _notify_state
    ijai_de_1027836802_v3_set_notdisturb_a_12_1: _notify_state
    ijai_de_1027836802_v3_download_voice_a_14_1: _notify_state
    telegram_bot_726633577_1001875044171: _notify_state
    telegram_bot_726633577_81870328: _notify_state
    telegram_bot_726633577_1001162241868: _notify_state
    telegram_bot_726633577_898416112: _notify_state
    telegram_bot_726633577_4080329146: _notify_state
    mijia_de_56078868_v1_start_rtsp_stream_a_3_1: _notify_state
    mijia_de_56078868_v1_start_hls_stream_a_4_1: _notify_state

    @staticmethod
    def send_message(*, entity_id: str, message: str, title: str | None=None):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def persistent_notification(*, message: str, title: str | None=None, data: Any | None=None):
        """

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            data:  Example: platform specific"""
        ...

    @staticmethod
    def google_assistant_broadcast(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the google_assistant_broadcast service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def google_assistant_command(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the google_assistant_command service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def mobile_app_alert_s_s24(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the mobile_app_alert_s_s24 integration.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def mobile_app_kateryna_drozd(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the mobile_app_kateryna_drozd integration.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def mobile_app_quest3(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the mobile_app_quest3 integration.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def mobile_app_alert_s_redmi_pad_pro(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the mobile_app_alert_s_redmi_pad_pro integration.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def mobile_app_21121119sg(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the mobile_app_21121119sg integration.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def mobile_app_mi_9_se(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the mobile_app_mi_9_se integration.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def notify(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the notify service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def tg_alert(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the tg_alert service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def tg_alert_video_snapshots(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the tg_alert_video_snapshots service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def tg_alert_video(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the tg_alert_video service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def tg_alert_ha_private(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the tg_alert_ha_private service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def tg_alert_ha(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the tg_alert_ha service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

    @staticmethod
    def alert_iot(*, message: str, title: str | None=None, target: Any | None=None, data: Any | None=None):
        """Sends a notification message using the alert_iot service.

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: platform specific
            data:  Example: platform specific"""
        ...

class _number_state(StateVal):
    max: int | float
    min: int | float
    mode: str
    restored: bool
    step: int | float
    supported_features: int
    unit_of_measurement: str

    def set_value(self, value: str):
        """

        Args:
            value:  Example: 42"""
        ...

    def min(self):
        """Set a number entity to its minimum value."""
        ...

    def max(self):
        """Set a number entity to its maximum value."""
        ...

    def decrement(self, amount: float | None):
        """Decrease a number entity value by a certain amount.

        Args:
            amount: The amount to decrease the number with. If not provided, the step of the number entity will be used."""
        ...

    def increment(self, amount: float | None):
        """Increase a number entity value by a certain amount.

        Args:
            amount: The amount to increase the number with. If not provided, the step of the number entity will be used."""
        ...

class number:
    boiler_expected_number_of_shower: _number_state
    boiler_target_temperature: _number_state
    boiler_water_target_temperature: _number_state
    valve_kitchen_eco_temperature: _number_state
    valve_kitchen_max_temperature: _number_state
    valve_kitchen_min_temperature: _number_state
    valve_kitchen_local_temperature_calibration: _number_state
    valve_kitchen_boost_heating_countdown_time_set: _number_state
    office_temphum_zb_temperature_calibration: _number_state
    office_temphum_zb_humidity_calibration: _number_state
    office_temphum_zb_comfort_temperature_min: _number_state
    office_temphum_zb_comfort_temperature_max: _number_state
    office_temphum_zb_comfort_humidity_min: _number_state
    office_temphum_zb_comfort_humidity_max: _number_state
    delta_pro_max_charge_level: _number_state
    delta_pro_min_discharge_level: _number_state
    delta_pro_backup_reserve_level: _number_state
    delta_pro_generator_auto_start_level: _number_state
    delta_pro_generator_auto_stop_level: _number_state
    delta_pro_ac_charging_power: _number_state
    delta_pro_api_ac_charging_power: _number_state
    delta_pro_api_backup_reserve_level: _number_state
    delta_pro_api_generator_auto_start_level: _number_state
    delta_pro_api_generator_auto_stop_level: _number_state
    delta_pro_api_max_charge_level: _number_state
    delta_pro_api_min_discharge_level: _number_state
    lumi_cn_132749107_v3_volume_p_3_2: _number_state
    ijai_de_1027836802_v3_volume_p_4_2: _number_state
    ijai_de_1027836802_v3_time_zone_p_7_20: _number_state
    ijai_de_1027836802_v3_order_id_p_8_1: _number_state
    ijai_de_1027836802_v3_day_p_8_3: _number_state
    ijai_de_1027836802_v3_hour_p_8_4: _number_state
    ijai_de_1027836802_v3_minute_p_8_5: _number_state
    ijai_de_1027836802_v3_mapid_p_8_11: _number_state
    ijai_de_1027836802_v3_room_count_p_8_12: _number_state
    ijai_de_1027836802_v3_time_zone_p_8_14: _number_state
    valve_office_local_temperature_calibration: _number_state
    valve_office_away_preset_days: _number_state
    valve_office_boost_time: _number_state
    valve_office_comfort_temperature: _number_state
    valve_office_eco_temperature: _number_state
    valve_office_max_temperature: _number_state
    valve_office_min_temperature: _number_state
    valve_office_away_preset_temperature: _number_state
    valve_room_local_temperature_calibration: _number_state
    valve_room_away_preset_days: _number_state
    valve_room_boost_time: _number_state
    valve_room_comfort_temperature: _number_state
    valve_room_eco_temperature: _number_state
    valve_room_max_temperature: _number_state
    valve_room_min_temperature: _number_state
    valve_room_away_preset_temperature: _number_state
    valve_bedroom_local_temperature_calibration: _number_state
    valve_bedroom_away_preset_days: _number_state
    valve_bedroom_boost_time: _number_state
    valve_bedroom_comfort_temperature: _number_state
    valve_bedroom_eco_temperature: _number_state
    valve_bedroom_max_temperature: _number_state
    valve_bedroom_min_temperature: _number_state
    valve_bedroom_away_preset_temperature: _number_state
    ijai_v3_4619_volume: _number_state
    lumi_v3_0661_volume: _number_state
    motion_cat_toilet_fading_time: _number_state
    motion_cat_toilet_static_detection_distance: _number_state
    motion_cat_toilet_static_detection_sensitivity: _number_state
    motion_cat_toilet_motion_detection_sensitivity: _number_state
    orbitrack_tl_timer: _number_state
    bedroom_entrance_delayed_power_on_time: _number_state
    washer_rinse_cycles: _number_state
    energy_monitoring_smartplug_timer: _number_state
    temphum_noscreen_1_temperature_calibration: _number_state
    temphum_noscreen_1_humidity_calibration: _number_state
    delta_pro_backup_reserve_level_2: _number_state
    delta_pro_api_backup_reserve_level_2: _number_state
    mijia_de_56078868_v1_image_rollover_p_2_2: _number_state
    motion_office_sun_fading_time: _number_state
    motion_office_sun_static_detection_distance: _number_state
    motion_office_sun_static_detection_sensitivity: _number_state
    motion_office_sun_motion_detection_sensitivity: _number_state
    music_assistant_jukebox_jukebox_queue_length: _number_state
    music_assistant_jukebox_jukebox_queuing_delay: _number_state
    bathroom_vents_delayed_power_on_time: _number_state
    delta_pro_api_remaining_charge_time: _number_state
    delta_pro_api_dynamic_charging_speed: _number_state
    bathroom_led_countdown: _number_state
    bedroom_led_countdown_l1: _number_state
    bedroom_led_countdown_l2: _number_state
    bathroom_floor_cl_temperature: _number_state
    office_motion_cat_mat_fading_time: _number_state
    office_motion_cat_mat_static_detection_distance: _number_state
    office_motion_cat_mat_static_detection_sensitivity: _number_state
    office_motion_cat_mat_motion_detection_sensitivity: _number_state

    @staticmethod
    def set_value(*, entity_id: str, value: str):
        """

        Args:
            entity_id: Entity ID
            value:  Example: 42"""
        ...

    @staticmethod
    def min(*, entity_id: str):
        """Set a number entity to its minimum value.

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def max(*, entity_id: str):
        """Set a number entity to its maximum value.

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def decrement(*, entity_id: str, amount: float | None=None):
        """Decrease a number entity value by a certain amount.

        Args:
            entity_id: Entity ID
            amount: The amount to decrease the number with. If not provided, the step of the number entity will be used."""
        ...

    @staticmethod
    def increment(*, entity_id: str, amount: float | None=None):
        """Increase a number entity value by a certain amount.

        Args:
            entity_id: Entity ID
            amount: The amount to increase the number with. If not provided, the step of the number entity will be used."""
        ...

class onedrive:

    @staticmethod
    def upload(*, config_entry_id: str, destination_folder: str, filename: Any | None=None) -> dict[str, Any]:
        ...

class openweathermap:

    @staticmethod
    def get_minute_forecast(*, entity_id: str) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID"""
        ...

class persistent_notification:

    @staticmethod
    def create(*, message: str, title: str | None=None, notification_id: str | None=None):
        """

        Args:
            message:  Example: Please check your configuration.yaml.
            title:  Example: Test notification
            notification_id:  Example: 1234"""
        ...

    @staticmethod
    def dismiss(*, notification_id: str):
        """

        Args:
            notification_id:  Example: 1234"""
        ...

    @staticmethod
    def dismiss_all():
        ...

class _person_state(StateVal):
    device_trackers: list
    editable: bool
    entity_picture: str
    gps_accuracy: int
    id: str
    latitude: float
    longitude: float
    source: str
    user_id: str

class person:
    catbird: _person_state
    alert: _person_state
    ma3a: _person_state
    kiosk: _person_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def remove_device_tracker(*, entity_id: str, device_tracker: str):
        """Remove a device tracker from a person.

        Args:
            entity_id: The person entity ID to remove the device tracker from.
            device_tracker: The device tracker entity ID to remove from the person."""
        ...

    @staticmethod
    def add_device_tracker(*, entity_id: str, device_tracker: str):
        """Add a device tracker to a person.

        Args:
            entity_id: The person entity ID to add the device tracker to.
            device_tracker: The device tracker entity ID to add to the person."""
        ...

class pi_hole:

    @staticmethod
    def disable(*, entity_id: str, duration: str):
        """

        Args:
            entity_id: Entity ID
            duration:  Example: 00:00:15"""
        ...

class pyscript:

    @staticmethod
    def wipe_callbacks(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function wipe_callbacks()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def broadcast(*, message: str='test message', player_ids: str='media_player.all_speakers', language: str='en'):
        """broadcasts message

        Args:
            message: message Example: message
            player_ids: player ids Example: media_player.office_speaker
            language: language Example: en"""
        ...

    @staticmethod
    def broadcast_urgent(*, message: str='test message', player_ids: str='media_player.all_speakers', language: str='en'):
        """broadcasts despite quiet hour

        Args:
            message: message Example: message
            player_ids: player ids Example: media_player.office_speaker
            language: language Example: en"""
        ...

    @staticmethod
    def broadcast_optional(*, message: str='test message', player_ids: str='media_player.all_speakers', language: str='en', pre_sound=None, post_sound=None, timeout_before=None):
        """broadcasts if not quiet hour

        Args:
            message: message Example: message
            player_ids: player ids Example: media_player.office_speaker
            language: language Example: en"""
        ...

    @staticmethod
    def tryouts(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function tryouts()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def air_quality_notification(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function air_quality_notification()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def alert_server_off_scenario(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function alert_server_off_scenario()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def alert_server_on_scenario(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function alert_server_on_scenario()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def chore_notifier(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """{'assignment_config': '1',
 'assignment_type': 'in-alphabetical-order',
 'description': 'test description',
 'id': 3,
 'last_done_by': {'display_name': 'ALERT',
                  'first_name': None,
                  'id': 1,
                  'last_name': None,
                  'username': 'ALERT'},
 'last_tracked_time': '2025-04-02T12:51:46',
 'name': 'test name',
 'next_estimated_execution_time': '2025-04-02T13:51:46',
 'next_execution_assigned_to_user_id': 1,
 'next_execution_assigned_user': {'display_name': 'ALERT',
                                  'first_name': None,
                                  'id': 1,
                                  'last_name': None,
                                  'username': 'ALERT'},
 'period_config': None,
 'period_days': 0,
 'period_type': 'hourly',
 'rollover': False,
 'track_count': 0,
 'track_date_only': False,
 'userfields': None}

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def scene_coffee():
        """pyscript function scene_coffee()"""
        ...

    @staticmethod
    def cron_office_hourly(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function cron_office_hourly()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def disable_disabled_devices():
        """pyscript function disable_disabled_devices()"""
        ...

    @staticmethod
    def ecoflow_set_dynamic_charging_speed(*, ecoflow_battery_level_sensor: Literal['', 'turn_on', 'fire'] | None=None, id_: str | None=None):
        """Sets the ecoflow charging speed according to the next outage.

        Args:
            ecoflow_battery_level_sensor: ecoflow_battery_level_sensor Entity ID
            id_: id of light, or name of event to fire Example: kitchen.light"""
        ...

    @staticmethod
    def entity_library_service(*, action=None, id_=None):
        """pyscript function entity_library_service()

        Args:
            action: argument action
            id_: argument id_"""
        ...

    @staticmethod
    def music_all():
        """pyscript function music_all()"""
        ...

    @staticmethod
    def music_shower():
        """pyscript function music_shower()"""
        ...

    @staticmethod
    def music_relax():
        """pyscript function music_relax()"""
        ...

    @staticmethod
    def music_funky():
        """pyscript function music_funky()"""
        ...

    @staticmethod
    def music_next():
        """pyscript function music_next()"""
        ...

    @staticmethod
    def music_best():
        """pyscript function music_best()"""
        ...

    @staticmethod
    def music_album():
        """pyscript function music_album()"""
        ...

    @staticmethod
    def music_artist():
        """pyscript function music_artist()"""
        ...

    @staticmethod
    def morning_greeting(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function morning_greeting()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def movie_time(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """movie_time:
  alias: Movie Time
  sequence:
    - action: scene.turn_on
      target:
        entity_id: scene.projector_on

    - action: media_player.turn_on
      target:
        entity_id: media_player.kitchen_tv_wifi

    - action: media_player.media_pause
      target:
        entity_id: media_player.all_speakers

    - action: light.turn_off
      target:
        area_id:
          - hallway
          - bedroom
          - room
          - office
          - shower
          - bathroom

    - action: light.turn_off
      target:
        entity_id:
          - light.kitchen
          - light.couch
          - light.couch_reading

    - action: media_player.volume_set
      target:
        entity_id: media_player.kitchen_tv_wifi
      data:
        volume_level: 0.5

    - action: media_player.volume_up
      target:
        entity_id: media_player.kitchen_tv_wifi

    - delay: 20

    - action: light.turn_off
      target:
        area_id:
          - kitchen

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def power_off_scenario(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function power_off()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def power_on_scenario(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function power_on()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def new_power_outage_calendar(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function new_power_outage_calendar()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def router_reboot():
        """pyscript function router_reboot()"""
        ...

    @staticmethod
    def entities_toggle_test(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function entities_toggle_test()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def test_last_active(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function test_last_active()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def speak(*, message: str='test message', player_ids: str | None=None, language: str='en'):
        """speak message

        Args:
            message: message Example: message
            player_ids: player ids Example: media_player.office_speaker
            language: language Example: en"""
        ...

    @staticmethod
    def vacuum_service_time_update(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """pyscript function vacuum_service_p_update()

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def rain_incoming(*, trigger_type=None, var_name=None, value=None, old_value=None, context=None):
        """{
    'weather.openweathermap': {
        'forecast': [
            {
                'apparent_temperature': 22.1,
                'cloud_coverage': 100,
                'condition': 'rainy',
                'datetime': '2025-06-27T15:00:00+00:00',
                'dew_point': 14.8,
                'humidity': 63,
                'precipitation': 0.28,
                'precipitation_probability': 51,
                'pressure': 1011.0,
                'temperature': 22.2,
                'uv_index': 0.8,
                'wind_bearing': 59,
                'wind_gust_speed': 7.16,
                'wind_speed': 3.92
            },
            {
                'apparent_temperature': 21.6,
                'cloud_coverage': 100,
                'condition': 'cloudy',
                'datetime': '2025-06-27T16:00:00+00:00',
                'dew_point': 14.8,
                'humidity': 65,
                'precipitation': 0.0,
                'precipitation_probability': 64,
                'pressure': 1011.0,
                'temperature': 21.6,
                'uv_index': 0.39,
                'wind_bearing': 149,
                'wind_gust_speed': 11.84,
                'wind_speed': 5.0
            },
        ]
    }
}

        Args:
            trigger_type: argument trigger_type
            var_name: argument var_name
            value: argument value
            old_value: argument old_value
            context: argument context"""
        ...

    @staticmethod
    def win11_vm_service(*, start: bool='true'):
        """Windows 11 VM start/stop

        Args:
            start: whether to start a vm or shut it down Example: true"""
        ...

    @staticmethod
    def alert_server_wake():
        """Wakes Alert Server"""
        ...

    @staticmethod
    def alert_server_shutdown():
        """Shuts down Alert Server"""
        ...

    @staticmethod
    def reload(*, global_ctx: str | None=None):
        """Reloads all available pyscripts and restart triggers

        Args:
            global_ctx: Only reload this specific global context (file or app) Example: file.example"""
        ...

    @staticmethod
    def generate_stubs() -> dict[str, Any]:
        """Build a stub files combining builtin helpers with discovered entities and services."""
        ...

    @staticmethod
    def jupyter_kernel_start(*, key: str, kernel_name: str='pyscript', shell_port: int | None=None, iopub_port: int | None=None, stdin_port: int | None=None, control_port: int | None=None, hb_port: int | None=None, ip: str='127.0.0.1', transport: Literal['', 'tcp', 'udp']='tcp', signature_scheme: Literal['', 'hmac-sha256']='hmac-sha256'):
        """Starts a jupyter kernel for interactive use; Called by Jupyter front end and should generally not be used by users

        Args:
            key: Used for signing Example: 012345678-9abcdef023456789abcdef
            kernel_name: Kernel name Example: pyscript
            shell_port: Shell port number Example: 63599
            iopub_port: IOPub port number Example: 63598
            stdin_port: Stdin port number Example: 63597
            control_port: Control port number Example: 63596
            hb_port: Heartbeat port number Example: 63595
            ip: IP address to connect to Jupyter front end Example: 127.0.0.1
            transport: Transport type Example: tcp
            signature_scheme: Signing algorithm Example: hmac-sha256"""
        ...

class recorder:

    @staticmethod
    def purge(*, keep_days: int | None=None, repack: bool=False, apply_filter: bool=False):
        ...

    @staticmethod
    def purge_entities(*, entity_id: str | None=None, domains: Any | None=None, entity_globs: Any | None=None, keep_days: int=0):
        """

        Args:
            domains:  Example: sun
            entity_globs:  Example: domain*.object_id*"""
        ...

    @staticmethod
    def enable():
        ...

    @staticmethod
    def disable():
        ...

    @staticmethod
    def get_statistics(*, start_time: datetime, statistic_ids, period: Literal['', '5minute', 'hour', 'day', 'week', 'month'], types: Literal['', 'change', 'last_reset', 'max', 'mean', 'min', 'state', 'sum'], end_time: datetime | None=None, units: Any | None=None) -> dict[str, Any]:
        """

        Args:
            start_time:  Example: 2025-01-01 00:00:00
            statistic_ids:  Example: ['sensor.energy_consumption', 'sensor.temperature']
            period:  Example: hour
            types:  Example: ['mean', 'sum']
            end_time:  Example: 2025-01-02 00:00:00
            units:  Example: {'energy': 'kWh', 'temperature': '°C'}"""
        ...

    @staticmethod
    def import_statistics(*, statistic_id: str, source: str, has_mean: bool, has_sum: bool, stats: Any, name: str | None=None, unit_of_measurement: str | None=None):
        """Import long-term statistics.

        Args:
            statistic_id: The statistics ID (entity ID) to import for.
            source: The source of the statistics data.
            has_mean: If the statistics has a mean value.
            has_sum: If the statistics has a sum value.
            stats: A list of mappings/dictionaries with statistics to import. The dictionaries must contain a "start" key with a datetime string other valid options are "mean", "sum", "min", "max", "last_reset", and "state". All of those are optional and either an integer or a float, except for "last_reset" which is a datetime string.
            name: The name of the statistics.
            unit_of_measurement: The unit of measurement of the statistics."""
        ...

class _remote_state(StateVal):
    activity_list: list
    current_activity: str
    supported_features: int

    def turn_off(self):
        ...

    def turn_on(self, activity: str | None):
        """

        Args:
            activity:  Example: BedroomTV"""
        ...

    def toggle(self):
        ...

    def send_command(self, *, command: Any, device: str | None=None, num_repeats: int=1, delay_secs: int=0.4, hold_secs: int=0):
        """

        Args:
            command:  Example: Play
            device:  Example: 32756745"""
        ...

    def learn_command(self, *, device: str | None=None, command: Any | None=None, command_type: Literal['', 'ir', 'rf']='ir', alternative: bool | None=None, timeout: int | None=None):
        """

        Args:
            device:  Example: television
            command:  Example: Turn on"""
        ...

    def delete_command(self, *, command: Any, device: str | None=None):
        """

        Args:
            command:  Example: Mute
            device:  Example: television"""
        ...

class remote:
    sonoff_10009b4ac7: _remote_state
    kitchen_tv_wifi: _remote_state
    projector_custom_projector_custom: _remote_state
    kitchen_vents_kitchen_vents: _remote_state
    projector_projector: _remote_state

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_on(*, entity_id: str, activity: str | None=None):
        """

        Args:
            entity_id: Entity ID
            activity:  Example: BedroomTV"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def send_command(*, entity_id: str, command: Any, device: str | None=None, num_repeats: int=1, delay_secs: int=0.4, hold_secs: int=0):
        """

        Args:
            entity_id: Entity ID
            command:  Example: Play
            device:  Example: 32756745"""
        ...

    @staticmethod
    def learn_command(*, entity_id: str, device: str | None=None, command: Any | None=None, command_type: Literal['', 'ir', 'rf']='ir', alternative: bool | None=None, timeout: int | None=None):
        """

        Args:
            entity_id: Entity ID
            device:  Example: television
            command:  Example: Turn on"""
        ...

    @staticmethod
    def delete_command(*, entity_id: str, command: Any, device: str | None=None):
        """

        Args:
            entity_id: Entity ID
            command:  Example: Mute
            device:  Example: television"""
        ...

class repairs:

    @staticmethod
    def create(*, title: str, description: str, issue_id: str | None=None, domain: str | None=None, severity: Literal['', 'warning', 'error', 'critical'] | None=None, persistent: bool | None=None):
        """Manually create and raise a issue in Home Assistant repairs.

        Args:
            title: The title of the issue.
            description: The description of the issue. Supports Markdown.
            issue_id: The issue can have an identifier, which allows you to cancel it later with that ID if needed. It also prevent duplicate issues to be created. If not provided, a random ID will be generated.
            domain: This field can be used to set the domain of the issue. For example, by default (if not set), it will use "spook". This causes Spook to be shown in the logo/image of the issue. If you set it to "homeassistant", the Home Assistant logo will be used, or use "hue", "zwave_js", "mqtt", etc. to use the logo of that integration.
            severity: The severity of the issue. This will be used to determine the priority of the issue. If not set, "warning" will be used
            persistent: If the issue should be persistent, which means it will survive restarts of Home Assistant. By default, issues are not persistent."""
        ...

    @staticmethod
    def remove(*, issue_id: str):
        """Removes a manually created Home Assistant repairs issue. This action can only remove issues created with the `repairs_create` action.

        Args:
            issue_id: The issue ID to remove."""
        ...

    @staticmethod
    def unignore_all():
        """Unignore all issues currently raised in Home Assistant Repairs."""
        ...

    @staticmethod
    def ignore_all():
        """Ignore all issues currently raised in Home Assistant Repairs."""
        ...

class rest:

    @staticmethod
    def reload():
        ...

class rest_command:

    @staticmethod
    def pihole_login() -> dict[str, Any]:
        ...

    @staticmethod
    def pihole_logout() -> dict[str, Any]:
        ...

    @staticmethod
    def pihole_set_blocking() -> dict[str, Any]:
        ...

    @staticmethod
    def reload():
        ...

class _scene_state(StateVal):
    id: str
    restored: bool
    supported_features: int

    def delete(self):
        ...

    def turn_on(self, transition: int | None):
        ...

class scene:
    room_window_open: _scene_state
    catbird_asleep: _scene_state
    catbird_awake: _scene_state
    new_scene: _scene_state
    projector_off: _scene_state
    projector_on: _scene_state

    @staticmethod
    def reload():
        ...

    @staticmethod
    def apply(*, entities: Any, transition: int | None=None):
        """

        Args:
            entities:  Example: light.kitchen: "on"
                light.ceiling:
                  state: "on"
                  brightness: 80
                """
        ...

    @staticmethod
    def create(*, scene_id: str, entities: Any | None=None, snapshot_entities: str | None=None):
        """

        Args:
            scene_id:  Example: all_lights
            entities:  Example: light.tv_back_light: "on"
                light.ceiling:
                  state: "on"
                  brightness: 200
                
            snapshot_entities:  Example: - light.ceiling
                - light.kitchen
                """
        ...

    @staticmethod
    def delete(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_on(*, entity_id: str, transition: int | None=None):
        """

        Args:
            entity_id: Entity ID"""
        ...

class schedule:

    @staticmethod
    def reload():
        ...

    @staticmethod
    def get_schedule(*, entity_id: str) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID"""
        ...

class scheduler:

    @staticmethod
    def run_action(*, entity_id: str, time: str | None=None, skip_conditions: bool | None=None):
        """Execute the action of a schedule, optionally at a given time.

        Args:
            entity_id: Identifier of the scheduler entity. Example: switch.schedule_abcdef
            time: Time for which to evaluate the action (only useful for schedules with multiple timeslot) Example: "12:00"
            skip_conditions: Whether the conditions of the schedule should be skipped or not"""
        ...

    @staticmethod
    def add(*, timeslots: Any, repeat_type: Literal['', 'repeat', 'single', 'pause'], weekdays: Any | None=None, start_date: Any | None=None, end_date: Any | None=None, name: str | None=None):
        """Create a new schedule entity

        Args:
            timeslots: list of timeslots with their actions and optionally conditions (should be kept the same for all timeslots) Example: [{start: "12:00", stop: "13:00", actions: [{service: "light.turn_on", entity_id: "light.my_lamp", service_data: {brightness: 200}}]}]
            repeat_type: Control what happens after the schedule is triggered Example: "repeat"
            weekdays: Days of the week for which the schedule should be repeated Example: ["daily"]
            start_date: Date from which schedule should be executed Example: ["2021-01-01"]
            end_date: Date until which schedule should be executed Example: ["2021-12-31"]
            name: Friendly name for the schedule Example: My schedule"""
        ...

    @staticmethod
    def edit(*, entity_id: str, weekdays: Any | None=None, start_date: Any | None=None, end_date: Any | None=None, timeslots: Any | None=None, repeat_type: Literal['', 'repeat', 'single', 'pause'] | None=None, name: str | None=None):
        """Edit a schedule entity

        Args:
            entity_id: Identifier of the scheduler entity. Example: switch.schedule_abcdef
            weekdays: Days of the week for which the schedule should be repeated Example: ["daily"]
            start_date: Date from which schedule should be executed Example: ["2021-01-01"]
            end_date: Date until which schedule should be executed Example: ["2021-12-31"]
            timeslots: list of timeslots with their actions and optionally conditions (should be kept the same for all timeslots) Example: [{start: "12:00", stop: "13:00", actions: [{service: "light.turn_on", entity_id: "light.my_lamp", service_data: {brightness: 200}}]}]
            repeat_type: Control what happens after the schedule is triggered Example: "repeat"
            name: Friendly name for the schedule Example: My schedule"""
        ...

    @staticmethod
    def remove(*, entity_id: str):
        """Remove a schedule entity

        Args:
            entity_id: Identifier of the scheduler entity. Example: switch.schedule_abcdef"""
        ...

    @staticmethod
    def copy(*, entity_id: str, name: str | None=None):
        """Duplicate a schedule entity

        Args:
            entity_id: Identifier of the scheduler entity. Example: switch.schedule_abcdef
            name: Friendly name for the copied schedule Example: My schedule"""
        ...

    @staticmethod
    def disable_all():
        """Disables all schedules"""
        ...

    @staticmethod
    def enable_all():
        """Enables all schedules"""
        ...

class _script_state(StateVal):
    current: int
    last_triggered: datetime
    mode: str
    restored: bool
    supported_features: int

    def turn_on(self):
        ...

    def turn_off(self):
        ...

    def toggle(self):
        ...

class script:
    check_config: _script_state
    reload_config: _script_state
    hass_restart: _script_state
    zigbee_permit: _script_state
    next_song: _script_state
    audio_alerts_actualize: _script_state
    speakers_volume_loud: _script_state
    speakers_volume_normal: _script_state
    speakers_volume_silent: _script_state
    router_reboot: _script_state
    router_reboot_ssh: _script_state
    catbird_sleep_toggle: _script_state
    pi_hole_disable: _script_state
    pi_hole_enable: _script_state

    @staticmethod
    def router_reboot() -> dict[str, Any]:
        ...

    @staticmethod
    def check_config() -> dict[str, Any]:
        ...

    @staticmethod
    def reload_config() -> dict[str, Any]:
        ...

    @staticmethod
    def hass_restart() -> dict[str, Any]:
        ...

    @staticmethod
    def zigbee_permit() -> dict[str, Any]:
        ...

    @staticmethod
    def next_song() -> dict[str, Any]:
        ...

    @staticmethod
    def pi_hole_disable() -> dict[str, Any]:
        ...

    @staticmethod
    def pi_hole_enable() -> dict[str, Any]:
        ...

    @staticmethod
    def speakers_volume_loud() -> dict[str, Any]:
        ...

    @staticmethod
    def speakers_volume_normal() -> dict[str, Any]:
        ...

    @staticmethod
    def speakers_volume_silent() -> dict[str, Any]:
        ...

    @staticmethod
    def router_reboot_ssh() -> dict[str, Any]:
        ...

    @staticmethod
    def reload():
        ...

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class _select_state(StateVal):
    id: str
    integration: str
    options: list
    restored: bool
    supported_features: int

    def select_first(self):
        ...

    def select_last(self):
        ...

    def select_next(self, cycle: bool):
        ...

    def select_option(self, option: str):
        '''

        Args:
            option:  Example: "Item A"'''
        ...

    def select_previous(self, cycle: bool):
        ...

    def random(self, options: Any | None):
        """Select an random option for a select entity.

        Args:
            options: Limits the options to select from. If not provided, all options will be considered."""
        ...

class select:
    ijai_v3_4619_mode: _select_state
    ijai_v3_4619_sweep_type: _select_state
    ijai_v3_4619_water_state: _select_state
    office_window_lt_direction: _select_state
    office_window_lt_motor_mode: _select_state
    bedroom_window_lt_direction: _select_state
    bedroom_window_lt_motor_mode: _select_state
    room_window_lt_direction: _select_state
    room_window_lt_motor_mode: _select_state
    kitchen_window_lt_direction: _select_state
    kitchen_window_lt_motor_mode: _select_state
    zigbee2mqtt_bridge_log_level_2: _select_state
    office_temphum_zb_temperature_display_mode: _select_state
    socket_cat_mat_power_outage_memory: _select_state
    socket_cat_mat_indicator_mode: _select_state
    projector_socket_power_outage_memory: _select_state
    projector_socket_indicator_mode: _select_state
    delta_pro_dc_12v_charge_current: _select_state
    delta_pro_screen_timeout: _select_state
    delta_pro_unit_timeout: _select_state
    delta_pro_ac_timeout: _select_state
    delta_pro_api_ac_timeout: _select_state
    delta_pro_api_dc_12v_charge_current: _select_state
    delta_pro_api_screen_timeout: _select_state
    delta_pro_api_unit_timeout: _select_state
    shower_vents_power_on_behavior: _select_state
    shower_vents_switch_type: _select_state
    ijai_de_1027836802_v3_mode_p_2_4: _select_state
    ijai_de_1027836802_v3_sweep_type_p_2_8: _select_state
    ijai_de_1027836802_v3_alarm_p_4_1: _select_state
    ijai_de_1027836802_v3_repeat_state_p_7_1: _select_state
    ijai_de_1027836802_v3_suction_state_p_7_5: _select_state
    ijai_de_1027836802_v3_water_state_p_7_6: _select_state
    ijai_de_1027836802_v3_mop_route_p_7_7: _select_state
    ijai_de_1027836802_v3_direction_p_7_16: _select_state
    ijai_de_1027836802_v3_tank_shake_p_7_48: _select_state
    ijai_de_1027836802_v3_shake_shift_p_7_50: _select_state
    ijai_de_1027836802_v3_enable_p_8_2: _select_state
    ijai_de_1027836802_v3_repeat_p_8_6: _select_state
    ijai_de_1027836802_v3_clean_way_p_8_7: _select_state
    ijai_de_1027836802_v3_suction_p_8_8: _select_state
    ijai_de_1027836802_v3_water_p_8_9: _select_state
    ijai_de_1027836802_v3_twice_clean_p_8_10: _select_state
    ijai_de_1027836802_v3_remember_state_p_10_1: _select_state
    ijai_de_1027836802_v3_map_uploads_p_10_23: _select_state
    valve_office_force: _select_state
    valve_office_week: _select_state
    valve_room_force: _select_state
    valve_room_week: _select_state
    valve_bedroom_force: _select_state
    valve_bedroom_week: _select_state
    valve_cold_power_on_behavior: _select_state
    valve_cold_indicator_mode: _select_state
    motion_cat_toilet_motion_detection_mode: _select_state
    orbitrack_tl_initial_state: _select_state
    orbitrack_tl_light: _select_state
    ijai_v3_4619_suction_state: _select_state
    bedroom_entrance_power_on_behavior: _select_state
    bedroom_entrance_external_trigger_mode: _select_state
    washer: _select_state
    energy_monitoring_smartplug_initial_state: _select_state
    energy_monitoring_smartplug_light_mode: _select_state
    gaggiuino_profile: _select_state
    a1_slwf_03_voice_assistant_assistant: _select_state
    a1_slwf_03_voice_assistant_finished_speaking_detection: _select_state
    a1_slwf_03_voice_assistant_wake_word: _select_state
    washer_spin_level: _select_state
    orbitrack_tl_light_mode: _select_state
    temphum_noscreen_1_temperature_unit: _select_state
    mijia_de_56078868_v1_night_shot_p_2_3: _select_state
    motion_office_sun_motion_detection_mode: _select_state
    a1_slwf_03_voice_assistant_assistant_2: _select_state
    a1_slwf_03_voice_assistant_wake_word_2: _select_state
    dahua_vto_dahua_preset_position: _select_state
    bathroom_vents_power_on_behavior: _select_state
    bathroom_vents_external_trigger_mode: _select_state
    bathroom_led_switch_type: _select_state
    bathroom_led_power_on_behavior: _select_state
    bedroom_led_switch_type_l1: _select_state
    bedroom_led_switch_type_l2: _select_state
    bedroom_led_power_on_behavior: _select_state
    room_accent_light_power_outage_memory: _select_state
    room_accent_light_indicator_mode: _select_state
    office_window_cloud_motor_mode_2: _select_state
    room_window_cloud_motor_mode_3: _select_state
    bedroom_window_cloud_motor_mode_2: _select_state
    kitchen_window_cloud_motor_mode_2: _select_state
    socket_random_cloud_power_on_behavior: _select_state
    delta_2_plug_power_on_behavior_3: _select_state
    delta_2_plug_indicator_light_mode_2: _select_state
    laundry_optional_power_on_behavior_3: _select_state
    laundry_optional_indicator_light_mode_2: _select_state
    orbitrack_power_on_behavior_3: _select_state
    office_motion_cat_mat_motion_detection_mode: _select_state

    @staticmethod
    def select_first(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def select_last(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def select_next(*, entity_id: str, cycle: bool=True):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def select_option(*, entity_id: str, option: str):
        '''

        Args:
            entity_id: Entity ID
            option:  Example: "Item A"'''
        ...

    @staticmethod
    def select_previous(*, entity_id: str, cycle: bool=True):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def random(*, entity_id: str, options: Any | None=None):
        """Select an random option for a select entity.

        Args:
            entity_id: Entity ID
            options: Limits the options to select from. If not provided, all options will be considered."""
        ...

class _sensor_state(StateVal):
    Confidence: str
    Country: str
    Locality: str
    Location: list
    Name: str
    Ocean: str
    SN: str
    Thoroughfare: str
    Types: list
    Zones: list
    administrative_area: str
    attribution: str
    available: int
    battery_last_reported: datetime
    battery_last_reported_level: int
    battery_level: int
    battery_low: bool
    battery_low_threshold: int | float
    battery_quantity: int | str
    battery_type: str
    battery_type_and_quantity: str
    bytes_received: int
    bytes_sent: int
    calculation_method: str
    calibration: int
    chores: list
    city: str
    comfort_description: str
    comfort_explanation: str
    comfort_level: str
    count: int
    country: str
    current: float
    current_state: str
    data_last_update: str
    device_id: str
    device_name: str
    event_end: Any
    event_start: Any
    event_type: str
    free: int
    humidity: float
    humidity_unit: str
    id: str
    is_comfortable: bool
    is_hidden: bool
    is_outdoor: bool
    iso_country_code: str
    label: str
    last_data_change: Any
    last_entity_id: str
    last_reset: str
    latitude: float
    locality: str
    location: list
    longitude: float
    metered: bool
    mqtt_connected: bool
    name: str
    options: list
    phone: str
    postal_code: str
    premises: str
    pressure: float
    pressure_unit: str
    quota_requests: int
    restored: bool
    server_country: str
    server_id: str
    server_location: str
    server_name: str
    source_entity_id: str
    state_class: str
    station_name: str
    sub_administrative_area: str
    sub_locality: str
    sub_thoroughfare: str
    supported_features: int
    supported_states: list
    switch: bool
    temperature: float
    temperature_unit: str
    thoroughfare: str
    time_of_day: str
    timestamp: str
    total: int
    unit_of_measurement: str
    updated: str
    url: str
    used: int
    voltage: float
    wind_speed: float
    wind_speed_unit: str

class sensor:
    local_ip: _sensor_state
    disk_use_percent: _sensor_state
    disk_free: _sensor_state
    memory_use_percent: _sensor_state
    swap_use: _sensor_state
    processor_use: _sensor_state
    load_1m: _sensor_state
    load_5m: _sensor_state
    load_15m: _sensor_state
    last_boot: _sensor_state
    memory_use: _sensor_state
    bathroom_humidity: _sensor_state
    bathroom_temperature: _sensor_state
    bathroom_temperature_humidity_sensor_battery: _sensor_state
    shower_temperature: _sensor_state
    miaomiaoce_t2_ce25_battery_level: _sensor_state
    miot_ble_room_temperature: _sensor_state
    miot_ble_room_humidity: _sensor_state
    mop_p_message: _sensor_state
    shower_humidity_miot: _sensor_state
    miaomiaoce_t2_b5ef_temperature_humidity_sensor: _sensor_state
    miaomiaoce_t2_b5ef_battery_level: _sensor_state
    miaomiaoce_t2_b5ef_relative_humidity: _sensor_state
    mi_flood_detector_battery: _sensor_state
    mi_flood_detector_voltage: _sensor_state
    speedtest_ping: _sensor_state
    speedtest_download: _sensor_state
    speedtest_upload: _sensor_state
    mi_flood_detector_battery_2: _sensor_state
    mi_flood_detector_voltage_2: _sensor_state
    bathroom_temphum_battery: _sensor_state
    bathroom_temphum_humidity_2: _sensor_state
    bathroom_temphum_temperature_2: _sensor_state
    bathroom_temphum_voltage: _sensor_state
    shower_temphum_humidity: _sensor_state
    shower_temphum_temperature: _sensor_state
    mi_flood_detector_battery_3: _sensor_state
    mi_flood_detector_voltage_3: _sensor_state
    mi_flood_detector_battery_4: _sensor_state
    mi_flood_detector_voltage_4: _sensor_state
    shower_humidity_latest: _sensor_state
    office_temperature_latest: _sensor_state
    office_humidity_latest: _sensor_state
    shower_temperature_latest: _sensor_state
    laundry_humidity_latest: _sensor_state
    laundry_temperature_latest: _sensor_state
    ijai_v3_4619_side_brush_life: _sensor_state
    ijai_v3_4619_main_brush_life: _sensor_state
    ijai_v3_4619_hypa_life: _sensor_state
    ijai_v3_4619_mop_life: _sensor_state
    ijai_v3_4619_battery_level: _sensor_state
    mop_2_pro_status: _sensor_state
    home_assistant_core_memory_percent: _sensor_state
    home_assistant_host_disk_free: _sensor_state
    sun_next_dawn: _sensor_state
    sun_next_dusk: _sensor_state
    sun_next_midnight: _sensor_state
    sun_next_noon: _sensor_state
    sun_next_rising: _sensor_state
    sun_next_setting: _sensor_state
    miaomiaoce_t2_b99d_temperature_humidity_sensor: _sensor_state
    miaomiaoce_t2_b99d_battery_level: _sensor_state
    miaomiaoce_t2_b99d_relative_humidity: _sensor_state
    flood_1_miot_battery_battery_level: _sensor_state
    flood_2_miot_battery_battery_level: _sensor_state
    flood_3_miot_battery_battery_level: _sensor_state
    flood_4_miot_battery_battery_level: _sensor_state
    shower_air_meter_miot_battery: _sensor_state
    alert: _sensor_state
    alert_2_4g: _sensor_state
    vacuum_map_build_map: _sensor_state
    vacuum_vacuum_fault: _sensor_state
    vacuum_map_remember_state: _sensor_state
    vacuum_map_cur_map_id: _sensor_state
    vacuum_map_map_num: _sensor_state
    vacuum_map_build_map_2: _sensor_state
    vacuum_map_has_new_map: _sensor_state
    u6_lite_uptime: _sensor_state
    u6_pro_uptime: _sensor_state
    room_temperature_latest: _sensor_state
    room_humidity_latest: _sensor_state
    kitchen_temperature_latest: _sensor_state
    kitchen_humidity_latest: _sensor_state
    miaomiaoce_t2_7360_temperature_humidity_sensor: _sensor_state
    miaomiaoce_t2_7360_battery_level: _sensor_state
    miaomiaoce_t2_7360_relative_humidity: _sensor_state
    mi_1621319031_474001000930_scene_history: _sensor_state
    mi_1621319031_474001004679_scene_history: _sensor_state
    bedroom_temperature_latest: _sensor_state
    bedroom_humidity_latest: _sensor_state
    bedroom_tvoc_latest: _sensor_state
    bedroom_co2_latest: _sensor_state
    bedroom_pm25_latest: _sensor_state
    bedroom_pm10_latest: _sensor_state
    xiaomi_wireless_button_1_battery_type: _sensor_state
    xiaomi_wireless_button_2_battery_type: _sensor_state
    water_leak_sensor_battery_type: _sensor_state
    water_leak_sensor_battery_type_2: _sensor_state
    water_leak_sensor_battery_type_3: _sensor_state
    valve_kitchen_battery_type: _sensor_state
    bedroom_window_lt_situation: _sensor_state
    room_window_lt_situation: _sensor_state
    kitchen_window_lt_situation: _sensor_state
    xiaomi_wireless_button_1_battery_last_replaced: _sensor_state
    xiaomi_wireless_button_2_battery_last_replaced: _sensor_state
    water_leak_sensor_battery_last_replaced: _sensor_state
    water_leak_sensor_battery_last_replaced_2: _sensor_state
    water_leak_sensor_battery_last_replaced_3: _sensor_state
    valve_kitchen_battery_last_replaced: _sensor_state
    u6_lite_state: _sensor_state
    u6_pro_state: _sensor_state
    bathroom_temperature_latest: _sensor_state
    bathroom_humidity_latest: _sensor_state
    office_co2_latest: _sensor_state
    valve_bedroom_battery_type: _sensor_state
    valve_bedroom_battery_last_replaced: _sensor_state
    valve_office_battery_type: _sensor_state
    valve_office_battery_last_replaced: _sensor_state
    valve_room_battery_type: _sensor_state
    valve_room_battery_last_replaced: _sensor_state
    xiaomi_wireless_button_2_battery_plus: _sensor_state
    valve_kitchen_battery_plus: _sensor_state
    office_temphum_zb_battery_plus: _sensor_state
    ttgo_noscreen_ip: _sensor_state
    ttgo_noscreen_last_restart_time: _sensor_state
    ttgo_noscreen_wifi_connect_count: _sensor_state
    ttgo_noscreen_mqtt_connect_count: _sensor_state
    ttgo_noscreen_restart_reason: _sensor_state
    ttgo_noscreen_ssid: _sensor_state
    door_last_restart_time: _sensor_state
    door_mqtt_connect_count: _sensor_state
    door_restart_reason: _sensor_state
    door_ssid: _sensor_state
    door_wifi_connect_count: _sensor_state
    alert_s_s24_ringer_mode: _sensor_state
    alert_s_s24_battery_level: _sensor_state
    alert_s_s24_battery_state: _sensor_state
    alert_s_s24_charger_type: _sensor_state
    alert_s_s24_ble_transmitter: _sensor_state
    alert_s_s24_do_not_disturb_sensor: _sensor_state
    alert_s_s24_wifi_connection: _sensor_state
    alert_s_s24_wifi_bssid: _sensor_state
    alert_s_s24_wifi_ip_address: _sensor_state
    alert_s_s24_public_ip_address: _sensor_state
    ping_one_round_trip_time_average: _sensor_state
    ping_eight_round_trip_time_average: _sensor_state
    boiler_bottom_tank_water_temperature: _sensor_state
    boiler_expected_number_of_shower: _sensor_state
    boiler_number_of_shower_remaining: _sensor_state
    boiler_modbuslink_1_2_electric_energy_consumption: _sensor_state
    air_quality: _sensor_state
    alarm_control_panels: _sensor_state
    areas: _sensor_state
    automations: _sensor_state
    binary_sensors: _sensor_state
    buttons: _sensor_state
    calendars: _sensor_state
    cameras: _sensor_state
    climate: _sensor_state
    covers: _sensor_state
    dates: _sensor_state
    datetimes: _sensor_state
    devices: _sensor_state
    device_trackers: _sensor_state
    entities: _sensor_state
    fans: _sensor_state
    humidifiers: _sensor_state
    integrations: _sensor_state
    custom_integrations: _sensor_state
    input_booleans: _sensor_state
    input_buttons: _sensor_state
    input_datetimes: _sensor_state
    input_numbers: _sensor_state
    input_selects: _sensor_state
    input_texts: _sensor_state
    images: _sensor_state
    lights: _sensor_state
    locks: _sensor_state
    media_players: _sensor_state
    numbers: _sensor_state
    persistent_notifications: _sensor_state
    persons: _sensor_state
    remotes: _sensor_state
    scenes: _sensor_state
    scripts: _sensor_state
    selects: _sensor_state
    sensors: _sensor_state
    sirens: _sensor_state
    suns: _sensor_state
    stt: _sensor_state
    switches: _sensor_state
    texts: _sensor_state
    times: _sensor_state
    tts: _sensor_state
    vacuums: _sensor_state
    update: _sensor_state
    water_heaters: _sensor_state
    weather: _sensor_state
    zones: _sensor_state
    issues: _sensor_state
    active_issues: _sensor_state
    ignored_issues: _sensor_state
    shower_floor_temperature: _sensor_state
    shower_floor_temperature_floor: _sensor_state
    shower_floor_wifi_rssi: _sensor_state
    shower_floor_ip: _sensor_state
    batteries_group: _sensor_state
    u6_lite_cpu_utilization: _sensor_state
    u6_pro_cpu_utilization: _sensor_state
    u6_lite_memory_utilization: _sensor_state
    u6_pro_memory_utilization: _sensor_state
    water_leak_zb_1_kitchen_below_battery_type: _sensor_state
    water_leak_zb_1_kitchen_below_battery_last_replaced: _sensor_state
    water_leak_zb_1_kitchen_below_battery_plus: _sensor_state
    water_leak_zb_2_kitchen_sink_closest_battery_type: _sensor_state
    water_leak_zb_2_kitchen_sink_closest_battery_last_replaced: _sensor_state
    water_leak_zb_2_kitchen_sink_closest_battery_plus: _sensor_state
    water_leak_zb_4_laundry_washing_machine_battery_type: _sensor_state
    water_leak_zb_4_laundry_washing_machine_battery_last_replaced: _sensor_state
    water_leak_zb_4_laundry_washing_machine_battery_plus: _sensor_state
    water_leak_zb_3_laundry_water_filter_battery_type: _sensor_state
    water_leak_zb_3_laundry_water_filter_battery_last_replaced: _sensor_state
    water_leak_zb_3_laundry_water_filter_battery_plus: _sensor_state
    room_window_reed_battery_type: _sensor_state
    room_window_reed_battery_last_replaced: _sensor_state
    room_window_reed_battery_plus: _sensor_state
    washer_energy: _sensor_state
    washer_power: _sensor_state
    washer_deltaenergy: _sensor_state
    washer_powerenergy: _sensor_state
    washer_energysaved: _sensor_state
    washer_washer_machine_state: _sensor_state
    washer_washer_job_state: _sensor_state
    washer_washer_completion_time: _sensor_state
    washer_energy_meter: _sensor_state
    washer_power_meter: _sensor_state
    reed_wardrobe_battery_type: _sensor_state
    reed_wardrobe_battery_last_replaced: _sensor_state
    reed_wardrobe_battery_plus: _sensor_state
    valve_kitchen_battery: _sensor_state
    valve_kitchen_position: _sensor_state
    valve_kitchen_boost_heating_countdown: _sensor_state
    zigbee2mqtt_bridge_version_2: _sensor_state
    office_temphum_zb_battery: _sensor_state
    office_temphum_zb_temperature: _sensor_state
    office_temphum_zb_humidity: _sensor_state
    socket_cat_mat_power: _sensor_state
    socket_cat_mat_energy: _sensor_state
    reed_wardrobe_battery: _sensor_state
    reed_wardrobe_device_temperature: _sensor_state
    water_leak_zb_4_battery: _sensor_state
    water_leak_zb_4_device_temperature: _sensor_state
    water_leak_zb_3_battery: _sensor_state
    water_leak_zb_3_device_temperature: _sensor_state
    water_leak_zb_1_battery: _sensor_state
    water_leak_zb_1_device_temperature: _sensor_state
    boiler_warm_water_remaining: _sensor_state
    boiler_electric_power_consumption: _sensor_state
    iphone_kateryna_activity: _sensor_state
    iphone_kateryna_ssid: _sensor_state
    iphone_kateryna_bssid: _sensor_state
    iphone_kateryna_connection_type: _sensor_state
    iphone_kateryna_geocoded_location: _sensor_state
    iphone_kateryna_last_update_trigger: _sensor_state
    room_window_reed_battery: _sensor_state
    projector_socket_power: _sensor_state
    projector_socket_voltage: _sensor_state
    projector_socket_energy: _sensor_state
    iphone_kateryna_battery_type: _sensor_state
    iphone_kateryna_battery_last_replaced: _sensor_state
    qp_bedroom_mqtt_582d34838c0c_battery: _sensor_state
    qp_bedroom_mqtt_582d34838c0c_co2_ppm: _sensor_state
    qp_bedroom_mqtt_582d34838c0c_humidity: _sensor_state
    qp_bedroom_mqtt_582d34838c0c_temperature: _sensor_state
    qp_office_mqtt_582d34826eac_battery: _sensor_state
    qp_office_mqtt_582d34826eac_co2_ppm: _sensor_state
    qp_office_mqtt_582d34826eac_humidity: _sensor_state
    qp_office_mqtt_582d34826eac_temperature: _sensor_state
    reed_wardrobe_last_seen: _sensor_state
    qp_office_bt_battery: _sensor_state
    qp_office_bt_carbon_dioxide: _sensor_state
    qp_office_bt_humidity: _sensor_state
    qp_office_bt_temperature: _sensor_state
    qp_office_bt_signal_strength: _sensor_state
    qp_bedroom_bt_8c0c_battery: _sensor_state
    qp_bedroom_bt_8c0c_carbon_dioxide: _sensor_state
    qp_bedroom_bt_8c0c_humidity: _sensor_state
    qp_bedroom_bt_8c0c_temperature: _sensor_state
    qp_bedroom_bt_8c0c_signal_strength: _sensor_state
    temperature_humidity_sensor_ce25_temperature: _sensor_state
    temperature_humidity_sensor_ce25_humidity: _sensor_state
    shower_temphum_battery: _sensor_state
    shower_temphum_voltage: _sensor_state
    bathroom_temphum_battery_type: _sensor_state
    bathroom_temphum_battery_last_replaced: _sensor_state
    bathroom_temphum_battery_plus: _sensor_state
    shower_temphum_battery_type: _sensor_state
    shower_temphum_battery_last_replaced: _sensor_state
    shower_temphum_battery_plus: _sensor_state
    temperature_humidity_sensor_ce25_battery_type: _sensor_state
    temperature_humidity_sensor_ce25_battery_last_replaced: _sensor_state
    laundry_mi_battery: _sensor_state
    laundry_mi_voltage: _sensor_state
    laundry_mi_humidity: _sensor_state
    laundry_mi_temperature: _sensor_state
    temperature_humidity_sensor_ce25_battery: _sensor_state
    temperature_humidity_sensor_ce25_voltage: _sensor_state
    temperature_humidity_sensor_ce25_battery_plus: _sensor_state
    usw_flex_mini_uptime: _sensor_state
    usw_flex_mini_state: _sensor_state
    laundry_mi_battery_type: _sensor_state
    laundry_mi_battery_last_replaced: _sensor_state
    laundry_mi_battery_plus: _sensor_state
    mi_kitchen_battery: _sensor_state
    mi_kitchen_battery_last_replaced: _sensor_state
    mi_kitchen_battery_type: _sensor_state
    mi_kitchen_battery_plus: _sensor_state
    mi_kitchen_humidity: _sensor_state
    mi_kitchen_temperature: _sensor_state
    mi_kitchen_voltage: _sensor_state
    usw_lite_16_poe_uptime: _sensor_state
    usw_lite_16_poe_state: _sensor_state
    usw_lite_16_poe_cpu_utilization: _sensor_state
    usw_lite_16_poe_memory_utilization: _sensor_state
    mi_1621319031_891001253881_scene_history: _sensor_state
    usw_flex_mini_office_cpu_utilization: _sensor_state
    usw_flex_mini_office_memory_utilization: _sensor_state
    iphone_kateryna_location_permission: _sensor_state
    iphone_kateryna_app_version: _sensor_state
    iphone_kateryna_watch_battery: _sensor_state
    iphone_kateryna_battery_plus: _sensor_state
    delta_pro_main_battery_level: _sensor_state
    delta_pro_state_of_health: _sensor_state
    delta_pro_battery_level: _sensor_state
    delta_pro_total_in_power: _sensor_state
    delta_pro_total_out_power: _sensor_state
    delta_pro_ac_in_power: _sensor_state
    delta_pro_ac_out_power: _sensor_state
    delta_pro_ac_in_volts: _sensor_state
    delta_pro_ac_out_volts: _sensor_state
    delta_pro_dc_out_power: _sensor_state
    delta_pro_dc_out_voltage: _sensor_state
    delta_pro_dc_car_out_power: _sensor_state
    delta_pro_dc_anderson_out_power: _sensor_state
    delta_pro_type_c_1_out_power: _sensor_state
    delta_pro_type_c_2_out_power: _sensor_state
    delta_pro_usb_1_out_power: _sensor_state
    delta_pro_usb_2_out_power: _sensor_state
    delta_pro_usb_qc_1_out_power: _sensor_state
    delta_pro_usb_qc_2_out_power: _sensor_state
    delta_pro_charge_remaining_time: _sensor_state
    delta_pro_discharge_remaining_time: _sensor_state
    delta_pro_cycles: _sensor_state
    delta_pro_battery_temperature: _sensor_state
    delta_pro_slave_1_battery_level: _sensor_state
    delta_pro_slave_1_state_of_health: _sensor_state
    delta_pro_slave_1_battery_temperature: _sensor_state
    delta_pro_slave_1_in_power: _sensor_state
    delta_pro_slave_1_out_power: _sensor_state
    delta_pro_slave_1_cycles: _sensor_state
    delta_pro_status: _sensor_state
    room_window_reed_last_seen: _sensor_state
    door_wifi_signal_db: _sensor_state
    door_wifi_signal_percent: _sensor_state
    door_lock_voltage: _sensor_state
    delta_pro_api_ac_in_power: _sensor_state
    delta_pro_api_ac_in_volts: _sensor_state
    delta_pro_api_ac_out_power: _sensor_state
    delta_pro_api_ac_out_volts: _sensor_state
    delta_pro_api_battery_charge_energy_from_ac: _sensor_state
    delta_pro_api_battery_charge_energy_from_dc: _sensor_state
    delta_pro_api_battery_discharge_energy_to_ac: _sensor_state
    delta_pro_api_battery_discharge_energy_to_dc: _sensor_state
    delta_pro_api_battery_level: _sensor_state
    delta_pro_api_battery_temperature: _sensor_state
    delta_pro_api_charge_remaining_time: _sensor_state
    delta_pro_api_cycles: _sensor_state
    delta_pro_api_dc_anderson_out_power: _sensor_state
    delta_pro_api_dc_car_out_power: _sensor_state
    delta_pro_api_dc_out_power: _sensor_state
    delta_pro_api_dc_out_voltage: _sensor_state
    delta_pro_api_discharge_remaining_time: _sensor_state
    delta_pro_api_main_battery_level: _sensor_state
    delta_pro_api_slave_1_state_of_health: _sensor_state
    delta_pro_api_state_of_health: _sensor_state
    delta_pro_api_status: _sensor_state
    delta_pro_api_total_in_power: _sensor_state
    delta_pro_api_total_out_power: _sensor_state
    delta_pro_api_type_c_1_out_power: _sensor_state
    delta_pro_api_type_c_2_out_power: _sensor_state
    delta_pro_api_usb_1_out_power: _sensor_state
    delta_pro_api_usb_2_out_power: _sensor_state
    delta_pro_api_usb_qc_1_out_power: _sensor_state
    delta_pro_api_usb_qc_2_out_power: _sensor_state
    delta_pro_api_battery_volts: _sensor_state
    delta_pro_api_main_remain_capacity: _sensor_state
    delta_pro_api_slave_1_battery_level: _sensor_state
    delta_pro_api_slave_1_battery_temperature: _sensor_state
    delta_pro_api_slave_1_battery_volts: _sensor_state
    delta_pro_api_slave_1_cycles: _sensor_state
    delta_pro_api_slave_1_in_power: _sensor_state
    delta_pro_api_slave_1_out_power: _sensor_state
    delta_pro_api_slave_1_remain_capacity: _sensor_state
    electricity_price: _sensor_state
    delta_pro_api_battery_discharge_energy_to_ac_cost: _sensor_state
    delta_pro_api_battery_discharge_energy_to_dc_cost: _sensor_state
    u6_pro_uplink_mac: _sensor_state
    bt_proxy_c6_man8_wifi_signal_db: _sensor_state
    bt_proxy_c6_man8_wifi_signal_percent: _sensor_state
    kateryna_drozd_watch_battery_state: _sensor_state
    xiaomi_wireless_button_1_battery_plus: _sensor_state
    fridge_temperature_latest: _sensor_state
    fridge_humidity_latest: _sensor_state
    temperature_humidity_sensor_7360_battery: _sensor_state
    temperature_humidity_sensor_7360_voltage: _sensor_state
    temperature_humidity_sensor_7360_battery_type: _sensor_state
    temperature_humidity_sensor_7360_battery_last_replaced: _sensor_state
    temperature_humidity_sensor_7360_battery_plus: _sensor_state
    ha_uptime: _sensor_state
    ha_uptime_seconds: _sensor_state
    quest3_volume_level_music: _sensor_state
    quest3_volume_level_system: _sensor_state
    quest3_battery_level: _sensor_state
    quest3_battery_state: _sensor_state
    quest3_charger_type: _sensor_state
    quest3_battery_health: _sensor_state
    quest3_battery_temperature: _sensor_state
    quest3_battery_power: _sensor_state
    quest3_remaining_charge_time: _sensor_state
    quest3_last_reboot: _sensor_state
    quest3_wifi_connection: _sensor_state
    quest3_wifi_bssid: _sensor_state
    quest3_wifi_ip_address: _sensor_state
    quest3_wifi_link_speed: _sensor_state
    quest3_wifi_frequency: _sensor_state
    quest3_wifi_signal_strength: _sensor_state
    quest3_public_ip_address: _sensor_state
    quest3_network_type: _sensor_state
    quest3_internal_storage: _sensor_state
    quest3_battery_type: _sensor_state
    quest3_battery_last_replaced: _sensor_state
    quest3_battery_plus: _sensor_state
    cleargrass_dk1_3904_temperature: _sensor_state
    cleargrass_dk1_3c69_temperature: _sensor_state
    miaomiaoce_t2_b99d_temperature: _sensor_state
    miaomiaoce_t2_ce25_temperature: _sensor_state
    miaomiaoce_t2_7360_temperature: _sensor_state
    miaomiaoce_t2_b5ef_temperature: _sensor_state
    slzb_06p10_connection_mode: _sensor_state
    slzb_06p10_firmware_channel: _sensor_state
    slzb_06p10_zigbee_type: _sensor_state
    slzb_06p10_core_chip_temp: _sensor_state
    slzb_06p10_zigbee_chip_temp: _sensor_state
    slzb_06p10_ram_usage: _sensor_state
    slzb_06p10_filesystem_usage: _sensor_state
    slzb_06p10_core_uptime: _sensor_state
    slzb_06p10_zigbee_uptime: _sensor_state
    miaomiaoc_cn_blt_3_1e11g52molc00_t2_temperature_p_2_1: _sensor_state
    miaomiaoc_cn_blt_3_1e11g52molc00_t2_relative_humidity_p_2_2: _sensor_state
    miaomiaoc_cn_blt_3_1e11g52molc00_t2_battery_level_p_3_1: _sensor_state
    miaomiaoc_cn_blt_3_1g0ou6ds0kc00_t2_temperature_p_2_1: _sensor_state
    miaomiaoc_cn_blt_3_1g0ou6ds0kc00_t2_relative_humidity_p_2_2: _sensor_state
    miaomiaoc_cn_blt_3_1g0ou6ds0kc00_t2_battery_level_p_3_1: _sensor_state
    cleargras_cn_blt_3_11p1kol8ge400_dk1_temperature_p_2_1: _sensor_state
    cleargras_cn_blt_3_11p1kol8ge400_dk1_relative_humidity_p_2_2: _sensor_state
    cleargras_cn_blt_3_11p1kol8ge400_dk1_battery_level_p_3_1: _sensor_state
    cleargras_cn_blt_3_11p1kj7ikec00_dk1_temperature_p_2_1: _sensor_state
    cleargras_cn_blt_3_11p1kj7ikec00_dk1_relative_humidity_p_2_2: _sensor_state
    cleargras_cn_blt_3_11p1kj7ikec00_dk1_battery_level_p_3_1: _sensor_state
    lumi_cn_blt_3_15uta0cjolo00_bmcn01_submersion_state_p_2_1: _sensor_state
    lumi_cn_blt_3_15uta0cjolo00_bmcn01_battery_level_p_3_1: _sensor_state
    lumi_cn_blt_3_15utbdl8clk00_bmcn01_submersion_state_p_2_1: _sensor_state
    lumi_cn_blt_3_15utbdl8clk00_bmcn01_battery_level_p_3_1: _sensor_state
    lumi_cn_blt_3_15utcieasec00_bmcn01_submersion_state_p_2_1: _sensor_state
    lumi_cn_blt_3_15utcieasec00_bmcn01_battery_level_p_3_1: _sensor_state
    lumi_cn_blt_3_15utcv1agec00_bmcn01_submersion_state_p_2_1: _sensor_state
    lumi_cn_blt_3_15utcv1agec00_bmcn01_battery_level_p_3_1: _sensor_state
    miaomiaoc_cn_blt_3_1fq9n0qa8kk00_t2_temperature_p_2_1: _sensor_state
    miaomiaoc_cn_blt_3_1fq9n0qa8kk00_t2_relative_humidity_p_2_2: _sensor_state
    miaomiaoc_cn_blt_3_1fq9n0qa8kk00_t2_battery_level_p_3_1: _sensor_state
    miaomiaoc_cn_blt_4_1i13sjg71gc00_t2_temperature_p_2_1: _sensor_state
    miaomiaoc_cn_blt_4_1i13sjg71gc00_t2_relative_humidity_p_2_2: _sensor_state
    miaomiaoc_cn_blt_4_1i13sjg71gc00_t2_battery_level_p_3_1: _sensor_state
    ijai_de_1027836802_v3_fault_p_2_2: _sensor_state
    ijai_de_1027836802_v3_door_state_p_7_3: _sensor_state
    ijai_de_1027836802_v3_cloth_state_p_7_4: _sensor_state
    ijai_de_1027836802_v3_side_brush_life_p_7_8: _sensor_state
    ijai_de_1027836802_v3_side_brush_hours_p_7_9: _sensor_state
    ijai_de_1027836802_v3_main_brush_life_p_7_10: _sensor_state
    ijai_de_1027836802_v3_main_brush_hours_p_7_11: _sensor_state
    ijai_de_1027836802_v3_hypa_life_p_7_12: _sensor_state
    ijai_de_1027836802_v3_hypa_hours_p_7_13: _sensor_state
    ijai_de_1027836802_v3_mop_life_p_7_14: _sensor_state
    ijai_de_1027836802_v3_mop_hours_p_7_15: _sensor_state
    ijai_de_1027836802_v3_cleaning_time_p_7_22: _sensor_state
    ijai_de_1027836802_v3_cleaning_area_p_7_23: _sensor_state
    ijai_de_1027836802_v3_multi_prop_vacuum_p_7_45: _sensor_state
    ijai_de_1027836802_v3_map_encrypt_p_7_55: _sensor_state
    ijai_de_1027836802_v3_all_enable_count_p_8_18: _sensor_state
    ijai_de_1027836802_v3_cur_map_id_p_10_2: _sensor_state
    ijai_de_1027836802_v3_map_num_p_10_3: _sensor_state
    ijai_de_1027836802_v3_cur_cleaning_path_p_10_5: _sensor_state
    ijai_de_1027836802_v3_build_map_p_10_14: _sensor_state
    ijai_de_1027836802_v3_has_new_map_p_10_19: _sensor_state
    ijai_de_1027836802_v3_dnd_enable_p_12_1: _sensor_state
    ijai_de_1027836802_v3_dnd_start_hour_p_12_2: _sensor_state
    ijai_de_1027836802_v3_dnd_start_minute_p_12_3: _sensor_state
    ijai_de_1027836802_v3_dnd_end_hour_p_12_4: _sensor_state
    ijai_de_1027836802_v3_dnd_end_minute_p_12_5: _sensor_state
    ijai_de_1027836802_v3_multi_prop_dnd_p_12_7: _sensor_state
    kateryna_drozd_audio_output: _sensor_state
    valve_office_position: _sensor_state
    valve_room_position: _sensor_state
    valve_bedroom_position: _sensor_state
    xiaomi_wireless_button_2_battery: _sensor_state
    xiaomi_wireless_button_2_device_temperature: _sensor_state
    lumi_v3_0661_illumination: _sensor_state
    flood_detector_a1e5_battery_type: _sensor_state
    flood_detector_a1e5_battery_last_replaced: _sensor_state
    flood_detector_a1e5_battery_plus: _sensor_state
    flood_detector_a948_battery_type: _sensor_state
    flood_detector_a948_battery_last_replaced: _sensor_state
    flood_detector_a948_battery_plus: _sensor_state
    flood_detector_ad9d_battery_type: _sensor_state
    flood_detector_ad9d_battery_last_replaced: _sensor_state
    flood_detector_ad9d_battery_plus: _sensor_state
    flood_detector_b134_battery_type: _sensor_state
    flood_detector_b134_battery_last_replaced: _sensor_state
    flood_detector_b134_battery_plus: _sensor_state
    motion_cat_toilet_motion_state: _sensor_state
    motion_cat_toilet_battery: _sensor_state
    motion_cat_toilet_battery_type: _sensor_state
    motion_cat_toilet_battery_last_replaced: _sensor_state
    motion_cat_toilet_battery_plus: _sensor_state
    motion_cat_toilet_illuminance: _sensor_state
    orbitrack_tl_current_2: _sensor_state
    orbitrack_tl_energy: _sensor_state
    orbitrack_tl_power_2: _sensor_state
    orbitrack_tl_voltage_2: _sensor_state
    mi_1621319031_891001017564_scene_history: _sensor_state
    qp_bedroom_bt_8c0c_battery_type: _sensor_state
    qp_bedroom_bt_8c0c_battery_last_replaced: _sensor_state
    qp_bedroom_bt_8c0c_battery_plus: _sensor_state
    qp_office_bt_battery_type: _sensor_state
    qp_office_bt_battery_last_replaced: _sensor_state
    qp_office_bt_battery_plus: _sensor_state
    motion_office_cat_battery_type: _sensor_state
    motion_office_cat_battery_last_replaced: _sensor_state
    motion_office_cat_battery_plus: _sensor_state
    reed_office_cabinet_battery: _sensor_state
    reed_office_cabinet_battery_type_2: _sensor_state
    reed_office_cabinet_battery_last_replaced_2: _sensor_state
    reed_office_cabinet_battery_plus_2: _sensor_state
    alert_s_redmi_pad_pro_ringer_mode: _sensor_state
    alert_s_redmi_pad_pro_audio_mode: _sensor_state
    alert_s_redmi_pad_pro_battery_level: _sensor_state
    alert_s_redmi_pad_pro_battery_state: _sensor_state
    alert_s_redmi_pad_pro_charger_type: _sensor_state
    alert_s_redmi_pad_pro_ble_transmitter: _sensor_state
    alert_s_redmi_pad_pro_do_not_disturb_sensor: _sensor_state
    alert_s_redmi_pad_pro_wi_fi_connection: _sensor_state
    alert_s_redmi_pad_pro_wi_fi_bssid: _sensor_state
    alert_s_redmi_pad_pro_wi_fi_ip_address: _sensor_state
    alert_s_redmi_pad_pro_public_ip_address: _sensor_state
    alert_s_redmi_pad_pro_network_type: _sensor_state
    onedrive_used_storage: _sensor_state
    onedrive_remaining_storage: _sensor_state
    onedrive_drive_state: _sensor_state
    music_assistant_server_cpu_percent: _sensor_state
    ijai_v3_4619_door_state: _sensor_state
    grocy_chores: _sensor_state
    grocy_tasks: _sensor_state
    backup_backup_manager_state: _sensor_state
    backup_next_scheduled_automatic_backup: _sensor_state
    backup_last_successful_automatic_backup: _sensor_state
    telegram_client_alertua_id: _sensor_state
    telegram_client_alertua_username: _sensor_state
    telegram_client_alertua_last_name: _sensor_state
    telegram_client_alertua_first_name: _sensor_state
    telegram_client_alertua_phone: _sensor_state
    telegram_client_alertua_last_sent_message_id: _sensor_state
    telegram_client_alertua_last_edited_message_id: _sensor_state
    telegram_client_alertua_last_deleted_message_id: _sensor_state
    sonoff_aca80001d6: _sensor_state
    reed_hallway_closet_right_battery: _sensor_state
    reed_hallway_closet_right_voltage: _sensor_state
    reed_hallway_closet_right_battery_type: _sensor_state
    reed_hallway_closet_right_battery_last_replaced: _sensor_state
    reed_hallway_closet_right_battery_plus: _sensor_state
    energy_monitoring_smartplug_current: _sensor_state
    energy_monitoring_smartplug_power: _sensor_state
    energy_monitoring_smartplug_voltage: _sensor_state
    energy_monitoring_smartplug_temperature: _sensor_state
    gaggiuino_profile_id: _sensor_state
    gaggiuino_profile_name: _sensor_state
    gaggiuino_target_temperature: _sensor_state
    gaggiuino_temperature: _sensor_state
    gaggiuino_water_level: _sensor_state
    s2a87ff082a76aa9dc_6afc_estimated_distance: _sensor_state
    relay_laundry_power: _sensor_state
    relay_laundry_energy: _sensor_state
    relay_laundry_device_temperature: _sensor_state
    relay_laundry_voltage: _sensor_state
    relay_laundry_current: _sensor_state
    relay_laundry_last_seen: _sensor_state
    wine_fridge_temphum_voltage: _sensor_state
    wine_fridge_temphum_battery: _sensor_state
    wine_fridge_temphum_temperature: _sensor_state
    wine_fridge_temphum_humidity: _sensor_state
    wine_fridge_temphum_count: _sensor_state
    wine_fridge_temphum_battery_type: _sensor_state
    wine_fridge_temphum_battery_last_replaced: _sensor_state
    wine_fridge_temphum_battery_plus: _sensor_state
    a1_slwf_03_voice_assistant_slwf_03_uptime: _sensor_state
    backup_last_attempted_automatic_backup: _sensor_state
    openweathermap_weather: _sensor_state
    openweathermap_dew_point: _sensor_state
    openweathermap_temperature: _sensor_state
    openweathermap_feels_like_temperature: _sensor_state
    openweathermap_wind_speed: _sensor_state
    openweathermap_wind_bearing: _sensor_state
    openweathermap_humidity: _sensor_state
    openweathermap_pressure: _sensor_state
    openweathermap_cloud_coverage: _sensor_state
    openweathermap_rain: _sensor_state
    openweathermap_snow: _sensor_state
    openweathermap_precipitation_kind: _sensor_state
    openweathermap_uv_index: _sensor_state
    openweathermap_visibility: _sensor_state
    openweathermap_condition: _sensor_state
    openweathermap_weather_code: _sensor_state
    alert_test: _sensor_state
    temphum_noscreen_1_temperature: _sensor_state
    temphum_noscreen_1_humidity: _sensor_state
    temphum_noscreen_1_battery: _sensor_state
    alert_s_s24_battery_type: _sensor_state
    alert_s_s24_battery_last_replaced: _sensor_state
    alert_s_s24_battery_plus: _sensor_state
    office_vitamins_temphum_battery_type: _sensor_state
    office_vitamins_temphum_battery_last_replaced: _sensor_state
    office_vitamins_temphum_battery_plus: _sensor_state
    co2_temp_rh_2cf6_temperature: _sensor_state
    co2_temp_rh_2cf6_humidity: _sensor_state
    co2_temp_rh_2cf6_battery: _sensor_state
    co2_temp_rh_2cf6_carbon_dioxide: _sensor_state
    co2_temp_rh_2cf6_battery_type: _sensor_state
    co2_temp_rh_2cf6_battery_last_replaced: _sensor_state
    co2_temp_rh_2cf6_battery_plus: _sensor_state
    s57c97f77153dcf28c_9cf3_estimated_distance: _sensor_state
    openweathermap_wind_gust: _sensor_state
    s2ef73d665717bbfdc_e7c6_estimated_distance: _sensor_state
    mi_9_se_battery_level: _sensor_state
    mi_9_se_battery_state: _sensor_state
    mi_9_se_charger_type: _sensor_state
    mi_9_se_geocoded_location: _sensor_state
    mijia_de_56078868_v1_stream_status_p_3_1: _sensor_state
    u6_lite_uplink_mac: _sensor_state
    u7_pro_uptime: _sensor_state
    u7_pro_state: _sensor_state
    u7_pro_cpu_utilization: _sensor_state
    u7_pro_memory_utilization: _sensor_state
    u7_pro_uplink_mac: _sensor_state
    xiaomi_wireless_button_1_battery: _sensor_state
    xiaomi_wireless_button_1_device_temperature: _sensor_state
    bedroom_window_reed_battery: _sensor_state
    bedroom_window_reed_voltage: _sensor_state
    bedroom_entrance_uptime: _sensor_state
    light_shower_led_uptime: _sensor_state
    motion_office_sun_motion_state: _sensor_state
    motion_office_sun_illuminance: _sensor_state
    motion_office_sun_battery: _sensor_state
    bedroom_window_reed_battery_type_2: _sensor_state
    bedroom_window_reed_battery_last_replaced_2: _sensor_state
    bedroom_window_reed_battery_plus_2: _sensor_state
    weathersense_feels_like_outside: _sensor_state
    weathersense_office_feels_like_feels_like_temperature_inside: _sensor_state
    sleepasandroid_alert: _sensor_state
    sleep_as_android_next_alarm: _sensor_state
    sleep_as_android_alarm_label: _sensor_state
    ghcr_io_round_trip_time_average: _sensor_state
    water_leak_laundry_washing_machine_battery: _sensor_state
    water_leak_laundry_washing_machine_voltage: _sensor_state
    water_leak_laundry_washing_machine_battery_type: _sensor_state
    water_leak_laundry_washing_machine_battery_last_replaced: _sensor_state
    water_leak_laundry_washing_machine_battery_plus: _sensor_state
    xiaomi_gateway_2_illumination: _sensor_state
    water_leak_zb_2_battery: _sensor_state
    water_leak_zb_2_device_temperature: _sensor_state
    ijai_de_1027836802_v3_battery_level_p_3_1: _sensor_state
    xiaomi_gateway_illumination: _sensor_state
    lun_misto_air_home_pm2_5: _sensor_state
    lun_misto_air_home_pm10: _sensor_state
    lun_misto_air_home_pm1: _sensor_state
    lun_misto_air_home_temperature: _sensor_state
    lun_misto_air_home_humidity: _sensor_state
    lun_misto_air_home_pressure: _sensor_state
    lun_misto_air_quality_index: _sensor_state
    fridge_temperature_ble: _sensor_state
    fridge_humidity_ble: _sensor_state
    room_accent_light_power: _sensor_state
    room_accent_light_current: _sensor_state
    room_accent_light_voltage: _sensor_state
    room_accent_light_energy: _sensor_state
    sd3523776c5f01c53c_73ef_estimated_distance: _sensor_state
    socket_random_cloud_power_2: _sensor_state
    socket_random_cloud_consumption: _sensor_state
    socket_random_cloud_daily_consumption: _sensor_state
    socket_random_cloud_monthly_consumption: _sensor_state
    socket_random_cloud_yearly_consumption: _sensor_state
    delta_2_plug_power_3: _sensor_state
    delta_2_plug_consumption: _sensor_state
    delta_2_plug_daily_consumption: _sensor_state
    delta_2_plug_monthly_consumption: _sensor_state
    delta_2_plug_yearly_consumption: _sensor_state
    laundry_optional_power_3: _sensor_state
    laundry_optional_consumption: _sensor_state
    laundry_optional_daily_consumption: _sensor_state
    laundry_optional_monthly_consumption: _sensor_state
    laundry_optional_yearly_consumption: _sensor_state
    atorch_breaker_power: _sensor_state
    smart_energy_meter_at2pl_gr2p_voltage_3: _sensor_state
    smart_energy_meter_at2pl_gr2p_consumption: _sensor_state
    smart_energy_meter_at2pl_gr2p_daily_consumption: _sensor_state
    smart_energy_meter_at2pl_gr2p_monthly_consumption: _sensor_state
    smart_energy_meter_at2pl_gr2p_yearly_consumption: _sensor_state
    orbitrack_power_2: _sensor_state
    orbitrack_consumption: _sensor_state
    orbitrack_daily_consumption: _sensor_state
    orbitrack_monthly_consumption: _sensor_state
    orbitrack_yearly_consumption: _sensor_state
    office_window_cloud_cover_controls_inverted_2: _sensor_state
    office_window_cloud_cover_status_inverted: _sensor_state
    room_window_cloud_cover_controls_inverted_2: _sensor_state
    room_window_cloud_cover_status_inverted: _sensor_state
    bedroom_window_cloud_cover_controls_inverted_2: _sensor_state
    bedroom_window_cloud_cover_status_inverted: _sensor_state
    kitchen_window_cloud_cover_controls_inverted_2: _sensor_state
    kitchen_window_cloud_cover_status_inverted: _sensor_state
    kiiv_dtek_3_1_electricity: _sensor_state
    kiiv_dtek_3_1_schedule_updated_on: _sensor_state
    kiiv_dtek_3_1_schedule_data_changed_on: _sensor_state
    kiiv_dtek_3_1_next_planned_outage: _sensor_state
    kiiv_dtek_3_1_next_connectivity: _sensor_state
    alert_server_array_state: _sensor_state
    alert_server_array_usage: _sensor_state
    alert_server_ram_usage: _sensor_state
    alert_server_cpu_utilization: _sensor_state
    alert_server_cpu_temperature: _sensor_state
    alert_server_cpu_power: _sensor_state
    mini_array_state: _sensor_state
    mini_array_usage: _sensor_state
    mini_ram_usage: _sensor_state
    mini_cpu_utilization: _sensor_state
    mini_cpu_temperature: _sensor_state
    mini_cpu_power: _sensor_state
    office_motion_cat_mat_motion_state: _sensor_state
    office_motion_cat_mat_illuminance: _sensor_state
    office_motion_cat_mat_battery: _sensor_state
    office_motion_cat_mat_battery_type: _sensor_state
    office_motion_cat_mat_battery_last_replaced: _sensor_state
    office_motion_cat_mat_battery_plus: _sensor_state
    delta_pro_estimated_discharge_time: _sensor_state
    delta_pro_battery_percent_after_outage: _sensor_state
    usw_flex_mini_office_uplink_mac: _sensor_state
    season: _sensor_state

class shell_command:

    @staticmethod
    def nut_restart() -> dict[str, Any]:
        ...

    @staticmethod
    def bt_connect() -> dict[str, Any]:
        ...

class siren:

    @staticmethod
    def turn_on(*, entity_id: str, tone: str | None=None, volume_level: int | None=None, duration: str | None=None):
        """

        Args:
            entity_id: Entity ID
            tone:  Example: fire
            volume_level:  Example: 0.5
            duration:  Example: 15"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class sonoff:

    @staticmethod
    def send_command(*, device=None, cmd=None):
        """Sends a command to a device.

        Args:
            device: Device ID to send command to. Example: 1000123456
            cmd: A single command to send. Example: switch"""
        ...

class spook:

    @staticmethod
    def boo():
        """Calling this action spooks Home Assistant. Performing this action will always fail."""
        ...

    @staticmethod
    def random_fail():
        """Performing this action will randomly fail."""
        ...

class ssh_command:

    @staticmethod
    def exec_command(*, command: str, host: str | None=None, port: int | None=None, user: str | None=None, private_key: str | None=None, passphrase: str | None=None, timeout: int | None=None) -> dict[str, Any]:
        """

        Args:
            command:  Example: ls -la
            host:  Example: 172.17.0.1
            port:  Example: 22
            user:  Example: root
            private_key:  Example: /config/ssh/id_rsa
            passphrase:  Example: secret
            timeout:  Example: 5"""
        ...

class _stt_state(StateVal):
    ...

class stt:
    home_assistant_cloud: _stt_state
    google_ai_stt: _stt_state
    custom_whisper: _stt_state

class _switch_state(StateVal):
    actions: list
    alarm: int
    current_slot: int
    entities: list
    id: str
    inching: str
    integration: str
    next_slot: int
    next_trigger: str
    restored: bool
    supported_features: int
    tags: list
    test_bit: int
    timeslots: list
    weekdays: list

    def turn_off(self):
        ...

    def turn_on(self):
        ...

    def toggle(self):
        ...

class switch:
    schedule_sunrise_close_window: _switch_state
    schedule_room_ac_off_midnight: _switch_state
    schedule_office_ac_off_midnight: _switch_state
    schedule_kitchen_ac_off_midnight: _switch_state
    schedule_kitchen_window_close_3_30pm_temp_27: _switch_state
    schedule_bedroom_ac_off_morning: _switch_state
    dahua_vto_dahua_motion_detection: _switch_state
    dahua_vto_dahua_disarming: _switch_state
    schedule_router_reboot_3am: _switch_state
    schedule_bedroom_light_off_at_1am_of_noone_home: _switch_state
    ijai_v3_4619_alarm: _switch_state
    ijai_v3_4619_repeat_state: _switch_state
    schedule_ha_restart_sun_3am: _switch_state
    schedule_12d109: _switch_state
    schedule_cfc8fc: _switch_state
    schedule_000977: _switch_state
    schedule_242c1c: _switch_state
    schedule_57f7bd: _switch_state
    schedule_4db69b: _switch_state
    alert: _switch_state
    alert_2_4g: _switch_state
    schedule_f5231c: _switch_state
    schedule_turn_off_shower_lights_2_am: _switch_state
    schedule_turn_off_bathroom_lights_2_am: _switch_state
    schedule_37edc0: _switch_state
    schedule_0e456c: _switch_state
    schedule_0fe17a: _switch_state
    schedule_4baf46: _switch_state
    schedule_lights_off_if_noone_home_1am: _switch_state
    projector: _switch_state
    schedule_f0a9f3: _switch_state
    door_door_close: _switch_state
    door_door_open: _switch_state
    schedule_2ea9fb: _switch_state
    water_valves: _switch_state
    washer: _switch_state
    valve_kitchen_eco_mode: _switch_state
    valve_kitchen_window_detection: _switch_state
    valve_kitchen_boost_heating: _switch_state
    zigbee2mqtt_bridge_permit_join_2: _switch_state
    office_temphum_zb_show_smiley: _switch_state
    office_temphum_zb_enable_display: _switch_state
    socket_cat_mat: _switch_state
    projector_socket: _switch_state
    card_tools_pre_release: _switch_state
    local_tuya_pre_release: _switch_state
    layout_card_pre_release: _switch_state
    delta_pro_beeper: _switch_state
    delta_pro_dc_12v_enabled: _switch_state
    delta_pro_ac_enabled: _switch_state
    delta_pro_x_boost_enabled: _switch_state
    delta_pro_ac_always_on: _switch_state
    delta_pro_backup_reserve_enabled: _switch_state
    door_lock: _switch_state
    door_unlock: _switch_state
    delta_pro_api_ac_always_on: _switch_state
    delta_pro_api_backup_reserve_enabled: _switch_state
    delta_pro_api_beeper: _switch_state
    delta_pro_api_bypass_ac_auto_start: _switch_state
    delta_pro_api_dc_12v_enabled: _switch_state
    delta_pro_api_x_boost_enabled: _switch_state
    alert_server_switch: _switch_state
    cloud_alexa: _switch_state
    cloud_alexa_report_state: _switch_state
    cloud_google: _switch_state
    cloud_google_report_state: _switch_state
    cloud_remote: _switch_state
    shower_vents_l1: _switch_state
    shower_vents_l2: _switch_state
    schedule_turn_off_lights_at_1_am_if_someone_is_asleep: _switch_state
    schedule_1a5dec: _switch_state
    ijai_v3_4619_switch_status: _switch_state
    slzb_06p10_disable_leds: _switch_state
    slzb_06p10_led_night_mode: _switch_state
    schedule_1a2393: _switch_state
    valve_office_window_detection: _switch_state
    valve_office_valve_detection: _switch_state
    valve_office_auto_lock: _switch_state
    valve_office_away_mode: _switch_state
    valve_room_window_detection: _switch_state
    valve_room_valve_detection: _switch_state
    valve_room_auto_lock: _switch_state
    valve_room_away_mode: _switch_state
    valve_bedroom_window_detection: _switch_state
    valve_bedroom_valve_detection: _switch_state
    valve_bedroom_auto_lock: _switch_state
    valve_bedroom_away_mode: _switch_state
    valve_cold: _switch_state
    motion_cat_toilet_indicator: _switch_state
    socket_cat_mat_child_lock: _switch_state
    projector_socket_child_lock: _switch_state
    valve_office_child_lock: _switch_state
    valve_room_child_lock: _switch_state
    valve_bedroom_child_lock: _switch_state
    orbitrack_tl_overcharge_cutoff: _switch_state
    orbitrack_tl: _switch_state
    schedule_light_after_dusk_if_anyone_home: _switch_state
    bedroom_entrance: _switch_state
    bedroom_entrance_network_indicator: _switch_state
    bedroom_entrance_turbo_mode: _switch_state
    bedroom_entrance_delayed_power_on_state: _switch_state
    bedroom_entrance_detach_relay_mode: _switch_state
    washer_bubble_soak: _switch_state
    schedule_kitchen_lights_turn_off_sunrise_1h: _switch_state
    schedule_bedroom_light_off_after_sunrise: _switch_state
    energy_monitoring_smartplug_overcharge_protection: _switch_state
    wine_fridge_tl: _switch_state
    schedule_97f403: _switch_state
    schedule_7bb684: _switch_state
    schedule_6a20ee: _switch_state
    schedule_bf8a68: _switch_state
    relay_laundry_l1: _switch_state
    relay_laundry_l2: _switch_state
    relay_laundry_power_outage_memory: _switch_state
    relay_laundry_interlock: _switch_state
    alert_test: _switch_state
    pi_hole: _switch_state
    mijia_de_56078868_v1_on_p_2_1: _switch_state
    mijia_de_56078868_v1_time_watermark_p_2_5: _switch_state
    mijia_de_56078868_v1_wdr_mode_p_2_6: _switch_state
    motion_office_sun_indicator: _switch_state
    music_assistant_jukebox_jukebox_queue: _switch_state
    music_assistant_jukebox_jukebox_allow_access: _switch_state
    music_assistant_jukebox_jukebox_play_music_on_start: _switch_state
    schedule_boiler_auto_7_am: _switch_state
    bathroom_vents: _switch_state
    bathroom_vents_network_indicator: _switch_state
    bathroom_vents_turbo_mode: _switch_state
    bathroom_vents_delayed_power_on_state: _switch_state
    bathroom_vents_detach_relay_mode: _switch_state
    ecoflow_delta_pro: _switch_state
    unifi_block_a0_bd_1d_c2_5a_c3: _switch_state
    door_lock_2: _switch_state
    slzb_06p10: _switch_state
    unifi_block_30_52_53_02_c0_d3: _switch_state
    nest_audio: _switch_state
    nest_audio_2: _switch_state
    esp32s3_fcf280: _switch_state
    unifi_block_84_f3_eb_8d_75_90: _switch_state
    bt_proxy_c6_man8: _switch_state
    nest_audio_3: _switch_state
    unifi_block_08_ed_ed_6c_cb_a7: _switch_state
    ecoflow_delta_2: _switch_state
    washer_2: _switch_state
    unifi_block_04_bf_1b_32_bd_60: _switch_state
    unifi_block_7c_83_34_bf_d0_8a: _switch_state
    wlan0: _switch_state
    er_x: _switch_state
    schedule_bedroom_lights_after_dawn: _switch_state
    schedule_bedroom_led_bot_after_dusk: _switch_state
    door_door_restart: _switch_state
    room_accent_light: _switch_state
    room_accent_light_child_lock: _switch_state
    server_switch: _switch_state
    bathroom_floor_cl_switch: _switch_state
    bathroom_floor_cl_child_lock_2: _switch_state
    office_window_cloud_reverse: _switch_state
    room_window_cloud_reverse: _switch_state
    bedroom_window_cloud_reverse: _switch_state
    kitchen_window_cloud_reverse: _switch_state
    socket_random_cloud_switch_1: _switch_state
    delta_2_plug_switch_1: _switch_state
    delta_2_plug_child_lock_3: _switch_state
    laundry_optional_none: _switch_state
    laundry_optional_child_lock_3: _switch_state
    smart_energy_meter_at2pl_gr2p_switch_1_2: _switch_state
    orbitrack_switch_1: _switch_state
    office_window_cloud_invert_cover_controls_2: _switch_state
    office_window_cloud_invert_cover_status: _switch_state
    room_window_cloud_invert_cover_controls_2: _switch_state
    room_window_cloud_invert_cover_status: _switch_state
    bedroom_window_cloud_invert_cover_controls_2: _switch_state
    bedroom_window_cloud_invert_cover_status: _switch_state
    kitchen_window_cloud_invert_cover_controls_2: _switch_state
    kitchen_window_cloud_invert_cover_status: _switch_state
    office_motion_cat_mat_indicator: _switch_state
    schedule_be025f: _switch_state
    schedule_f2cd07: _switch_state
    schedule_bedroom_wanted_temp_non_summer: _switch_state

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class system_log:

    @staticmethod
    def clear():
        ...

    @staticmethod
    def write(*, message: str, level: Literal['', 'debug', 'info', 'warning', 'error', 'critical']='error', logger: str | None=None):
        """

        Args:
            message:  Example: Something went wrong
            logger:  Example: mycomponent.myplatform"""
        ...

class telegram:

    @staticmethod
    def reload():
        ...

class telegram_bot:

    @staticmethod
    def send_message(*, message: str, config_entry_id: str | None=None, title: str | None=None, target: str | None=None, parse_mode: Literal['', 'html', 'markdown', 'markdownv2', 'plain_text'] | None=None, disable_notification: bool | None=None, disable_web_page_preview: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or ["Text button1:/button1, Text button2:/button2", "Text button3:/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_chat_action(*, config_entry_id: str | None=None, chat_action: Literal['', 'typing', 'upload_photo', 'record_video', 'upload_video', 'record_voice', 'upload_voice', 'upload_document', 'choose_sticker', 'find_location', 'record_video_note', 'upload_video_note'] | None=None, target: str | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            target:  Example: [12345, 67890] or 12345"""
        ...

    @staticmethod
    def send_photo(*, config_entry_id: str | None=None, url: str | None=None, url_options=None, file: str | None=None, caption: str | None=None, target: str | None=None, parse_mode: Literal['', 'html', 'markdown', 'markdownv2', 'plain_text'] | None=None, disable_notification: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            url:  Example: http://example.org/path/to/the/image.png
            file:  Example: /path/to/the/image.png
            caption:  Example: My image
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_sticker(*, config_entry_id: str | None=None, url: str | None=None, url_options=None, file: str | None=None, sticker_id: str | None=None, target: str | None=None, disable_notification: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            url:  Example: http://example.org/path/to/the/sticker.webp
            file:  Example: /path/to/the/sticker.webp
            sticker_id:  Example: CAACAgIAAxkBAAEDDldhZD-hqWclr6krLq-FWSfCrGNmOQAC9gAD9HsZAAFeYY-ltPYnrCEE
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_animation(*, config_entry_id: str | None=None, url: str | None=None, url_options=None, file: str | None=None, caption: str | None=None, target: str | None=None, parse_mode: Literal['', 'html', 'markdown', 'markdownv2', 'plain_text'] | None=None, disable_notification: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            url:  Example: http://example.org/path/to/the/animation.gif
            file:  Example: /path/to/the/animation.gif
            caption:  Example: My animation
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_video(*, config_entry_id: str | None=None, url: str | None=None, url_options=None, file: str | None=None, caption: str | None=None, target: str | None=None, parse_mode: Literal['', 'html', 'markdown', 'markdownv2', 'plain_text'] | None=None, disable_notification: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            url:  Example: http://example.org/path/to/the/video.mp4
            file:  Example: /path/to/the/video.mp4
            caption:  Example: My video
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_voice(*, config_entry_id: str | None=None, url: str | None=None, url_options=None, file: str | None=None, caption: str | None=None, target: str | None=None, disable_notification: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            url:  Example: http://example.org/path/to/the/voice.opus
            file:  Example: /path/to/the/voice.opus
            caption:  Example: My microphone recording
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_document(*, config_entry_id: str | None=None, url: str | None=None, url_options=None, file: str | None=None, caption: str | None=None, target: str | None=None, parse_mode: Literal['', 'html', 'markdown', 'markdownv2', 'plain_text'] | None=None, disable_notification: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            url:  Example: http://example.org/path/to/the/document.odf
            file:  Example: /tmp/whatever.odf
            caption:  Example: Document Title xy
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_location(*, latitude: int, longitude: int, config_entry_id: str | None=None, target: str | None=None, disable_notification: bool | None=None, timeout: int | None=None, keyboard: str | None=None, inline_keyboard: Any | None=None, message_tag: str | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            target:  Example: [12345, 67890] or 12345
            keyboard:  Example: ["/command1, /command2", "/command3"]
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]
            message_tag:  Example: msg_to_edit"""
        ...

    @staticmethod
    def send_poll(*, question: str, options: str, config_entry_id: str | None=None, target: str | None=None, is_anonymous: bool=True, allows_multiple_answers: bool | None=None, open_period: int | None=None, disable_notification: bool | None=None, timeout: int | None=None, reply_to_message_id: float | None=None, message_thread_id: float | None=None) -> dict[str, Any]:
        """

        Args:
            options:  Example: ["Option 1", "Option 2", "Option 3"]
            target:  Example: [12345, 67890] or 12345"""
        ...

    @staticmethod
    def edit_message(*, message_id: str, chat_id: str, config_entry_id: str | None=None, message: str | None=None, title: str | None=None, parse_mode: Literal['', 'html', 'markdown', 'markdownv2', 'plain_text'] | None=None, disable_web_page_preview: bool | None=None, inline_keyboard: Any | None=None):
        """

        Args:
            message_id:  Example: {{ trigger.event.data.message.message_id }}
            chat_id:  Example: 12345
            message:  Example: The garage door has been open for 10 minutes.
            title:  Example: Your Garage Door Friend
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]"""
        ...

    @staticmethod
    def edit_message_media(*, message_id: str, chat_id: str, config_entry_id: str | None=None, timeout: int | None=None, media_type: Literal['', 'animation', 'audio', 'document', 'photo', 'video'] | None=None, url: str | None=None, url_options=None, file: str | None=None, caption: str | None=None, inline_keyboard: Any | None=None):
        """

        Args:
            message_id:  Example: {{ trigger.event.data.message.message_id }}
            chat_id:  Example: 12345
            url:  Example: http://example.org/path/to/the/image.png
            file:  Example: /path/to/the/image.png
            caption:  Example: Document Title xy
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]"""
        ...

    @staticmethod
    def edit_caption(*, message_id: str, chat_id: str, caption: str, config_entry_id: str | None=None, inline_keyboard: Any | None=None):
        """

        Args:
            message_id:  Example: {{ trigger.event.data.message.message_id }}
            chat_id:  Example: 12345
            caption:  Example: The garage door has been open for 10 minutes.
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]"""
        ...

    @staticmethod
    def edit_replymarkup(*, message_id: str, chat_id: str, inline_keyboard: Any, config_entry_id: str | None=None):
        """

        Args:
            message_id:  Example: {{ trigger.event.data.message.message_id }}
            chat_id:  Example: 12345
            inline_keyboard:  Example: ["/button1, /button2", "/button3"] or [[["Text button1", "/button1"], ["Text button2", "/button2"]], [["Text button3", "/button3"]]]"""
        ...

    @staticmethod
    def answer_callback_query(*, message: str, callback_query_id: str, show_alert: bool, config_entry_id: str | None=None, timeout: int | None=None):
        """

        Args:
            message:  Example: OK, I'm listening
            callback_query_id:  Example: {{ trigger.event.data.id }}"""
        ...

    @staticmethod
    def delete_message(*, message_id: str, chat_id: str, config_entry_id: str | None=None):
        """

        Args:
            message_id:  Example: {{ trigger.event.data.message.message_id }}
            chat_id:  Example: 12345"""
        ...

    @staticmethod
    def leave_chat(*, chat_id: str, config_entry_id: str | None=None):
        """

        Args:
            chat_id:  Example: 12345"""
        ...

    @staticmethod
    def set_message_reaction(*, message_id: str, chat_id: str, reaction: str, config_entry_id: str | None=None, is_big: bool | None=None):
        """

        Args:
            message_id:  Example: 54321
            chat_id:  Example: 12345
            reaction:  Example: 👍"""
        ...

class telegram_client:

    @staticmethod
    def send_messages(*, config_entry_id: str | None=None, target_username: str | None=None, target_id: str | None=None, message: str | None=None, reply_to: float | None=None, parse_mode: Literal['', 'html', 'markdown'] | None=None, link_preview: bool | None=None, file: str | None=None, force_document: bool | None=None, clear_draft: bool | None=None, keyboard: Any | None=None, inline_keyboard: Any | None=None, keyboard_resize: bool | None=None, keyboard_single_use: bool | None=None, silent: bool | None=None, supports_streaming: bool | None=None, schedule: datetime | None=None, comment_to: float | None=None, nosound_video: bool | None=None):
        """

        Args:
            target_username:  Example: me
            message:  Example: This is the test message, sent from **Telegram client** for Home Assistant.
            parse_mode:  Example: markdown
            file:  Example: configuration.yaml
            inline_keyboard:  Example: [[{'text': '😂', 'data': 'joy'}, {'text': '🤣', 'data': 'rofl'}, {'text': '😅', 'data': 'sweat'}], [{'text': '😀', 'data': 'grinning'}, {'text': '😃', 'data': 'smiley'}, {'text': '😄', 'data': 'smile'}]]"""
        ...

    @staticmethod
    def edit_message(*, config_entry_id: str, message: float, text: str, target_username: str | None=None, target_id: float | None=None, parse_mode: Literal['', 'html', 'markdown'] | None=None, link_preview: bool | None=None, file: str | None=None, force_document: bool | None=None, keyboard: Any | None=None, inline_keyboard: Any | None=None, keyboard_resize: bool | None=None, keyboard_single_use: bool | None=None, supports_streaming: bool | None=None, schedule: datetime | None=None):
        """

        Args:
            message:  Example: 100
            text:  Example: **New** message text.
            target_username:  Example: me
            parse_mode:  Example: markdown
            file:  Example: configuration.yaml
            inline_keyboard:  Example: [[{'text': '😂', 'data': 'joy'}, {'text': '🤣', 'data': 'rofl'}, {'text': '😅', 'data': 'sweat'}], [{'text': '😀', 'data': 'grinning'}, {'text': '😃', 'data': 'smiley'}, {'text': 'smile', 'data': '😄'}]]"""
        ...

    @staticmethod
    def delete_messages(*, config_entry_id: str, message_ids: str, target_username: str | None=None, target_id: str | None=None, revoke: bool | None=None):
        """

        Args:
            message_ids:  Example: 2
            target_username:  Example: me"""
        ...

class template:

    @staticmethod
    def reload():
        ...

class _text_state(StateVal):
    max: int
    min: int
    mode: str
    pattern: Any
    restored: bool
    supported_features: int

    def set_value(self, value: str):
        """

        Args:
            value:  Example: Hello world!"""
        ...

class text:
    valve_kitchen_programming_mode: _text_state
    ijai_de_1027836802_v3_on_p_2_9: _text_state
    ijai_de_1027836802_v3_cur_lang_p_7_21: _text_state
    ijai_de_1027836802_v3_room_data_p_8_13: _text_state
    ijai_de_1027836802_v3_zone_points_p_9_2: _text_state
    ijai_de_1027836802_v3_restrict_points_p_9_3: _text_state
    ijai_de_1027836802_v3_target_point_p_9_5: _text_state
    valve_office_workdays_schedule: _text_state
    valve_office_holidays_schedule: _text_state
    valve_room_workdays_schedule: _text_state
    valve_room_holidays_schedule: _text_state
    valve_bedroom_workdays_schedule: _text_state
    valve_bedroom_holidays_schedule: _text_state

    @staticmethod
    def set_value(*, entity_id: str, value: str):
        """

        Args:
            entity_id: Entity ID
            value:  Example: Hello world!"""
        ...

class _time_state(StateVal):
    cycle_timer: str
    random_timer: str

    def set_value(self, time: str):
        """

        Args:
            time:  Example: 22:15"""
        ...

class time:
    wine_fridge_tl_timer: _time_state
    orbitrack_tl_timer: _time_state

    @staticmethod
    def set_value(*, entity_id: str, time: str):
        """

        Args:
            entity_id: Entity ID
            time:  Example: 22:15"""
        ...

class timer:

    @staticmethod
    def reload():
        ...

    @staticmethod
    def start(*, entity_id: str, duration: str | None=None):
        """

        Args:
            entity_id: Entity ID
            duration:  Example: 00:01:00 or 60"""
        ...

    @staticmethod
    def pause(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def cancel(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def finish(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def change(*, entity_id: str, duration: str=0):
        """

        Args:
            entity_id: Entity ID
            duration:  Example: 00:01:00, 60 or -60"""
        ...

    @staticmethod
    def set_duration(*, entity_id: str, duration: str):
        """Set duration for an existing timer.

        Args:
            entity_id: Entity ID
            duration: New duration for the timer, as a timedelta string. Example: 00:01:00, 60"""
        ...

class _tts_state(StateVal):
    access_tokens: dict
    restored: bool
    supported_features: int

    def speak(self, *, media_player_entity_id: str, message: str, cache: bool=True, language: str | None=None, options: Any | None=None):
        """

        Args:
            message:  Example: My name is hanna
            language:  Example: ru
            options:  Example: platform specific"""
        ...

class tts:
    google_uk_com_ua: _tts_state
    google_en_com_ua: _tts_state
    home_assistant_cloud: _tts_state
    styletts2: _tts_state
    google_ai_tts: _tts_state
    edge_tts_4: _tts_state
    edge: _tts_state

    @staticmethod
    def speak(*, entity_id: str, media_player_entity_id: str, message: str, cache: bool=True, language: str | None=None, options: Any | None=None):
        """

        Args:
            entity_id: Entity ID
            message:  Example: My name is hanna
            language:  Example: ru
            options:  Example: platform specific"""
        ...

    @staticmethod
    def clear_cache():
        ...

    @staticmethod
    def cloud_say(*, entity_id: str, message: str, cache: bool=False, language: str | None=None, options: Any | None=None):
        """Say something using text-to-speech on a media player with cloud.

        Args:
            message:  Example: My name is hanna
            language:  Example: ru
            options:  Example: platform specific"""
        ...

class unifi:

    @staticmethod
    def reconnect_client(*, device_id):
        ...

    @staticmethod
    def remove_clients():
        ...

class _update_state(StateVal):
    auto_update: bool
    display_precision: int
    entity_picture: str
    in_progress: bool
    installed_version: str
    latest_version: str
    release_summary: Any
    release_url: str
    restored: bool
    skipped_version: str
    supported_features: int
    title: str
    update_percentage: Any

    def install(self, *, version: str | None=None, backup: bool | None=None):
        """

        Args:
            version:  Example: 1.0.0"""
        ...

    def skip(self):
        ...

    def clear_skipped(self):
        ...

class update:
    home_assistant_supervisor_update: _update_state
    home_assistant_core_update: _update_state
    home_assistant_google_drive_backup_update: _update_state
    log_viewer_update: _update_state
    mosquitto_broker_update: _update_state
    samba_share_update: _update_state
    studio_code_server_update: _update_state
    ssh_web_terminal_update: _update_state
    nextcloud_backup_update: _update_state
    unifi_device_update_24_5a_4c_11_20_bc: _update_state
    unifi_device_update_78_45_58_f7_db_fb: _update_state
    unifi_device_update_74_83_c2_fd_05_57: _update_state
    home_assistant_operating_system_update: _update_state
    tasmoadmin_update: _update_state
    esphome_update: _update_state
    tailscale_update: _update_state
    office_temphum_zb: _update_state
    socket_cat_mat: _update_state
    ikea_tradfri: _update_state
    projector_socket: _update_state
    vlc_update: _update_state
    usw_lite_16_poe: _update_state
    zigbee2mqtt_slzb_update: _update_state
    clearglass_update: _update_state
    ssh_command_update: _update_state
    gismeteo_update: _update_state
    card_tools_update: _update_state
    badge_card_update: _update_state
    local_llm_conversation_update: _update_state
    hacs_update: _update_state
    slate_theme_update: _update_state
    adaptive_cover_update: _update_state
    xiaomi_miot_auto_update: _update_state
    flex_table_highly_customizable_data_visualization_update: _update_state
    check_weather_update: _update_state
    edgeos_ubiquiti_update: _update_state
    dahua_update: _update_state
    entity_attributes_card_update: _update_state
    local_tuya_update: _update_state
    microsoft_edge_tts_update: _update_state
    frigate_update: _update_state
    fold_entity_row_update: _update_state
    battery_state_card_entity_row_update: _update_state
    dahua_vto_update: _update_state
    stack_in_card_update: _update_state
    battery_entity_row_update: _update_state
    lun_misto_air_update: _update_state
    lovelace_card_templater_update: _update_state
    lovelace_google_keep_card_update: _update_state
    upnp_availability_update: _update_state
    xiaomi_cloud_map_extractor_update: _update_state
    scheduler_component_update: _update_state
    cozytouch_update: _update_state
    card_mod_update: _update_state
    nova_poshta_update: _update_state
    lovelace_lock_card_update: _update_state
    auto_entities_update: _update_state
    mini_graph_card_update: _update_state
    weather_card_update: _update_state
    mushroom_update: _update_state
    simpleicons_update: _update_state
    multiple_entity_row_update: _update_state
    tabbed_card_update: _update_state
    custom_icons_update: _update_state
    psexec_api_update: _update_state
    pyscript_update: _update_state
    spook_your_homie_update: _update_state
    better_thermostat_ui_update: _update_state
    passive_ble_monitor_integration_update: _update_state
    restriction_card_update: _update_state
    apexcharts_card_update: _update_state
    yasno_outages_update: _update_state
    battery_notes_update: _update_state
    bermuda_ble_trilateration_update: _update_state
    search_card_update: _update_state
    sonoff_lan_update: _update_state
    scheduler_card_update: _update_state
    qingping_local_cloud_update: _update_state
    ssh_sensor_update: _update_state
    vertical_stack_in_card_update: _update_state
    mini_media_player_update: _update_state
    tuya_local_update: _update_state
    ecoflowcloud_update: _update_state
    mushroom_themes_update: _update_state
    layout_card_update: _update_state
    ytube_music_player_update: _update_state
    ecoflow_update: _update_state
    xiaomi_multifunction_air_monitor_update: _update_state
    amoled_theme_update: _update_state
    browser_mod_update: _update_state
    llm_vision_update: _update_state
    bubble_card_update: _update_state
    slzb_06p10_core_firmware: _update_state
    slzb_06p10_zigbee_firmware: _update_state
    glances_update: _update_state
    xiaomi_home_update: _update_state
    valve_office: _update_state
    valve_room: _update_state
    valve_bedroom: _update_state
    openai_tts_speech_service_update: _update_state
    music_assistant_server_update: _update_state
    xtend_tuya_update: _update_state
    yt_music_po_token_generator_update: _update_state
    bedroom_entrance: _update_state
    lovelace_grocy_chores_card_update: _update_state
    grocy_custom_component_update: _update_state
    telegram_client_update: _update_state
    openwebui_conversation_update: _update_state
    calendar_card_pro_update: _update_state
    mediocre_hass_media_player_cards_update: _update_state
    gaggiuino_update: _update_state
    relay_laundry: _update_state
    matter_server_update: _update_state
    automation_inspector_update: _update_state
    webrtc_camera_update: _update_state
    go2rtc_update: _update_state
    material_symbols_update: _update_state
    aliexpress_package_tracker_update: _update_state
    aliexpress_package_tracker_card_update: _update_state
    portainer_update: _update_state
    mushroom_dashboard_strategy_update: _update_state
    extended_openai_conversation_update: _update_state
    google_maps_card_update: _update_state
    pi_hole_core_update_available: _update_state
    pi_hole_web_update_available: _update_state
    pi_hole_ftl_update_available: _update_state
    ollama_vision_update: _update_state
    embedded_view_card_update: _update_state
    google_maps_update: _update_state
    vnc_viewer_update: _update_state
    beszel_agent_branch_update: _update_state
    u7_pro: _update_state
    ha_weathersense_update: _update_state
    meteogram_card_update: _update_state
    sleep_as_android_update: _update_state
    speedtest_update: _update_state
    music_assistant_jukebox_update: _update_state
    openai_whisper_cloud_update: _update_state
    bathroom_vents: _update_state
    unraid_api_update: _update_state
    local_openai_llm_update: _update_state
    svitlo_yeah_svitlo_e_update: _update_state
    beszel_api_update: _update_state
    ecoflow_ble_update: _update_state
    ecoflow_ble_update_2: _update_state
    room_accent_light: _update_state

    @staticmethod
    def install(*, entity_id: str, version: str | None=None, backup: bool | None=None):
        """

        Args:
            entity_id: Entity ID
            version:  Example: 1.0.0"""
        ...

    @staticmethod
    def skip(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def clear_skipped(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class _vacuum_state(StateVal):
    alarm: int
    battery_level: int
    fan_speed: str
    fan_speed_list: list
    state_updater: str
    supported_features: int

    def start(self):
        ...

    def pause(self):
        ...

    def return_to_base(self):
        ...

    def clean_spot(self):
        ...

    def locate(self):
        ...

    def stop(self):
        ...

    def set_fan_speed(self, fan_speed: str):
        """

        Args:
            fan_speed:  Example: low"""
        ...

    def send_command(self, *, command: str, params: Any | None=None):
        """

        Args:
            command:  Example: set_dnd_timer
            params:  Example: { "key": "value" }"""
        ...

class vacuum:
    mop_2_pro: _vacuum_state
    ijai_de_1027836802_v3: _vacuum_state

    @staticmethod
    def start(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def pause(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def return_to_base(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def clean_spot(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def locate(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def stop(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_fan_speed(*, entity_id: str, fan_speed: str):
        """

        Args:
            entity_id: Entity ID
            fan_speed:  Example: low"""
        ...

    @staticmethod
    def send_command(*, entity_id: str, command: str, params: Any | None=None):
        """

        Args:
            entity_id: Entity ID
            command:  Example: set_dnd_timer
            params:  Example: { "key": "value" }"""
        ...

class valve:

    @staticmethod
    def open_valve(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def close_valve(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_valve_position(*, entity_id: str, position: int):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def stop_valve(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def toggle(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

class wake_on_lan:

    @staticmethod
    def send_magic_packet(*, mac: str, broadcast_address: str | None=None, broadcast_port: float=9):
        """

        Args:
            mac:  Example: aa:bb:cc:dd:ee:ff
            broadcast_address:  Example: 192.168.255.255"""
        ...

class _water_heater_state(StateVal):
    away_mode: str
    current_temperature: float
    max_temp: float
    min_temp: float
    operation_list: list
    operation_mode: str
    supported_features: int
    target_temp_high: Any
    target_temp_low: Any
    temperature: float

    def turn_on(self):
        ...

    def turn_off(self):
        ...

    def set_away_mode(self, away_mode: bool):
        ...

    def set_temperature(self, *, temperature: float, operation_mode: str | None=None):
        """

        Args:
            operation_mode:  Example: eco"""
        ...

    def set_operation_mode(self, operation_mode: str):
        """

        Args:
            operation_mode:  Example: eco"""
        ...

class water_heater:
    boiler: _water_heater_state

    @staticmethod
    def turn_on(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def turn_off(*, entity_id: str):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_away_mode(*, entity_id: str, away_mode: bool):
        """

        Args:
            entity_id: Entity ID"""
        ...

    @staticmethod
    def set_temperature(*, entity_id: str, temperature: float, operation_mode: str | None=None):
        """

        Args:
            entity_id: Entity ID
            operation_mode:  Example: eco"""
        ...

    @staticmethod
    def set_operation_mode(*, entity_id: str, operation_mode: str):
        """

        Args:
            entity_id: Entity ID
            operation_mode:  Example: eco"""
        ...

class _weather_state(StateVal):
    apparent_temperature: float
    attribution: str
    cloud_coverage: int | float
    dew_point: float
    humidity: int
    precipitation_unit: str
    pressure: float
    pressure_unit: str
    supported_features: int
    temperature: float
    temperature_unit: str
    uv_index: float
    visibility: float
    visibility_unit: str
    wind_bearing: int | float
    wind_gust_speed: float
    wind_speed: float
    wind_speed_unit: str

    def get_forecasts(self, type: Literal['', 'daily', 'hourly', 'twice_daily']) -> dict[str, Any]:
        ...

class weather:
    forecast_home: _weather_state
    home: _weather_state

    @staticmethod
    def get_forecasts(*, entity_id: str, type: Literal['', 'daily', 'hourly', 'twice_daily']) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID"""
        ...

class workday:

    @staticmethod
    def check_date(*, entity_id: str, check_date: datetime | None=None) -> dict[str, Any]:
        """

        Args:
            entity_id: Entity ID
            check_date:  Example: 2022-12-25"""
        ...

class xiaomi_aqara:

    @staticmethod
    def play_ringtone(*, gw_mac: str, ringtone_id: str, ringtone_vol: int | None=None):
        """

        Args:
            gw_mac:  Example: 34ce00880088
            ringtone_id:  Example: 8"""
        ...

    @staticmethod
    def stop_ringtone(*, gw_mac: str):
        """

        Args:
            gw_mac:  Example: 34ce00880088"""
        ...

    @staticmethod
    def add_device(*, gw_mac: str):
        """

        Args:
            gw_mac:  Example: 34ce00880088"""
        ...

    @staticmethod
    def remove_device(*, device_id: str, gw_mac: str):
        """

        Args:
            device_id:  Example: 158d0000000000
            gw_mac:  Example: 34ce00880088"""
        ...

class xiaomi_miot:

    @staticmethod
    def get_token(*, name: str) -> dict[str, Any]:
        """Get xiaomi device token.

        Args:
            name: Keyword of device name in Mihome / IP / Model."""
        ...

    @staticmethod
    def renew_devices(*, username: str | None=None):
        """Renew xiaomi devices.

        Args:
            username: Xiaomi Account ID / Email / Phone."""
        ...

    @staticmethod
    def reload():
        ...

    @staticmethod
    def send_command(*, entity_id: str, method: str, params: Any) -> dict[str, Any]:
        """Send miio command.

        Args:
            entity_id: ID of the entity. Example: light.yeelight_living_e92c
            method: Method of the command. Example: set_power
            params: Params for the method. Example: ['on']"""
        ...

    @staticmethod
    def set_property(*, entity_id: str, field: str, value: Any) -> dict[str, Any]:
        """Set miot property.

        Args:
            entity_id: ID of the entity. Example: climate.xiaomi_mc5_374e
            field: Field of property. Example: air_conditioner.on
            value: Value of property. Example: True"""
        ...

    @staticmethod
    def set_miot_property(*, entity_id: str, siid: float, piid: float, value: Any) -> dict[str, Any]:
        """Set miot property by siid/piid.

        Args:
            entity_id: ID of the entity. Example: climate.xiaomi_mc5_374e
            siid: Miot service ID. Example: 2
            piid: Miot property ID. Example: 1
            value: Miot property value. Example: True"""
        ...

    @staticmethod
    def get_properties(*, entity_id: str, mapping: Any, update_entity: bool=False) -> dict[str, Any]:
        """Get miot properties.

        Args:
            entity_id: ID of the entity. Example: climate.xiaomi_mc5_374e
            mapping: Mapping for properties. Example: [{"siid": 2, "piid": 1}, {"siid": 3, "piid": 1}]
            update_entity: Update to entity state attributes. Example: True"""
        ...

    @staticmethod
    def call_action(*, entity_id: str, siid: float, aiid: float, params: Any | None=None) -> dict[str, Any]:
        """Call miot action.

        Args:
            entity_id: ID of the entity. Example: media_player.xiaoai_x08c
            siid: Miot service ID. Example: 3
            aiid: Miot action ID. Example: 5
            params: Miot action params. Example: ['Turn on light', 1]"""
        ...

    @staticmethod
    def get_device_data(*, entity_id: str, key: str, type: Literal['', 'prop', 'event', 'prop_cal_day', 'prop_cal_week', 'prop_cal_month', 'store']='prop', time_start: float | None=None, time_end: float | None=None, limit: float | None=None, group: Literal['', 'raw', 'hour', 'day', 'week', 'month']='raw') -> dict[str, Any]:
        """Get xiaomi device data from cloud.

        Args:
            entity_id: ID of the entity. Example: sensor.xiaomi_lock
            key: Data key. Example: power
            type: Data type. Example: prop
            time_start: From the unix timestamp.
            time_end: To the unix timestamp.
            limit: Limit of results. Example: 10
            group: Results grouping. Example: raw"""
        ...

    @staticmethod
    def get_bindkey(*, entity_id: str, did: str | None=None) -> dict[str, Any]:
        """Get bindkey for ble device from cloud.

        Args:
            entity_id: ID of the entity. Example: sensor.lywsd03mmc_temperature
            did: Xiaomi device ID."""
        ...

    @staticmethod
    def request_xiaomi_api(*, entity_id: str, api: str, data: Any | None=None, method: Literal['', 'POST', 'GET']='POST', crypt: bool=True, sid: Literal['', 'xiaomiio', 'micoapi', 'i.mi.com']='xiaomiio') -> dict[str, Any]:
        """Request xiaomi cloud api.

        Args:
            entity_id: ID of the entity. Example: sensor.xiaomi_device
            api: Xiaomi API path. Example: /home/device_list
            data: Xiaomi API request data. Example: {'getVirtualModel':true}
            method: Request method. Example: POST
            crypt: Crypt data. Example: True
            sid: Xiaomi service ID. Example: xiaomiio"""
        ...

    @staticmethod
    def intelligent_speaker(*, entity_id: str, text: str, execute: bool=False, silent: bool=False) -> dict[str, Any]:
        """Play text on Xiaoai speaker / Execute text directive / 小爱TTS及执行语音命令

        Args:
            entity_id: ID of the entity. Example: media_player.xiaoai_x08c
            text: Text content. Example: Turn on light
            execute: Execute text directive. Example: True
            silent: Silent execution."""
        ...

    @staticmethod
    def xiaoai_wakeup(*, entity_id: str, text: str | None=None) -> dict[str, Any]:
        """Wake up the Xiaoai speaker / 唤醒小爱音箱

        Args:
            entity_id: ID of the xiaoai entity. Example: media_player.xiaoai_x08c
            text: Text content for wake up. Example: Livingroom light"""
        ...

class xtend_tuya:

    @staticmethod
    def get_camera_stream_url(*, device_id, source='tuya_sharing', stream_type='rtsp'):
        """

        Args:
            source:  Example: tuya_sharing
            stream_type:  Example: rtsp"""
        ...

    @staticmethod
    def call_api(*, source, method='GET', url, payload=None):
        """

        Args:
            source:  Example: tuya_sharing
            method:  Example: GET
            url:  Example: /v1.0/devices/{device_id}/webrtc-configs"""
        ...

    @staticmethod
    def webrtc_get_ice_servers(*, device_id, session_id, source='tuya_iot', format='GO2RTC'):
        """

        Args:
            session_id:  Example: test1
            source:  Example: tuya_iot
            format:  Example: SimpleWHEP"""
        ...

    @staticmethod
    def webrtc_sdp_exchange(*, device_id, session_id, source='tuya_iot'):
        """

        Args:
            session_id:  Example: test1
            source:  Example: tuya_iot"""
        ...

    @staticmethod
    def webrtc_debug(*, session_id, source='tuya_iot'):
        """

        Args:
            session_id:  Example: test1
            source:  Example: tuya_iot"""
        ...

class zone:

    @staticmethod
    def reload():
        ...

    @staticmethod
    def create(*, name: str, latitude: float, longitude: float, icon: str | None=None, radius: float=100):
        """Create a new zone in Home Assistant on the fly.

        Args:
            name: Name of the zone
            latitude: Latitude of the zone
            longitude: Longitude of the zone
            icon: Icon to use for the zone
            radius: Radius of the zone"""
        ...

    @staticmethod
    def update(*, entity_id: str, name: str | None=None, icon: str | None=None, latitude: float | None=None, longitude: float | None=None, radius: float=100):
        """Update properties of a zone on the fly.

        Args:
            entity_id: The ID of the entity (or entities) to update.
            name: Name of the zone
            icon: Icon to use for the zone
            latitude: Latitude of the zone
            longitude: Longitude of the zone
            radius: Radius of the zone"""
        ...

    @staticmethod
    def delete(*, entity_id: str):
        """Delete a zone. This works only with zones created and managed via the UI. Zones created and managed in YAML cannot be managed by Spook.

        Args:
            entity_id: The ID of the entity (or entities) to remove."""
        ...