"""
FiftyOne GraphQL HistogramValues aggregation

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from datetime import datetime
import typing as t

import strawberry as gql

T = t.TypeVar("T")


@gql.type
class HistogramValuesResponse(t.Generic[T]):
    counts: t.List[int]
    edges: t.List[T]
    other: int


@gql.type
class DatetimeHistogramValuesResponse(HistogramValuesResponse[datetime]):
    edges: t.List[datetime]


@gql.type
class FloatHistogramValuesResponse(HistogramValuesResponse[float]):
    edges: t.List[float]


@gql.type
class IntHistogramValuesResponse(HistogramValuesResponse[int]):
    edges: t.List[float]


@gql.input
class HistogramValues:
    field: str


HistogramValuesResponses = gql.union(
    "HistogramValuesResponses",
    (
        DatetimeHistogramValuesResponse,
        FloatHistogramValuesResponse,
        IntHistogramValuesResponse,
    ),
)
