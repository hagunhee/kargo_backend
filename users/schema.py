import strawberry
import typing
from . import types
from . import queries


@strawberry.type
class Query:
    all_users: typing.List[types.UserType] = strawberry.field(
        resolver=queries.get_all_users,
    )
    all_influencers: typing.List[types.InfluencerType] = strawberry.field(
        resolver=queries.get_all_influencers,
    )
