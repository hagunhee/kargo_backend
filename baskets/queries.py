from . import models


def get_basket_manager(pk: int):
    try:
        return models.Basket.objects.get(pk=pk)
    except models.Basket.DoesNotExist:
        return models.Basket.objects.create(pk=pk)


def get_basket_item(pk: int):
    try:
        return models.BasketItem.objects.get(pk=pk)
    except models.BasketItem.DoesNotExist:
        return None


def get_basket(pk: int):
    basket = get_basket_manager(pk=pk)
    return basket
