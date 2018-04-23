from django.test import TestCase, RequestFactory

# fixtures
PAYMENT_REQUEST_FORM = {

}


class FacadeTestCase(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def can_build_payment_request_form(self):
        pass
