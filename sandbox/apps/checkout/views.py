from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from oscar.apps.checkout import views
from oscar.apps.payment import forms, models


class PaymentDetailsView(views.PaymentDetailsView):
    """
    An example view that shows how to integrate BOTH PayFast Express
    (see get_context_data method)and Payppal Flow (the other methods).
    Naturally, you will only want to use one of the two.
    """

    def get_context_data(self, **kwargs):
        """
        Add data for PayFast Express flow.
        """
        # Override method so the bankcard and billing address forms can be
        # added to the context.

        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        # ctx['bankcard_form'] = kwargs.get(
        #     'bankcard_form', forms.BankcardForm())
        ctx['billing_address_form'] = kwargs.get(
            'billing_address_form', forms.BillingAddressForm())
        #
        return ctx

    def post(self, request, *args, **kwargs):
        # Override so we can validate the bankcard/billingaddress submission.
        # If it is valid, we render the preview screen with the forms hidden
        # within it.  When the preview is submitted, we pick up the 'action'
        # parameters and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            submission = self.build_submission()
            self.submit(**submission)
            return redirect(reverse('payfast-redirect'))

        # bankcard_form = forms.BankcardForm(request.POST)
        billing_address_form = forms.BillingAddressForm(request.POST)
        #
        if not billing_address_form.is_valid():
            # Form validation failed, render page again with errors
            self.preview = False
            ctx = self.get_context_data(billing_address_form=billing_address_form)
            return self.render_to_response(ctx)

        # Render billing address details hidden
        return self.render_preview(request, billing_address_form=billing_address_form)

    def handle_payment(self, order_number, total, **kwargs):
        """
        Make submission to PayFast
        """
