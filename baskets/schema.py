import strawberry
import typing
from . import types
from . import queries


@strawberry.type
class Query:
    get_basket: typing.Optional[types.BasketType] = strawberry.field(
        resolver=queries.get_basket,
    )
