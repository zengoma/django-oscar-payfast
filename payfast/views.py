from oscar.core.loading import get_class, get_model
from django.shortcuts import get_object_or_404, render
from django.shortcuts import reverse
from django.http import HttpResponse

Interface = get_class('payfast.interface', 'Interface')
Order = get_model('order', 'Order')


def redirect_view(request):
    interface = Interface()
    order = get_object_or_404(Order, id=request.session.get('checkout_order_id', 0))
    form_fields = interface.get_form_fields(order_data={
        'm_payment_id': order.number,
        'amount': order.total_incl_tax,
        'item_name': 'Payfast order: {}'.format(order.number),
        'return_url': request.build_absolute_uri(reverse('checkout:thank-you')),
        'notify_url': request.build_absolute_uri(reverse('payfast-notify'))
    })

    form_action_url = interface.get_form_action()

    return render(request, "payfast/redirect.html", {
        'form_fields': form_fields,
        'form_action_url': form_action_url
    })


def notify_view(request):

    interface = Interface()

    try:
        interface.handle_notification_request(request)
    except:  # noqa
        pass
    finally:
        # Always return a 200 OK as per Payfast documentation
        return HttpResponse(status=200)


def cancel_view(request):
    return HttpResponse(status=200)
