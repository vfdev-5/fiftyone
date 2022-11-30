"""
FiftyOne GraphQL Query

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import strawberry as gql

from .dataset import DatasetMixin


@gql.type
class Query(DatasetMixin):
    pass
