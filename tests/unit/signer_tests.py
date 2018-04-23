from django.test.utils import override_settings
from django.conf import settings
from payfast.signer import MD5Signer
from unittest import TestCase


# Fixtures
REQUEST_DICTIONARY = {
    'merchant_id': 10000100,
    'merchant_key': '46f0cd694581a',
    'return_url': 'http://example.com/return',
    'cancel_url': 'http://example.com/cancel',
    'notify_url': 'http://example.com/notify',
    'name_first': 'John',
    'name_last': 'Doe',
    'email_address': 'john@example.com',
    'cell_number': 729099009,
    'm_payment_id': '55',
    'amount': 100.00,
    'item_name': 'Oscar Invoice 55',
    'item_description': 'An invoice from Django oscar',
    'email_confirmation': 1,
    'confirmation_address': 'admin@example.com'
}

RESPONSE_DICTIONARY = {
    'm_payment_id': '55',
    'pf_payment_id': 123456789,
    'payment_status': 'COMPLETE',
    'item_name': 'Oscar Invoice 55',
    'item_description': 'An invoice from Django oscar',
    'amount_gross': 100.00,
    'amount_fee': 5.00,
    'amount_net': 95.00,
    'name_first': 'John',
    'name_last': 'Doe',
    'email_address': 'john@example.com',
    'merchant_id': 10000100
}

PASSPHRASE_SALT = 'MYSECRETPASSPHRASE'
UNSALTED_REQUEST_SIGNATURE = '34f4c69658c18d7a21327118f7b49ddf'
SALTED_REQUEST_SIGNATURE = 'add40aee61b0ac8ca36c574f8680d9db'
UNSALTED_RESPONSE_SIGNATURE = 'f1d22cff421688a6fe3bb97f2fef4a66'
SALTED_RESPONSE_SIGNATURE = '44026fc49f1aeaa0eb1a25cbd64e484c'
SAMPLE_HASH_SALTED = ''  # Generated using "the signature string"
SAMPLE_HASH_UNSALTED = ''  # Generated using "the signature string"


class MD5SignerTestCase(TestCase):

    def setUp(self):
        self.md5signer = MD5Signer()

    @override_settings(PAYFAST_PASSPHRASE=PASSPHRASE_SALT)
    def test_can_generate_a_hash(self):
        generated_hash = self.md5signer.generate_hash('the signature string')

        self.assertEqual(generated_hash, SAMPLE_HASH_SALTED)
        # Remove PAYFAST_PASSPHRASE from settings
        del settings.PAYFAST_PASSPHRASE

        self.assertEqual(generated_hash, SAMPLE_HASH_UNSALTED)

    @override_settings(PAYFAST_PASSPHRASE=PASSPHRASE_SALT)
    def test_sign_can_return_a_valid_signature(self):

        # Test that signer returns the correct salted signature if PAYFAST_PASSPHRASE is set
        signature = self.md5signer.sign(REQUEST_DICTIONARY)
        self.assertEqual(signature, SALTED_REQUEST_SIGNATURE, "the sign method returned a malformed signature (salted)")

        # Remove PAYFAST_PASSPHRASE from settings
        del settings.PAYFAST_PASSPHRASE

        # Test that signer returns the correct unsalted signature if NO PAYFAST_PASSPHRASE is set
        signature = self.md5signer.sign(REQUEST_DICTIONARY)
        self.assertEqual(signature, UNSALTED_REQUEST_SIGNATURE,
                         "the sign method returned a malformed signature (unsalted)")

    @override_settings(PAYFAST_PASSPHRASE=PASSPHRASE_SALT)
    def test_can_verify_a_response_signature(self):

        # Test that verify method will return true for a valid salted signature
        RESPONSE_DICTIONARY.update({'signature': SALTED_RESPONSE_SIGNATURE})
        self.assertTrue(self.md5signer.verify(RESPONSE_DICTIONARY),
                        "the verify method returned an unexpected False in response to a valid signature (salted)")

        # Remove PAYFAST_PASSPHRASE from settings
        del settings.PAYFAST_PASSPHRASE

        # Test that verify method will return true for a valid unsalted signature
        RESPONSE_DICTIONARY['signature'] = UNSALTED_RESPONSE_SIGNATURE
        self.assertTrue(self.md5signer.verify(RESPONSE_DICTIONARY),
                        "the verify method returned an unexpected False in response to a valid signature (unsalted)")

        # Test that verify method will return false for a malformed signature
        RESPONSE_DICTIONARY['item_description'] = 'Some kind of malicious tampering'
        self.assertFalse(self.md5signer.verify(RESPONSE_DICTIONARY),
                         "the verify method returned an unexpected True in response to an invalid signature")
