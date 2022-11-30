"""
FiftyOne GraphQL Aggregate

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import typing as t

import strawberry as gql

from .count import Count, CountResponse
from .count_values import (
    CountValues,
    BoolCountValuesResponse,
    IntCountValuesResponse,
    StrCountValuesResponse,
)
from .distinct import (
    Distinct,
    BoolDistinctResponse,
    IntDistinctResponse,
    StrDistinctResponse,
)
from .histogram_values import (
    HistogramValues,
    DatetimeHistogramValuesResponse,
    FloatHistogramValuesResponse,
    IntHistogramValuesResponse,
)


@gql.input
class Aggregations:
    count: t.Optional[Count] = None
    count_values: t.Optional[CountValues] = None
    distinct: t.Optional[Distinct] = None
    histogram_values: t.Optional[HistogramValues] = None


AggregationsResponse = t.List[
    gql.union(
        "AggregationResponse",
        (
            CountResponse,
            BoolCountValuesResponse,
            IntCountValuesResponse,
            StrCountValuesResponse,
            BoolDistinctResponse,
            IntDistinctResponse,
            StrDistinctResponse,
            DatetimeHistogramValuesResponse,
            FloatHistogramValuesResponse,
            IntHistogramValuesResponse,
        ),
    )
]


def aggregate(
    aggregations: t.List[Aggregations],
    view: t.Optional[t.List[gql.scalars.JSON]] = None,
) -> AggregationsResponse:
    raise NotImplementedError("resolver must be implemented")
