import os

from backend.docker_client import client


def build_docker_image(image_name: str, image_tag: str) -> str:
    """
    Builds a docker image using the docker file stored in the /tmp folder

    Parameters:
    :param image_name: the name of the docker image
    :param image_tag: the tag for the docker image
    :returns: A string of the format 'image_name:image_tag'
    """
    client.images.build(
        path="./user-dockerfiles/",
        dockerfile=f"{image_name}.dockerfile",
        tag=f"{image_name}:{image_tag}",
    )
    return f"{image_name}:{image_tag}"
