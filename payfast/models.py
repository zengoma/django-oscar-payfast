# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils import timezone
from oscar.core.loading import get_class

Constants = get_class('payfast.gateway', 'Constants')
# Order = get_class('oscar.apps.order.models', 'Order')


class PayfastTransaction(models.Model):

    # we create an order before redirecting to payfast. The transaction updated
    order_number = models.CharField(max_length=20)

    payfast_reference = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    amount = models.DecimalField(decimal_places=2, max_digits=12)
    amount_net = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    amount_fee = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    currency = models.CharField(max_length=3, default=settings.OSCAR_DEFAULT_CURRENCY)

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):

        # Payfast transaction description
        return u'Payfast %s txn %s | amount: %s | status: %s' % (
            self.method.upper(),
            self.reference,
            self.amount,
            self.status)

    def __unicode__(self):
        return str(self)
