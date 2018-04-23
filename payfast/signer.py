# -*- coding: utf-8 -*-
"""Signers are helpers to sign and verify Payfast requests & responses.

There is currently one type of signature:

* MD5

This class could be modified in future should payfast implement other signature methods eg SHA.

.. note::

    **About the signature:**

    The data passed in the form fields, is parsed into a url encoded querystring,
    referred to as the “signing string”. The signature is then generated
    and optionally "salted" using the PAYFAST_PASSPHRASE setting.

    The signature is passed along with the form data and once Payfast receives it
    they use the key to verify that the data has not been tampered with in
    transit.

    The signing string should be packed into a binary format containing hex
    characters, and then encoded for transmission.

"""
import hashlib
try:
    # Python > 3
    import urllib.parse as parse
except ImportError:
    # Python < 3
    import urllib as parse


from payfast.constants import Constants
from .config import get_config


class AbstractSigner:
    """Abstract base class that define the common interface.

    A signer must expose three methods:

    * :meth:`sign`: take form fields and return a dict of signature fields.
    * :meth:`verify`: take a dict of fields and make sure there have an
        appropriate signature field.
    * :meth:`genetrate_hash`: take a signature string and compute its hash value.

    These methods are not implementd by the :class:`AbstractSigner`, therefore
    subclasses **must** implement them.
    """

    def sign(self, fields):
        """Sign the given form ``fields`` and return the signature fields.

        :param dict fields: The form fields used to perform a payment request
        :return: A dict of signature fields
        :rtype: ``dict``

        A payment request form must contains specific signature fields,
        depending on the selected sign method.
        """
        raise NotImplementedError

    def verify(self, fields):
        """Verify ``fields`` contains the appropriate signatures.

        :param dict fields: A dict of fields, given by a payment return
            response or by a payment notification.
        :return: ``True`` the ``fields`` contain valid signatures
        :rtype: ``boolean``
        """
        raise NotImplementedError

    def genetrate_hash(self, signature_string):
        """Return a hash for the given ``signature_string``.

        :param str signature_string: A ``signature_string`` used to generate a signature.
        :return: str siganture: A hashed version of the ``signature_string`` using the
            :attr:`PAYFAST_PASSPHRASE` if it has been assigned in the settings folder.

        The md5 hashing algorithm is used to sign the ``signature_string`` string. This method is not supposed to know how
        the ``signature_string`` is built. A secret 'PAYFAST_PASSPHRASE' can be used to salt the hash and compensate for
        some of the known md5 vulnerabilities.
        """
        raise NotImplementedError


class MD5Signer(AbstractSigner):
    """Implement a MD5 signature.

    .. seealso::

        The Payfast documentation about `MD5 siganture generation`__ for an explanation
        on generating the signature.

        .. __: https://developers.payfast.co.za/documentation/#checkout-page


    """
    REQUEST_HASH_KEYS = (
        Constants.MERCHANT_ID,
        Constants.MERCHANT_KEY,
        Constants.RETURN_URL,
        Constants.CANCEL_URL,
        Constants.NOTIFY_URL,
        Constants.NAME_FIRST,
        Constants.NAME_LAST,
        Constants.EMAIL_ADDRESS,
        Constants.CELL_NUMBER,
        Constants.M_PAYMENT_ID,
        Constants.AMOUNT,
        Constants.ITEM_NAME,
        Constants.ITEM_DESCRIPTION,
        Constants.EMAIL_CONFIRMATION,
        Constants.CONFIRMATION_ADDRESS
    )
    """An ordered tuple of possible request keys
    This is used to build or verify the payfast signature before the user is directed to the payfast gateway.
    Note that the order of the fields matter to generate the hash with the MD5 algorithm.
    """

    RESPONSE_HASH_KEYS = (
        Constants.M_PAYMENT_ID,
        Constants.PF_PAYMENT_ID,
        Constants.PAYMENT_STATUS,
        Constants.ITEM_NAME,
        Constants.ITEM_DESCRIPTION,
        Constants.AMOUNT_GROSS,
        Constants.AMOUNT_FEE,
        Constants.AMOUNT_NET,
        Constants.NAME_FIRST,
        Constants.NAME_LAST,
        Constants.EMAIL_ADDRESS,
        Constants.MERCHANT_ID
    )
    """An ordered tuple of possible response/notification keys

    This is used to build or verify the payfast signature that is by payfast to the ITN endpoint. Note that the order of
    the fields matter to generate the hash with the MD5 algorithm.
    """

    def sign(self, fields):
        """Sign the given form ``fields`` and return the signature field.

        :param dict fields: A dictionary of request fields
        :returns str signature: The signature to be send with the payfast request

        .. seealso::

            The :meth:`AbstractSigner.sign` method for usage.

        """
        signature_list = [(key, fields[key]) for key in self.REQUEST_HASH_KEYS if fields.get(key, None)]
        signature_string = parse.urlencode(signature_list)
        signature = self.generate_hash(signature_string)

        return signature

    def verify(self, fields):
        """Verify ``fields`` contains the appropriate signature response from payfast.

        :param dict fields: A dictionary of request fields
        :returns bool: returns True only if the signature from the payfast server is valid, else returns False

        .. seealso::

            The :meth:`AbstractSigner.verify` method for usage.

        """
        response_signature = fields.pop('signature', None)
        signature_list = [(key, fields[key]) for key in self.RESPONSE_HASH_KEYS if fields.get(key, None)]
        signature_string = parse.urlencode(signature_list)
        signature = self.generate_hash(signature_string)

        return signature == response_signature

    def generate_hash(self, signature_string):
        """Generate the hash using the ``hashlib.md5`` algorithm.

        .. seealso::

            The :meth:`AbstractSigner.genetrate_hash` method for usage.

        """
        if get_config().get_passphrase():
            signature_string += '&passphrase=' + parse.quote(get_config().get_passphrase())

        return hashlib.md5(signature_string.encode()).hexdigest()
