"""
App Coloring configuration.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import typing as t

import strawberry as gql

import fiftyone.core.fields as fof
from fiftyone.core.odm import EmbeddedDocument
import fiftyone.core.utils as fou


class LabelSetting(EmbeddedDocument):
    """TODO"""

    name = fof.StringField()
    color = fof.StringField()


class CustomizedColor(EmbeddedDocument):
    """TODO"""

    meta = {"abstract": True, "allow_inheritance": True}

    field = fof.StringField(required=True)
    use_field_color = fof.BooleanField()
    field_color = fof.StringField()
    attribute_for_color = fof.StringField()
    use_opacity = fof.BooleanField()
    attribute_for_opacity = fof.StringField()
    use_label_colors = fof.BooleanField()
    label_colors = fof.ListField(
        fof.EmbeddedDocumentField(LabelSetting), default=[]
    )
