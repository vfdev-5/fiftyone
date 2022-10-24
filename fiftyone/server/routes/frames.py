"""
FiftyOne Server /frames route

| Copyright 2017-2022, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from bson import ObjectId
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request

from fiftyone.core.expressions import ViewField as F
import fiftyone.core.json as foj
import fiftyone.core.odm as foo

from fiftyone.server.decorators import route
import fiftyone.server.view as fosv


class Frames(HTTPEndpoint):
    @route
    async def post(self, request: Request, data: dict):
        start_frame = int(data.get("frameNumber", 1))
        frame_count = int(data.get("frameCount", 1))
        num_frames = int(data.get("numFrames"))
        extended = data.get("extended", None)
        dataset = data.get("dataset")
        stages = data.get("view")
        sample_id = data.get("sampleId")

        end_frame = min(num_frames + start_frame, frame_count)

        view = fosv.get_view(
            dataset,
            stages=stages,
            extended_stages=extended,
            support=[start_frame, end_frame],
        )
        frames = await foo.aggregate(
            foo.get_async_db_conn()[view._dataset._sample_collection_name],
            [{"$match": {"_id": {"$in": [ObjectId(sample_id)]}}}]
            + view._pipeline(
                frames_only=True, support=[start_frame, end_frame]
            ),
        ).to_list(end_frame - start_frame + 1)

        return {
            "frames": foj.stringify(frames),
            "range": [start_frame, end_frame],
        }
