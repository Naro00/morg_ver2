import strawberry
from clubs import schema as clubs_schema


@strawberry.type
class Query(clubs_schema.Query):
    pass


@strawberry.type
class Mutation:
    pass


schema = strawberry.Schema(query=Query,)  # mutation=Mutation
