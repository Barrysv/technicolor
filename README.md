# Home Assistant VDSL modem sensor integration
Modem sensor for Home Assistant using xdslctl command via SSH

Rewrote this sensor completely.  It connects to the modem using the paramiko ssh python library and fetches the modem stats by running the XDSLCTL command.

This means it should be able to work with pretty much any modem that can be connected to via SSH and can run this command.  By changing the Regex and cmd strings it should be possible to extract from any modem that uses a different command and has a differing output format.  It should be robust for all modems of the same family although have only used it with my TG789vac V2.  Please submit a pull request if you would like to support additional modems.


HOW TO INSTALL:
1. Do *either* of the following, then restart Home Assistant to load the integration;  
   - add this repository's URL to HACS as a custom integration repository, and download using HACS, *or*  
   - copy the contents of /custom_components/xdslctl into .homeassistant/custom_components/xdslctl  
2. in your sensors.yaml file include the following (*or* merge into your configuration.yaml sensor: section)
```
- platform: xdslctl
  name: modem
  host: 10.1.1.1                   # IP address of the modem
  username: !secret modem_username # use root instead of admin
  password: !secret modem_password # modem admin password
  scan_interval: 600 # or less if you want more frequent updates
- platform: template
  sensors:
    up_rate:
      friendly_name: 'DSL Up Rate'
      device_class: data_rate
      unit_of_measurement: 'Mbit/s'
      value_template: '{{ "%.2f" | format(states.sensor.modem.attributes.up_rate | float / 1000) }}'
    down_rate:
      friendly_name: 'DSL Down Rate'
      device_class: data_rate
      unit_of_measurement: 'Mbit/s'
      value_template: '{{ "%.2f"|format(states.sensor.modem.attributes.down_rate | float / 1000) }}'
    modem_uptime_text:
      friendly_name: 'Modem Uptime Text'
      value_template: '{{ states.sensor.modem.attributes.modem_uptime }}'
    dsl_uptime_text:
      friendly_name: 'DSL Uptime Text'
      value_template: '{{ states.sensor.modem.attributes.dsl_uptime }}'
    dsl_uptime_days:
      friendly_name: 'DSL Uptime Days'
      device_class: duration
      unit_of_measurement: 'd'
      value_template: '{{ "%.2f"|format(states.sensor.modem.attributes.dsl_uptime_secs | float / 86400) }}'
    modem_uptime_days:
      friendly_name: 'Modem Uptime Days'
      device_class: duration
      unit_of_measurement: 'd'
      value_template: '{{ "%.2f"|format(states.sensor.modem.attributes.modem_uptime_secs | float / 86400) }}'
    dsl_up_noisemargin:
      friendly_name: 'DSL Up Noisemargin'
      unit_of_measurement: 'dB'
      value_template: '{{ states.sensor.modem.attributes.up_noisemargin}}'
    dsl_down_noisemargin:
      friendly_name: 'DSL Down Noisemargin'
      unit_of_measurement: 'dB'
      value_template: '{{ states.sensor.modem.attributes.down_noisemargin}}'
    max_up_rate:
      friendly_name: 'DSL Max Up Rate'
      device_class: data_rate
      unit_of_measurement: 'Mbit/s'
      value_template: '{{ "%.2f"|format(states.sensor.modem.attributes.up_maxrate | float / 1000) }}'
    max_down_rate:
      friendly_name: 'DSL Max Down Rate'
      device_class: data_rate
      unit_of_measurement: 'Mbit/s'
      value_template: '{{ "%.2f"|format(states.sensor.modem.attributes.down_maxrate | float / 1000) }}'
    crc_up:
      friendly_name: 'DSL Up Errors'
      unit_of_measurement: 'errors'
      value_template: '{{ states.sensor.modem.attributes.CRC_up }}'
    crc_down:
      friendly_name: 'DSL Down Errors'
      unit_of_measurement: 'errors'
      value_template: '{{ states.sensor.modem.attributes.CRC_down }}'
    es_up:
      friendly_name: 'DSL Errored Seconds Up'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.ES_up }}'
    es_down:
      friendly_name: 'DSL Errored Seconds Down'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.ES_down }}'
    ses_up:
      friendly_name: 'DSL Severely Errored Seconds Up'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.SES_up }}'
    ses_down:
      friendly_name: 'DSL Severely Errored Seconds Down'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.SES_down }}'
    attn_up:
      friendly_name: 'DSL Line Attenuation Up'
      unit_of_measurement: 'dB'
      value_template: '{{ states.sensor.modem.attributes.attn_up }}'
    attn_down:
      friendly_name: 'DSL Line Attenuation Down'
      unit_of_measurement: 'dB'
      value_template: '{{ states.sensor.modem.attributes.attn_down }}'
    power_up:
      friendly_name: 'DSL Line Power Up'
      unit_of_measurement: 'dBm'
      value_template: '{{ states.sensor.modem.attributes.up_power }}'
    power_down:
      friendly_name: 'DSL Line Power Down'
      unit_of_measurement: 'dBm'
      value_template: '{{ states.sensor.modem.attributes.down_power }}'
```

3. Use Groups / lovelace to customise these into a card:
```
system_status:
  name: System
  entities:
    - sensor.modem
    - sensor.dsl_uptime
    - sensor.down_rate
    - sensor.up_rate
    - sensor.dsl_down_noisemargin
    - sensor.dsl_up_noisemargin
    - sensor.max_down_rate
    - sensor.max_up_rate
    - sensor.crc_down
    - sensor.crc_up
    - sensor.es_down
    - sensor.es_up
    - sensor.ses_down
    - sensor.ses_up
    - sensor.attn_down
    - sensor.attn_up
    - sensor.power_down
    - sensor.power_up
```
![Home assistant dashboard](/assets/images/Screenshot%202022-09-07%20at%204.07.04%20pm.png)
