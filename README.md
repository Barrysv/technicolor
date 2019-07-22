# technicolor
Technicolor modem sensor for home assistant

Rewrote this sensor completely.  It connects to the modem using the paramiko ssh python library and fetches the modem stats by running the XDSLCTL command.

This means it should be able to work with pretty much any modem that can be connected to via SSH and can run this command.  By changing the Regex and cmd strings it should be possible to extract from any modem that uses a different command and has a differing output format.  It should be robust for all modems of the same family although have only used it with my TG789vac V2.  Please submit a pull request if you would like to support additional modems.


HOW TO INSTALL:
1. Clone into .homeassistant/custom-components/technicolor
2. in your sensors.yaml file include the following.
```
- platform: technicolor
  name: modem
  host: 10.1.1.1                   # IP address of the modem
  username: !secret modem_username # use root instead of admin
  password: !secret modem_password # modem admin password
  scan_interval: 600 # or less if you want more frequent updates
- platform: template
  sensors:
    up_rate:
      friendly_name: 'Up rate'
      unit_of_measurement: 'kbps'
      value_template: '{{ states.sensor.modem.attributes.up_rate }}'
    down_rate:
      friendly_name: 'Down rate'
      unit_of_measurement: 'kbps'
      value_template: '{{ states.sensor.modem.attributes.down_rate }}'
    dsl_uptime:
      friendly_name: 'DSL uptime'
      unit_of_measurement: 'days'
      value_template: '{{ states.sensor.modem.attributes.dsl_uptime}}'
    dsl_up_noisemargin:
      friendly_name: 'DSL up noisemargin'
      unit_of_measurement: 'dB'
      value_template: '{{ states.sensor.modem.attributes.up_noisemargin}}'
    dsl_down_noisemargin:
      friendly_name: 'DSL down noisemargin'
      unit_of_measurement: 'dB'
      value_template: '{{ states.sensor.modem.attributes.down_noisemargin}}'
    max_up_rate:
      friendly_name: 'DSL max up rate'
      unit_of_measurement: 'kbps'
      value_template: '{{ states.sensor.modem.attributes.up_maxrate }}'
    max_down_rate:
      friendly_name: 'DSL max down rate'
      unit_of_measurement: 'kbps'
      value_template: '{{ states.sensor.modem.attributes.down_maxrate }}'
    crc_up:
      friendly_name: 'CRC up errors'
      unit_of_measurement: 'errors'
      value_template: '{{ states.sensor.modem.attributes.CRC_up }}'
    crc_down:
      friendly_name: 'CRC down errors'
      unit_of_measurement: 'errors'
      value_template: '{{ states.sensor.modem.attributes.CRC_down }}'
    es_up:
      friendly_name: 'Errored seconds up'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.ES_up }}'
    es_down:
      friendly_name: 'Errored seconds down'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.ES_down }}'
    ses_up:
      friendly_name: 'Severely Errored seconds up'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.SES_up }}'
    ses_down:
      friendly_name: 'Severely Errored seconds down'
      unit_of_measurement: 'seconds'
      value_template: '{{ states.sensor.modem.attributes.SES_down }}'
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

```
