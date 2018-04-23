from django.test.utils import override_settings
from django.conf import settings
from payfast.config import get_config
from payfast.constants import Constants
from django.core.exceptions import ImproperlyConfigured
import unittest

# Fixtures
PAYFAST_MERCHANT_ID = 12345
PAYFAST_MERCHANT_KEY = 'mysecretkey'
PAYFAST_PASSPHRASE = 'mypassphrase'
PAYFAST_IP_ADDRESS_HTTP_HEADER = 'X_FORWARDED_FOR'


class ConfigTestCase(unittest.TestCase):

    @override_settings(PAYFAST_MERCHANT_KEY=PAYFAST_MERCHANT_KEY, PAYFAST_MERCHANT_ID=PAYFAST_MERCHANT_ID)
    def test_can_detect_incorrect_settings_configuration(self):

        # Both settings should not raise an exception
        try:
            get_config()
        except ImproperlyConfigured:
            self.fail("get_config() raised ImproperlyConfigured unexpectedly!")

        # Remove the merchant key setting
        del settings.PAYFAST_MERCHANT_KEY

        # Test for exception raised by only setting PAYFAST_MERCHANT_ID
        with self.assertRaises(ImproperlyConfigured):
            get_config()

        # Remove the merchant id setting
        del settings.PAYFAST_MERCHANT_ID

        # Absence of both merchant id and merchant key should not raise an exception
        try:
            get_config()
        except ImproperlyConfigured:
            self.fail("get_config() raised ImproperlyConfigured unexpectedly!")

        # Set PAYFAST_MERCHANT_KEY
        settings.PAYFAST_MERCHANT_KEY = PAYFAST_MERCHANT_KEY

        # Test for exception raised by only setting PAYFAST_MERCHANT_KEY
        with self.assertRaises(ImproperlyConfigured):
            get_config()

    @override_settings(PAYFAST_MERCHANT_ID=PAYFAST_MERCHANT_ID, PAYFAST_MERCHANT_KEY=PAYFAST_MERCHANT_KEY)
    def test_can_get_merchant_id(self):
        # Return the merchant id from the settings module
        self.assertEqual(get_config().get_merchant_id(), PAYFAST_MERCHANT_ID,
                         "Unable to retrieve merchant id from settings")

        # Remove the merchant id from settings
        del settings.PAYFAST_MERCHANT_ID
        del settings.PAYFAST_MERCHANT_KEY

        # Return the development id if setting is not present in settings
        self.assertEqual(get_config().get_merchant_id(), Constants.MERCHANT_ID_DEV,
                         "Cannot retrieve default development merchant id from Constants")

    @override_settings(PAYFAST_MERCHANT_KEY=PAYFAST_MERCHANT_KEY, PAYFAST_MERCHANT_ID=PAYFAST_MERCHANT_ID)
    def test_can_get_merchant_key(self):
        # Return the merchant key from the settings module
        self.assertEqual(get_config().get_merchant_key(), PAYFAST_MERCHANT_KEY,
                         "Unable to retrieve merchant key from settings")

        # Remove PAYFAST_MERCHANT_KEY and PAYFAST_MERCHANT_ID from settings
        del settings.PAYFAST_MERCHANT_KEY
        del settings.PAYFAST_MERCHANT_ID

        # Return the development key if PAYFAST_MERCHANT_KEY is not present in settings
        self.assertEqual(get_config().get_merchant_key(), Constants.MERCHANT_KEY_DEV,
                         "Cannot retrieve default development merchant key from Constants")

    @override_settings(PAYFAST_MERCHANT_KEY=PAYFAST_MERCHANT_KEY, PAYFAST_MERCHANT_ID=PAYFAST_MERCHANT_ID)
    def test_can_get_action_url(self):
        # Return live server url if merchant key and id are set
        self.assertEqual(get_config().get_action_url(), Constants.ACTION_URL_LIVE,
                         'Cannot get live server url when merchant key and id are set')

        # Remove PAYFAST_MERCHANT_KEY and PAYFAST_MERCHANT_ID from settings
        del settings.PAYFAST_MERCHANT_KEY
        del settings.PAYFAST_MERCHANT_ID

        # Return development server url if merchant key and id are NOT set
        self.assertEqual(get_config().get_action_url(), Constants.ACTION_URL_DEV,
                         "Cannot get development server url when merchant key and id are NOT set")

    @override_settings(PAYFAST_PASSPHRASE=PAYFAST_PASSPHRASE)
    def test_can_get_passphrase(self):
        # Test if passphrase can be retrieved from settings
        self.assertEqual(get_config().get_passphrase(), PAYFAST_PASSPHRASE, "Unable to get passphrase from settings")
        # Unset passphrase
        del settings.PAYFAST_PASSPHRASE
        # Test if passphrase is None when not set in settings
        self.assertIsNone(get_config().get_passphrase(), "Passphrase does not default to none if")

    @override_settings(PAYFAST_IP_ADDRESS_HTTP_HEADER=PAYFAST_IP_ADDRESS_HTTP_HEADER)
    def test_can_get_ip_address_header(self):
        # Test if header can be retrieved from settings
        self.assertEqual(get_config().get_ip_address_header(), PAYFAST_IP_ADDRESS_HTTP_HEADER,
                         "Unable to get http header from settings")

        # Remove https header from settings
        del settings.PAYFAST_IP_ADDRESS_HTTP_HEADER

        # Test if header is 'REMOTE_ADDR' when http header is not set
        self.assertEqual(get_config().get_ip_address_header(),
                         'REMOTE_ADDR', "Unable to get default http header REMOTE_ADDR if not in settings")
