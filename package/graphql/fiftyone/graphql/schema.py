"""
FiftyOne GraphQL Schema

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from datetime import date, datetime

import strawberry as gql

from .extensions import EndSession
from .mutation import Mutation
from .query import Query
from .scalars import Date, DateTime

schema = gql.Schema(
    # mutation=Mutation,
    query=Query,
    extensions=[EndSession],
    scalar_overrides={
        date: Date,
        datetime: DateTime,
    },
)
