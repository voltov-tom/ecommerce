from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from order.views import render_to_pdf


def decrement_product_quantity(order):
    for item in order.items.all():
        product = item.product
        product.num_available -= item.quantity
        product.save()


def send_order_confirmation(order):
    subject = 'Order confirmation'
    from_email = 'noreply@online_store.com'
    to = ['mail@online_store.com', order.email]
    text_content = 'Your order is successful!'
    html_content = render_to_string('order_confirmation.html', {'order': order})

    pdf = render_to_pdf('order_pdf.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    if pdf:
        name = f'order_{order.id}.pdf'
        msg.attach(name, pdf, 'application/pdf')

    msg.send()
