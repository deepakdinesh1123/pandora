from backend.docker_client import client


def execute_task(container_name, command):
    """
    Executes the given command in the specified container

    :param container_name: Name of the container
    :param command: Command to be executed in the container
    :returns: Result of the execution of command
    """
    container = client.containers.get(container_name)
    res = container.exec_run(command)
    return res.output
