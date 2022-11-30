"""
FiftyOne GraphQL Dataset

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import strawberry as gql

from .aggregate import aggregate, AggregationsResponse


@gql.type
class Dataset:
    gql.field(resolver=aggregate)
    aggregate: AggregationsResponse
