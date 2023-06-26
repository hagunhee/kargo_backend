import strawberry
import typing
from . import types
from . import queries


@strawberry.type
class Query:
    get_cart: typing.Optional[types.CartType] = strawberry.field(
        resolver=queries.get_cart,
    )
