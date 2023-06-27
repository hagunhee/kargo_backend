import strawberry
import typing
from users import schema as users_schema
from baskets import schema as baskets_schema


@strawberry.type
class Query(users_schema.Query, baskets_schema.Query):
    # urls.py와 같이 movies field와 resolver를 연결시켜주는거지.
    pass


@strawberry.type
class Mutation:
    pass


schema = strawberry.Schema(
    query=Query,
    # mutation=Mutation
)
