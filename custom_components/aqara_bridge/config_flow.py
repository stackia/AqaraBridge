import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import (
    CONN_CLASS_LOCAL_PUSH,
    ConfigFlow,
    OptionsFlow,
    ConfigEntry
    )
from homeassistant.core import callback

from . import init_hass_data, data_masking, gen_auth_entry
from .core.const import *
_LOGGER = logging.getLogger(__name__)

DEVICE_GET_AUTH_CODE_CONFIG = vol.Schema(
    {
        vol.Required(CONF_FIELD_ACCOUNT): str,
        vol.Required(
            CONF_FIELD_COUNTRY_CODE, default=SERVER_COUNTRY_CODES_DEFAULT
        ): vol.In(SERVER_COUNTRY_CODES),
        vol.Optional(CONF_FIELD_REFRESH_TOKEN): str,
    }
)

DEVICE_GET_TOKEN_CONFIG = vol.Schema({vol.Required(CONF_FIELD_AUTH_CODE): str})


class AqaraBridgeFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle an Aqara Bridge config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self.account = None
        self.country_code = None
        self.account_type = None
        self._session = None
        self._device_manager = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        init_hass_data(self.hass)
        self._device_manager = self.hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
        auth_entry_id = self.hass.data[DOMAIN][HASS_DATA_AUTH_ENTRY_ID]
        self._session = self.hass.data[DOMAIN][HASS_DATA_AIOTCLOUD]
        if auth_entry_id:
            return await self.async_step_select_devices()
        else:
            # self._session = AiotCloud(
            #     aiohttp_client.async_create_clientsession(self.hass)
            # )
            # self.hass.data[DOMAIN][HASS_DATA_AIOTCLOUD] = self._session
            return await self.async_step_get_auth_code()

    async def async_step_get_auth_code(self, user_input=None):
        """Configure an aqara device through the Aqara Cloud."""
        errors = {}
        if user_input:
            self.account = user_input.get(CONF_FIELD_ACCOUNT)
            self.country_code = user_input.get(CONF_FIELD_COUNTRY_CODE)
            self.account_type = 0
            self._session.set_country(self.country_code)

            refresh_token = user_input.get(CONF_FIELD_REFRESH_TOKEN)
            if refresh_token and refresh_token != "":
                resp = await self._session.async_refresh_token(refresh_token)
                if resp["code"] == 0:
                    auth_entry = gen_auth_entry(
                        self.account,
                        self.account_type,
                        self.country_code,
                        resp["result"],
                    )
                    self.hass.async_add_job(
                        self.hass.config_entries.flow.async_init(
                            DOMAIN, context={"source": "get_token"}, data=auth_entry
                        )
                    )
                    return self.async_abort(reason="complete")
                else:
                    errors['base'] = 'refresh_token_error'
            else:
                resp = await self._session.async_get_auth_code(self.account, 0)
                if resp["code"] == 0:
                    return await self.async_step_get_token()
                else:
                    errors['base'] = 'auth_code_error'

        return self.async_show_form(
            step_id="get_auth_code",
            data_schema=DEVICE_GET_AUTH_CODE_CONFIG,
            errors=errors,
        )

    async def async_step_get_token(self, user_input=None):
        errors = {}
        if user_input:
            if CONF_FIELD_AUTH_CODE in user_input:
                auth_code = user_input.get(CONF_FIELD_AUTH_CODE)
                resp = await self._session.async_get_token(auth_code, self.account, 0)

                if resp["code"] == 0:
                    auth_entry = gen_auth_entry(
                        self.account,
                        self.account_type,
                        self.country_code,
                        resp["result"],
                    )
                    self.hass.async_add_job(
                        self.hass.config_entries.flow.async_init(
                            DOMAIN, context={"source": "get_token"}, data=auth_entry
                        )
                    )
                else:
                    errors["base"] = "cloud_credentials_incomplete"
            elif CONF_ENTRY_AUTH_ACCOUNT in user_input:
                return self.async_create_entry(
                    title=data_masking(user_input[CONF_ENTRY_AUTH_ACCOUNT], 4),
                    data=user_input,
                )

            return self.async_abort(reason="complete")

        return self.async_show_form(
            step_id="get_token", data_schema=DEVICE_GET_TOKEN_CONFIG, errors=errors
        )

class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self._account = None
        self._country_code= None
        self._account_type = 0
        self._refresh_token = None
        self._session = None
        
    async def async_step_init(self, user_input=None):
        """Configure an aqara device through the Aqara Cloud."""
        errors = {}
        if isinstance(user_input, dict):
            # 用户输入
            self._account = user_input.get(CONF_FIELD_ACCOUNT)
            self._country_code = user_input.get(CONF_FIELD_COUNTRY_CODE)
            if self._session is None:
                self._session = self.hass.data[DOMAIN][HASS_DATA_AIOTCLOUD]
            self._session.set_country(self._country_code)

            refresh_token = user_input.get(CONF_FIELD_REFRESH_TOKEN)
            if refresh_token and refresh_token != "":
                resp = await self._session.async_refresh_token(refresh_token)
                if resp["code"] == 0:
                    auth_entry = gen_auth_entry(
                        self._account,
                        self._account_type,
                        self._country_code,
                        resp["result"],
                    )
                    auth_entry[CONF_ENTRY_OPTION_REFRESH] = True
                    self.hass.config_entries.async_update_entry(self.config_entry, data=auth_entry)
                    return self.async_abort(reason="complete")
                else:
                    errors['base'] = 'refresh_token_error'
            else:
                resp = await self._session.async_get_auth_code(self.account, 0)
                if resp["code"] == 0:
                    return await self.async_step_get_token()
                else:
                    errors['base'] = 'auth_code_error'
        else:
            prev_input = {
                **self.config_entry.data,
                **self.config_entry.options,
            }
            config_scheme = vol.Schema(
                {
                    vol.Required(CONF_FIELD_ACCOUNT, default=prev_input.get(CONF_ENTRY_AUTH_ACCOUNT, vol.UNDEFINED)): str,
                    vol.Required(CONF_FIELD_COUNTRY_CODE, default=SERVER_COUNTRY_CODES_DEFAULT): vol.In(SERVER_COUNTRY_CODES),
                    vol.Optional(CONF_FIELD_REFRESH_TOKEN, default=prev_input.get(CONF_ENTRY_AUTH_REFRESH_TOKEN, vol.UNDEFINED)): str,
                }
            )
            return self.async_show_form(step_id="init", data_schema=config_scheme, errors=errors)

    async def async_step_get_token(self, user_input=None):
        errors = {}
        if user_input and CONF_FIELD_AUTH_CODE in user_input:
            auth_code = user_input.get(CONF_FIELD_AUTH_CODE)
            resp = await self._session.async_get_token(auth_code, self.account, 0)
            if resp["code"] == 0:
                auth_entry = gen_auth_entry(
                    self.account,
                    self.account_type,
                    self.country_code,
                    resp["result"],
                )
                auth_entry[CONF_ENTRY_OPTION_REFRESH] = True
                self.hass.config_entries.async_update_entry(self.config_entry, data=auth_entry)
                return self.async_abort(reason="complete")
            else:
                errors["base"] = "cloud_credentials_incomplete"
        return self.async_show_form(
            step_id="get_token", data_schema=DEVICE_GET_TOKEN_CONFIG, errors=errors
        )
