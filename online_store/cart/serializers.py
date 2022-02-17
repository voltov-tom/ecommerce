import json


def cart_serializer(cart):
    cart_data = []
    for item in cart:
        product = item['product']
        id = product.id
        title = product.title
        price = product.price
        quantity = item['quantity']
        total_price = item['total_price']
        thumbnail = product.thumbnail.url
        url = product.slug
        num_available = product.num_available
        data = dict(
            id=id,
            title=title,
            price=price,
            quantity=quantity,
            total_price=total_price,
            thrumbnail=thumbnail,
            url=url,
            num_available=num_available
        )
        cart_data.append(data)
    return json.dumps(cart_data)
