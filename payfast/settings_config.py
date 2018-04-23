from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .config import AbstractPayfastConfig
from .constants import Constants


class WebIntegrationConfig(AbstractPayfastConfig):
    """Manage Plugin's configuration from the project's settings.

    It gets all information required by the plugin from the project's settings,
    and can be used as a base class for specific cases.

    The following settings are required in production i.e DEBUG is set to False.
    If debug is set to false you may omit these settings and system will fallback to
    the payfast defaults:

    * :data:`PAYFAST_MERCHANT_ID`
    * :data:`PAYFAST_MERCHANT_KEY`

    """
    def __init__(self):
        """Initialize configuration and check project's settings.

        The only setting requirement here is: If PAYFAST_MERCHANT_ID is set then PAYFAST_MERCHANT_KEY must
        also be set and visa versa.
        """
        merchant_settings = [getattr(settings, 'PAYFAST_MERCHANT_ID', None), getattr(settings, 'PAYFAST_MERCHANT_KEY', None)]

        # A check to see if only one of the required merchant settings was set
        if not all(merchant_settings) and any(merchant_settings):
            raise ImproperlyConfigured(
                "You must declare both PAYFAST_MERCHANT_ID and PAYFAST_MERCHANT_KEY or neither in the settings module. "
                "You have declared only one of these settings, please check your settings module."
            )

    def get_merchant_id(self):
        """Return :data:`PAYFAST_MERCHANT_ID`."""
        return getattr(settings, 'PAYFAST_MERCHANT_ID', Constants.MERCHANT_ID_DEV)

    def get_action_url(self):
        """Return :data:`PAYFAST_ACTION_URL`.
        Returns the live payfast action url if the merchant id and the merchant key are set. Otherwise the sandbox url
        is returned.
        """
        merchant_id = getattr(settings, 'PAYFAST_MERCHANT_ID', False)
        merchant_key = getattr(settings, 'PAYFAST_MERCHANT_KEY', False)
        return Constants.ACTION_URL_LIVE if merchant_id and merchant_key else Constants.ACTION_URL_DEV

    def get_merchant_key(self):
        """Return :data:`PAYFAST_MERCHANT_KEY`."""
        return getattr(settings, 'PAYFAST_MERCHANT_KEY', Constants.MERCHANT_KEY_DEV)

    def get_passphrase(self):
        """Return :data:`PAYFAST_PASSPHRASE`. or None
        """
        return getattr(settings, 'PAYFAST_PASSPHRASE', None)

    def get_ip_address_header(self):
        """Return :data:`PAYFAST_IP_ADDRESS_HTTP_HEADER` or ``REMOTE_ADDR``.

        If the setting is not configured, the default value ``REMOTE_ADDR`` is
        returned instead. This is useful for situations where you are running behind
        a proxy and the real ip is passed in an alternate header.
        """
        return getattr(settings, 'PAYFAST_IP_ADDRESS_HTTP_HEADER', 'REMOTE_ADDR')
