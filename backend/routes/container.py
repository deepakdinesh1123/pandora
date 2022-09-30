from docker.errors import NotFound
from fastapi import APIRouter
from pydantic import BaseModel

from backend.docker_client import client

router = APIRouter()


class Container(BaseModel):
    image_name: str
    container_name: str
    container_settings: dict


@router.post("/create_container/")
def create_container(container: Container):
    """
    Starts a container as a daemon process with a pseudo-TTY,
    if it does not exist and returns the name of the container


    :param container: request body must contain a JSON object with
                      the image_name, conatiner_name and the arguments
                      to the docker run command as a JSON object
    :returns: Name of the container created
    """
    try:
        client.containers.get(container.container_name)
    except NotFound:
        try:
            client.containers.run(
                image=container.image_name,
                name=container.container_name,
                detach=True,
                tty=True,
                **container.container_settings,
            )
        except Exception as e:
            print(e)
    return container.container_name
