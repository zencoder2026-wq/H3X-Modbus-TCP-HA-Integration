
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_PORT, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

class SolarHubConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
 

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
      
        return SolarHubOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
       
        errors = {}
        
        if user_input is not None:
            return self.async_create_entry(
                title=f"Solar Hub ({user_input['host']})", 
                data=user_input
            )

        schema = vol.Schema({
            vol.Required("host", default="192.168.1.10"): str,
            vol.Required("port", default=DEFAULT_PORT): int,
            # Optional: Allow setting it during initial add
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=schema, 
            errors=errors
        )


class SolarHubOptionsFlowHandler(config_entries.OptionsFlow):
    

    def __init__(self, config_entry):
        
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Default to existing option, or fallback to config, or default constant
        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, 
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_SCAN_INTERVAL, default=current_interval): int,
            }),
        )