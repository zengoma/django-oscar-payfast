from oscar.core.loading import get_class


from .config import get_config

Constants = get_class('payfast.gateway', 'Constants')
Facade = get_class('payfast.facade', 'Facade')
MissingFieldException = get_class('payfast.gateway', 'MissingFieldException')


class Interface:
    """Django Oscar entry point to handle Payfast gateway.

    The ``Interface`` exposes an interface that can be used in any Django Oscar
    application. It aims to hide the inner complexity of payment form
    management and payment notification processing.

    The key methods are:

    * :meth:`get_form_action` and `get_form_fields` to build the Payfast gateway
      request submission form,
    * :meth:`handle_payment_return` to handle customer coming back from the
      Payfast gateway after a payment (successful or not)
    * :meth:`assess_notification_relevance`,
      :meth:`handle_payment_notification` and
      :meth:`build_notification_response` to handle Payfast Payment Notification.

    """
    def __init__(self):
        self.config = get_config()

    def get_form_action(self):
        """ Return the URL where the payment form should be submitted. """
        return self.config.get_action_url()

    @staticmethod
    def get_form_fields(order_data):
        """
        Return the payment form fields as a list of dicts.
        Expects a large-ish order_data dictionary with details of the order.
        """
        return Facade().build_payment_form_fields(order_data)

    @staticmethod
    def handle_notification_request(request):
        """
        Django oscar interface object for handling the payfast notification request
        :param request: The request object from payfast
        :return: object: Returns Facade.handle_notification object
        """
        return Facade().handle_notification_request(request)
