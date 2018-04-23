from oscar.app import Shop

from apps.checkout.app import application as checkout_app


class PayFastShop(Shop):
    checkout_app = checkout_app


application = PayFastShop()
