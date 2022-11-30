"""
FiftyOne GraphQL Count aggregation

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import typing as t

import strawberry as gql


@gql.type
class CountResponse:
    count: int


@gql.input
class Count:
    field: t.Optional[str] = None
