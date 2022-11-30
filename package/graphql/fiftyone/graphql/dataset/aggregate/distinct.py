"""
FiftyOne GraphQL Distinct aggregation

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import typing as t

import strawberry as gql

T = t.TypeVar("T")


@gql.type
class DistinctResponse(t.Generic[T]):
    values: t.List[T]


@gql.type
class BoolDistinctResponse(DistinctResponse[bool]):
    values: t.List[bool]


@gql.type
class IntDistinctResponse(DistinctResponse[int]):
    values: t.List[int]


@gql.type
class StrDistinctResponse(DistinctResponse[str]):
    values: t.List[str]


DistinctResponses = gql.union(
    "DistinctResponses",
    (BoolDistinctResponse, IntDistinctResponse, StrDistinctResponse),
)


@gql.input
class Distinct:
    field: str
