from . import models


def get_cart_manager(pk: int):
    try:
        return models.Cart.objects.get(pk=pk)
    except models.Cart.DoesNotExist:
        return models.Cart.objects.create(pk=pk)


def get_cart_item(pk: int):
    try:
        return models.CartItem.objects.get(pk=pk)
    except models.CartItem.DoesNotExist:
        return None


def get_cart(pk: int):
    cart = get_cart_manager(pk=pk)
    return cart
