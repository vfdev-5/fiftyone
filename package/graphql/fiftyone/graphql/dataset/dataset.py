"""
FiftyOne GraphQL Dataset

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import typing as t
import strawberry as gql

from .aggregate import AggregateMixin


@gql.type
class Dataset(AggregateMixin):
    pass


@gql.type
class DatasetMixin:
    @gql.field
    def dataset(self, name: str) -> Dataset:
        raise NotImplementedError("resolver must be implemented")
