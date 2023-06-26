import strawberry
import typing
from users import schema as users_schema
from carts import schema as carts_schema


@strawberry.type
class Query(users_schema.Query, carts_schema.Query):
    # urls.py와 같이 movies field와 resolver를 연결시켜주는거지.
    pass


@strawberry.type
class Mutation:
    pass


schema = strawberry.Schema(
    query=Query,
    # mutation=Mutation
)
