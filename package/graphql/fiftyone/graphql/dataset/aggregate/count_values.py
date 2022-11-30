"""
FiftyOne GraphQL CountValues aggregation

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import typing as t

import strawberry as gql

T = t.TypeVar("T")


@gql.type
class ValueCount(t.Generic[T]):
    key: t.Union[T, None]
    value: int


@gql.type
class CountValuesResponse(t.Generic[T]):
    values: t.List[ValueCount[T]]


@gql.type
class BoolCountValuesResponse(CountValuesResponse[bool]):
    values: t.List[ValueCount[bool]]


@gql.type
class IntCountValuesResponse(CountValuesResponse[int]):
    values: t.List[ValueCount[int]]


@gql.type
class StrCountValuesResponse(CountValuesResponse[str]):
    values: t.List[ValueCount[str]]


CountValuesResponses = gql.union(
    "CountValuesResponses",
    (BoolCountValuesResponse, IntCountValuesResponse, StrCountValuesResponse),
)


@gql.input
class CountValues:
    field: str
