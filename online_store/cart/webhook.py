import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives

from order.models import Order
from order.views import render_to_pdf

from store.utilites import decrement_product_quantity


@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_HIDDEN_KEY

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object

        order = Order.objects.get(payment_intent=payment_intent.id)
        order.paid = True
        order.save()

        decrement_product_quantity(order)

        subject = 'Order confirmation'
        from_email = 'noreply@online_store.com'
        to = ['mail@online_store.com', order.email]
        text_content = f'Your order №{order.id} is successful!'
        html_content = render_to_string('order_confirmation.html', {'order': order})

        pdf = render_to_pdf('order_pdf.html', {'order': order})

        msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to)
        msg.attach_alternative(html_content, 'text/html')

        if pdf:
            name = f'order_{order.id}.pdf'
            msg.attach(name, pdf, 'application/pdf')

        msg.send()

        html = render_to_string('order_confirmation.html', {'order': order})
        send_mail(
            'Order confirmation',
            f'Your order №{order.id} is successful!',
            'noreply@online_store.com',
            ['mail@online_store.com', order.email],
            html_message=html
        )

    else:
        print(f'Unhandled event type: {event.type}')

    return HttpResponse(status=200)
