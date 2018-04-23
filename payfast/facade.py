# -*- coding: utf-8 -*-
import logging
import iptools
from oscar.core.loading import get_class
from .signer import MD5Signer
from .config import get_config
from .models import PayfastTransaction

Constants = get_class('payfast.gateway', 'Constants')
Gateway = get_class('payfast.gateway', 'Gateway')


logger = logging.getLogger('payfast')


def get_gateway(config):
    """Instantiate a :class:`payfast.gateway.Gateway` from ``config``.

    :param config: Payfast Config object.
    :type config: :class:`~payfast.config.AbstractPayfastConfig`
    :return: An instance of ``Gateway`` configured properly.

    The ``Gateway`` is built using the given ``config`` and ``request`` to get
    specific values for ``identifier``, ``secret_key`` and ``action_url``.

    The configuration object requires the ``request`` in order to allow plugin
    user to define a per-request configuration, such as a different secret key
    based on the country or the language (or even the type of customer, its
    IP address, or other request specific parameter).
    """
    return Gateway({
        Constants.MERCHANT_ID: config.get_merchant_id(),
        Constants.MERCHANT_KEY: config.get_merchant_key(),
        Constants.ACTION_URL: config.get_action_url(),
        Constants.SIGNER: MD5Signer(),
    })


class Facade:
    """Facade used to expose the public behavior of the Payfast gateway.

    The ``Facade`` class exposes a set of public methods to be used by the
    plugin internally and by plugin users without having to deal with Payfast
    internal mecanism (such as how to sign a request form or how to read a
    payment response).

    The first entry point is the payment form:

    * :meth:`build_payment_form_fields` to handle payment data and generate
      the payment request form used to submit a payment request to Payfast gateway.

    Then payment processing entry points of the ``Facade`` are:

    * :meth:`handle_payment_return` to handle payment return data,
    * :meth:`handle_payment_notification` to handle payment standard
      notifications.

    These methods will build an appropriate Payfast Payment Response object and
    call the :meth:`process_payment_feedback` method to handle the payment
    feedback.
    """
    def __init__(self):
        self.config = get_config()

    @classmethod
    def _is_valid_ip_address(cls, s):
        """
        Make sure that a string is a valid representation of an IP address.
        Relies on the iptools package, even though Python 3.4 gave us the new
        shiny `ipaddress` module in the stdlib.
        """
        return iptools.ipv4.validate_ip(s) or iptools.ipv6.validate_ip(s)

    def _get_origin_ip_address(self, request):
        """
        Return the IP address where the payment originated from or None if
        we are unable to get it -- which *will* happen if we received a
        PaymentNotification rather than a PaymentRedirection, since the
        request, in that case, comes from the Payfast servers.

        When possible, we need to fetch the *real* origin IP address.
        According to the platform architecture, it may be transmitted to our
        application via vastly variable HTTP headers. The name of the relevant
        header is therefore configurable via the `payfast_IP_ADDRESS_HTTP_HEADER`
        Django setting. We fallback on the canonical `REMOTE_ADDR`, used for
        regular, unproxied requests.
        """
        ip_address_http_header = self.config.get_ip_address_header()

        try:
            ip_address = request.META[ip_address_http_header]
        except KeyError:
            return None

        if not self._is_valid_ip_address(ip_address):
            logger.warning("%s is not a valid IP address", ip_address)
            return None

        return ip_address

    def build_payment_form_fields(self, params):
        """
        Return a dict containing the name and value of all the hidden fields
        necessary to build the form that will be POSTed to Payfast.
        """
        return get_gateway(self.config).build_payment_form_fields(params)

    @staticmethod
    def _record_transaction(status, txn_details):
        """
        Record an PayfastTransaction to keep track of the current payment attempt.
        """
        order_number = txn_details['order_number']
        # Record payfast transactions.
        try:
            txn_log = PayfastTransaction.objects.create(
                amount=txn_details['amount'],
                method=txn_details.get('payment_method', None),
                reference=txn_details.get('payfast_reference', None),
                order_number=txn_details['order_number'],
                amount_net=txn_details.get('amount_net', None),
                amount_fee=txn_details.get('amount_fee', None),
                currency=txn_details.get('currency', None),
                status=status,
            )
        except Exception:  # noqa
            # Yes, this is generic, because basically, whatever happens, be it
            # a `KeyError` in `txn_details` or an exception when creating our
            # `PayfastTransaction`, we are going to do the same thing: log the
            # exception and carry on. This is not critical, and this should
            # not prevent the rest of the process.
            logger.exception("Unable to record transaction for order: %s", order_number)
            return

        return txn_log

    def handle_notification_request(self, request):
        host_ip = self._get_origin_ip_address(request)
        params = request.POST
        return get_gateway(self.config).handle_notification(ip_address=host_ip, host_ip=params)
