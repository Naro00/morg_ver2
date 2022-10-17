import strawberry
import typing
from . import types
from . import queries


@strawberry.type
class Query:
    all_clubs: typing.List[types.ClubType] = strawberry.field(
        resolver=queries.get_all_clubs,
    )
