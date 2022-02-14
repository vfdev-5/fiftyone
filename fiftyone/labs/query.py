"""
FiftyOne Teams queries.

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from datetime import date, datetime
from enum import Enum
import typing as t
from xmlrpc.client import boolean

from bson import ObjectId
from dacite import Config, from_dict
import motor
import strawberry as gql

import fiftyone as fo

from .dataloader import get_dataloader_resolver
from .mixins import HasCollection
from .paginator import Connection, get_paginator_resolver
from .utils import Info


ID = gql.scalar(
    t.NewType("ID", str),
    serialize=lambda v: str(v),
    parse_value=lambda v: ObjectId(v),
)


@gql.enum
class MediaType(Enum):
    image = "image"
    video = "video"


@gql.type
class Target:
    target: int
    value: str


@gql.type
class NamedTargets:
    name: str
    targets: t.List[Target]


@gql.type
class SampleField:
    ftype: str
    path: str
    subfield: t.Optional[str]
    embedded_doc_type: t.Optional[str]
    db_field: t.Optional[str]


@gql.interface
class RunConfig:
    cls: str


@gql.interface
class Run:
    key: str
    version: str
    timestamp: datetime
    config: RunConfig
    view_stages: t.List[str]


@gql.type
class BrainRunConfig(RunConfig):
    embeddings_field: t.Optional[str]
    method: str
    patches_field: t.Optional[str]


@gql.type
class BrainRun(Run):
    config: BrainRunConfig


@gql.type
class EvaluationRunConfig(RunConfig):
    classwise: boolean
    error_level: int
    gt_field: str
    pred_field: str
    method: str


@gql.type
class EvaluationRun(Run):
    config: EvaluationRunConfig


@gql.type
class SidebarGroup:
    name: str
    paths: t.List[str]


@gql.type
class Dataset(HasCollection):
    id: gql.ID
    name: str
    created_at: date
    last_loaded_at: datetime
    persistent: bool
    media_type: MediaType
    mask_targets: t.List[NamedTargets]
    default_mask_targets: t.Optional[t.List[Target]]
    sample_fields: t.List[SampleField]
    frame_fields: t.List[SampleField]
    brain_methods: t.List[BrainRun]
    evaluations: t.List[EvaluationRun]
    app_sidebar_groups: t.Optional[t.List[SidebarGroup]]
    version: str

    @staticmethod
    def get_collection_name() -> str:
        return "datasets"

    @staticmethod
    def modifier(doc: dict) -> dict:
        doc["id"] = doc.pop("_id")
        doc["sample_fields"] = _flatten_fields([], doc["sample_fields"])
        doc["frame_fields"] = _flatten_fields([], doc["frame_fields"])
        return doc

    @classmethod
    async def resolver(cls, name: str, info: Info) -> "Dataset":
        return await dataset_dataloader(name, info)


dataset_dataloader = get_dataloader_resolver(Dataset, "name")


@gql.type
class AppConfig:
    timezone: t.Optional[str]
    colorscale: str
    color_pool: t.List[str]
    grid_zoom: int
    loop_videos: bool
    notebook_height: int
    show_confidence: bool
    show_index: bool
    show_label: bool
    show_tooltip: bool
    use_frame_number: bool


@gql.type
class User(HasCollection):
    id: gql.ID
    datasets: Connection[Dataset] = gql.field(
        resolver=get_paginator_resolver(Dataset)
    )
    email: str
    family_name: str
    given_name: str

    @gql.field
    def colorscale(self) -> t.Optional[t.List[t.List[int]]]:
        if fo.app_config.colorscale:
            return fo.app_config.get_colormap()

        return None

    @gql.field
    def config(self) -> AppConfig:
        d = fo.app_config.serialize()
        d["timezone"] = fo.config.timezone
        return from_dict(AppConfig, d, config=Config(check_types=False))

    @staticmethod
    def get_collection_name():
        return "users"


@gql.type
class Query:
    users: Connection[User] = gql.field(resolver=get_paginator_resolver(User))

    dataset: Dataset = gql.field(resolver=Dataset.resolver)
    datasets: Connection[Dataset] = gql.field(
        resolver=get_paginator_resolver(Dataset)
    )

    @gql.field
    async def viewer(self, info: Info) -> User:
        db = info.context.db
        users: motor.MotorCollection = db.users
        user = await users.find_one({"sub": info.context.sub})
        user["id"] = user.pop("_id")
        return from_dict(User, user, config=Config(check_types=False))


def _flatten_fields(path, fields):
    result = []
    for field in fields:
        key = field.pop("name")
        field_path = path + [key]
        field["path"] = ".".join(field_path)
        result.append(field)

        fields = field.pop("fields", None)
        if fields:
            result = result + _flatten_fields(field_path, fields)

    return result
