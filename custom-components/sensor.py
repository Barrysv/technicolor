"""
Technicolor Modem sensor for Home Assistant
For more details about this platform, please refer to the documentation at
https://github.com/barrysv/technicolor
Barry Vayler
"""

from collections import OrderedDict
import logging
import voluptuous as vol

from homeassistant.const import (
    STATE_UNKNOWN, CONF_NAME, CONF_PASSWORD, CONF_USERNAME,
    CONF_HOST)
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv

DEFAULT_NAME = 'Technicolor Modem Sensor'
REQUIREMENTS = ['paramiko==2.4.2']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the technicolor modem sensor"""
    import paramiko #  hassio will get and install requirements
    add_devices([TechnicolorModemSensor(config)], True)
    
class TechnicolorModemSensor(Entity):
    """Representation of a modem Sensor."""
 
    def __init__(self, config):
        """Initialize the sensor."""
        address = config.get(CONF_HOST)
        username = config.get(CONF_USERNAME)
        password = config.get(CONF_PASSWORD)
        name = config.get(CONF_NAME)
        self._state = STATE_UNKNOWN
        self._name = name
        self._unit_of_measurement = None
        self._attributes = None
        self._available = False
        self._modemFetcher = FetchTechnicolorModemStats({'address':address, 'username':username, 'password':password})
 
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
 
    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
 
    @property
    def available(self):
        """Return if the sensor data is available."""
        return self._available
 
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
     
    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
         
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        stats = OrderedDict()
        self._modemFetcher.get(stats)
        self._available = len(stats) > 0
        self._attributes = dict(stats)
        self._state = stats['dsl_status']
        
class FetchTechnicolorModemStats(object):
    def __init__(self, config):
        import paramiko, os
        self._config = config
        self._data = None
        self._stderr = None
        self._errorcode = None
        self._cmd = 'xdslctl info --stats'
        self._regex_dsl_status = r"Status: (.*)"
        self._regex_max_up_down = r"Max:.*Upstream rate = (\d+).*Downstream rate = (\d+)"
        self._regex_act_up_down = r"Bearer:\t0.*Upstream rate = (\d+).*Downstream rate = (\d+)"
        self._regex_snr_up_down = r"SNR..dB.*?(\d+\.\d+)\t\t.(\d+\.\d+)"
        self._regex_attn_up_down = r"Attn.dB.*?(\d+\.\d+)\t\t.(\d+\.\d+)"
        self._regex_pwr_up_down = r"Pwr.dB.*?(\d+\.\d+)\t\t.(\d+\.\d+)"
        self._regex_totaltime = r"Total time = (.*)"
        self._regex_prev15 = r"Previous 15 minutes.*\nFEC:\t\t(\d+)\t\t(\d+)\nCRC:\t\t(\d+)\t\t(\d+)\nES:\t\t(\d+)\t\t(\d+)\nSES:\t\t(\d+)\t\t(\d+)"
        self._regex_sincelinktime = r"Since Link time = (\d.*)\nFEC:\t\t(\d+)\t\t(\d+)\nCRC:\t\t(\d+)\t\t(\d+)\nES:\t\t(\d+)\t\t(\d+)\nSES:\t\t(\d+)\t\t(\d+)"
        #hostkey = paramiko.util.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        #self._ssh.get_host_keys().add(self._config['address'], 'ssh-rsa', hostkey)
        self._connect()
    
    def get(self,res):
        if not self._ssh.get_transport():
            self._connect()
        if not self._ssh.get_transport():
            return None
        self.run_xdslctl()
        self.parsedata(res)    

    def _connect(self):
        try:
            self._ssh.connect(self._config['address'], username = self._config['username'], password = self._config['password'])
        except:
            _LOGGER.error("SSH connection refused by host {}".format(self._config['address']))
            self._disconnect()
            
    def _disconnect(self):
        self._ssh.close()
    
    def run_xdslctl(self):
        _, stdout, stderr = self._ssh.exec_command(self._cmd)
        self._data = stdout.read().decode('utf-8')
        self._stderr = stderr.read().decode('utf-8')
       
    def parsedata(self,res):
        import re
        matches_dsl_status = re.search(self._regex_dsl_status, self._data)
        matches_max_up_down = re.search(self._regex_max_up_down, self._data)
        matches_act_up_down = re.search(self._regex_act_up_down, self._data)
        matches_snr_up_down = re.search(self._regex_snr_up_down, self._data)
        matches_attn_up_down = re.search(self._regex_attn_up_down, self._data)
        matches_pwr_up_down = re.search(self._regex_pwr_up_down, self._data)
        matches_modem_uptime = re.search(self._regex_totaltime, self._data)
        matches_sincelinktime = re.search(self._regex_sincelinktime, self._data)
        #matches_prev15 = re.search(self._regex_prev15, self._data)

        def getmatches(matches,n):
            if len(matches.groups()) == n:
                return (matches.groups())
            else:
                return ((None,) * n)
        dsl_state, = getmatches(matches_dsl_status, 1)
        res['dsl_status'] = "Up" if dsl_state == "Showtime" else "Down"
        res['up_rate'], res['down_rate'] = getmatches(matches_act_up_down, 2)
        res['up_maxrate'], res['down_maxrate'] = getmatches(matches_max_up_down, 2)
        res['down_power'], res['up_power'] = getmatches(matches_pwr_up_down, 2)
        res['down_noisemargin'], res['up_noisemargin'] = getmatches(matches_snr_up_down, 2)     
        res['attn_down'], res['attn_up'] = getmatches(matches_attn_up_down, 2)
        res['modem_uptime'], = getmatches(matches_modem_uptime, 1)
        res['dsl_uptime'], res['FEC_down'], res['FEC_up'], res['CRC_down'], res['CRC_up'], \
          res['ES_down'], res['ES_up'], res['SES_down'], res['SES_up'] = getmatches(matches_sincelinktime, 9)
