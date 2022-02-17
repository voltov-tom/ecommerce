import json


def product_images_serializer(product):
    product_images = []

    image = product.image.url
    thumbnail = product.thumbnail.url
    data = dict(
        image=image,
        thumbnail=thumbnail
    )
    product_images.append(data)

    for image in product.images.all():
        img = image.image.url
        thumbnail = image.thumbnail.url
        data = dict(
            image=img,
            thumbnail=thumbnail
        )
        product_images.append(data)

    return json.dumps(product_images)
