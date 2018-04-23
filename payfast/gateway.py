import logging
from .constants import Constants
from .exceptions import (
    InvalidTransactionException,
    MissingFieldException,
    MissingParameterException,
    UnexpectedFieldException,
)

logger = logging.getLogger('payfast')


class Gateway:

    MANDATORY_SETTINGS = (
        Constants.MERCHANT_ID,
        Constants.MERCHANT_KEY,
        Constants.SIGNER,
        Constants.ACTION_URL,
    )

    def __init__(self, settings=None):
        """
        Initialize an Payfast gateway.
        """
        if settings is None:
            settings = {}

        if any(key not in settings for key in self.MANDATORY_SETTINGS):
            raise MissingParameterException(
                "You need to specify the following parameters to initialize "
                "the Payfast gateway: %s. "
                "Please check your configuration."
                % ', '.join(self.MANDATORY_SETTINGS))

        self.merchant_id = settings.get(Constants.MERCHANT_ID)
        self.merchant_key = settings.get(Constants.MERCHANT_KEY)
        self.signer = settings.get(Constants.SIGNER)
        self.action_url = settings.get(Constants.ACTION_URL)
        self.host_ip = settings.get(Constants.HOST_IP)

    @staticmethod
    def _build_form_fields(payfast_request):
        """
        Return the hidden fields of an HTML form allowing to perform this request.
        """
        return payfast_request.build_form_fields()

    def build_payment_form_fields(self, params):
        params.update({
            Constants.MERCHANT_ID: self.merchant_id,
            Constants.MERCHANT_KEY: self.merchant_key,
        })
        return self._build_form_fields(PaymentFormRequest(self, params))

    @staticmethod
    def _handle_notification(payfast_request):

        return payfast_request.process()

    def handle_notification(self, ip_address, params):

        return self._handle_notification(PaymentNotification(self, ip_address, params))


class BaseInteraction:
    REQUIRED_FIELDS = ()
    OPTIONAL_FIELDS = ()

    def validate(self):
        self.check_fields()

    def check_fields(self):
        """
        Validate required and optional fields for both
        requests and responses.
        """
        params = self.params

        # Check that all mandatory fields are present.
        for field_name in self.REQUIRED_FIELDS:
            if field_name not in params:
                raise MissingFieldException(
                    "The required field %s is missing" % field_name
                )

        # Check that no unexpected field is present.
        expected_fields = self.REQUIRED_FIELDS + self.OPTIONAL_FIELDS
        for field_name in params.keys():
            if field_name not in expected_fields:
                raise UnexpectedFieldException(
                    "Unexpected field %s" % field_name
                )


class PaymentFormRequest(BaseInteraction):
    REQUIRED_FIELDS = (
        Constants.MERCHANT_KEY,
        Constants.MERCHANT_ID,
        Constants.AMOUNT,
        Constants.ITEM_NAME
    )
    OPTIONAL_FIELDS = (
        Constants.RETURN_URL,
        Constants.NOTIFY_URL,
        Constants.CANCEL_URL,
        Constants.NAME_FIRST,
        Constants.NAME_LAST,
        Constants.EMAIL_ADDRESS,
        Constants.CELL_NUMBER,
        Constants.M_PAYMENT_ID,
        Constants.ITEM_DESCRIPTION,
        Constants.EMAIL_CONFIRMATION,
        Constants.EMAIL_ADDRESS
    )

    def __init__(self, client, params=None):
        self.client = client
        self.params = params or {}
        self.validate()

        # Generate MD5 signature.
        self.params.update({Constants.SIGNATURE: self.client.signer.sign(self.params)})

    def build_form_fields(self):
        return [{'type': 'hidden', 'name': name, 'value': value}
                for name, value in self.params.items()]


class PaymentNotification(BaseInteraction):
    """Process payment notifications (HTTPS ITN POST from Payfast to our servers).

    Payment notifications can have multiple fields. They fall into four
    categories:

    - required: Must be included.
    - optional: May be included.
    """

    REQUIRED_FIELDS = (
        Constants.PF_PAYMENT_ID,
        Constants.PAYMENT_STATUS,
        Constants.ITEM_NAME,
        Constants.AMOUNT_GROSS,
        Constants.AMOUNT_FEE,
        Constants.AMOUNT_NET,
        Constants.MERCHANT_ID
    )

    OPTIONAL_FIELDS = (
        Constants.M_PAYMENT_ID,
        Constants.ITEM_DESCRIPTION,
        Constants.NAME_FIRST,
        Constants.NAME_LAST,
        Constants.EMAIL_ADDRESS,
        Constants.SIGNATURE
    )

    def __init__(self, client, host_ip=None, params=None):
        self.client = client
        self.params = params or {}
        self.host_ip = host_ip
        self.validate()

    def validate(self):
        """
        Validates the ITN response from payfast see:
        :raises: InvalidTransactionException
        :return: None
        """
        super(PaymentNotification, self).validate()

        # Check that the transaction has not been tampered with. (Check 1)
        if not self.client.signer.verify(self.params):
            raise InvalidTransactionException("The transaction may have been tampered with. This could indicate fraud.")

        # Check that request originates from payfast servers (Check 2)
        host = self.host_ip
        if host not in Constants.VALID_PAYFAST_HOSTS:
            raise InvalidTransactionException("The transaction request originates from a server other than payfast")

    def process(self):
        payment_result = self.params.get(Constants.PAYMENT_STATUS, None)
        accepted = payment_result == Constants.PAYMENT_RESULT_COMPLETE
        status = payment_result

        return accepted, status, self.params
