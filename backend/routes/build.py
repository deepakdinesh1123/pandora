import asyncio

from fastapi import APIRouter, Request
from pydantic import BaseModel
from sse_starlette import EventSourceResponse

from backend.task_queue import build_task_queue
from backend.tasks.build_tasks import build_docker_image

DOCKERFILE_PATH = "/tmp"
STATUS_STREAM_DELAY = 5  # seconds
STATUS_STREAM_RETRY_TIMEOUT = 30000  # milisecond


class DockerImage(BaseModel):
    name: str
    tag: str
    dockerfile: str


router = APIRouter()


@router.post("/build_image/")
def build_image(image: DockerImage):
    """
    The contents of the dockerfile are read from
    request body and is written to a file in /tmp folder
    and the task of building an image using the dockerfile
    is added  to the redis queue

    :param image: request body must contain a JSON object with the image_name,
                  image_tag and the contents of the dockerfile
    :returns: JSON object with the status and the build_id
              which can be used to check the image build status.
    """
    with open(f"/tmp/{image.name}.dockerfile", "w") as f:
        f.writelines(image.dockerfile)
    try:
        task = build_task_queue.enqueue(build_docker_image, image.name, image.tag)
    except Exception as e:
        print(str(e))
        response_object = {"status": "Failure"}
    response_object = {"status": "success", "build_id": task.get_id()}
    return response_object


@router.get("/build_image/{build_id}")
def get_build_status(request: Request, build_id: str):
    """
    This method returns and EventSourceResponse that can be used by the client
    to subscribe to the current status of the build

    :param request: Request object passed by FastAPI
    :param build_id: The id of the task added to the queue
    :returns: An EventSourceResponse with a asynchronous generator that returns
              the status of the build
    """
    status_generator = build_status_generator(request, build_id)
    return EventSourceResponse(status_generator)


async def get_status(build):
    return build.get_status()


async def build_status_generator(request: Request, build_id: str):
    """
    Gets the current status of the build every 5 seconds
    and returns it

    :param request: Request object passed by FastAPI
    :param build_id: The id of the task added to the task queue
    :returns: The current build status
    """
    build = build_task_queue.fetch_job(build_id)
    while True:
        if await request.is_disconnected():
            print("Disconnected")

        currrent_build_status = await get_status(build)

        if currrent_build_status == "finished":
            yield {"event": "end", "data": "finished"}
            break

        if currrent_build_status == "queued":
            yield {
                "event": "update",
                "retry": STATUS_STREAM_RETRY_TIMEOUT,
                "data": "queued",
            }

        await asyncio.sleep(STATUS_STREAM_DELAY)
