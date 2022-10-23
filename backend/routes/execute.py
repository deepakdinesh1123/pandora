import time
import subprocess

from fastapi import APIRouter
from pydantic import BaseModel

from backend.task_queue import execution_task_queue
from backend.tasks.execute_tasks import execute_task
from backend.docker_client import client

router = APIRouter()

class Command(BaseModel):
    user_command: str
    editor_content: str


async def get_execution_status(task_id):
    """
    Checks the status of the execution job every 3 seconds
    and return the result of the task upon the completion of
    the task

    :param task_id: ID of the task added to the execution task queue
    :returns: Result of the execution
    """
    task = execution_task_queue.fetch_job(task_id)
    while True:
        status = task.get_status()
        if status == "finished":
            return task.result
        else:
            time.sleep(3)

@router.post("/execute/req/{container_name}/")
async def execute(command: Command, container_name: str):
    """
    Receives the command entered by the user in the terminal and adds
    it to the task queue for execution. Upon receiving the execution result, 
    returns it back to the user
    :param command: Request body must contain a JSON object with the user_command and the 
                    contents of the editor
    :container_name: Name of the container
    """
    with open('/tmp/temp.py', 'w') as f:
        f.writelines(command.editor_content)

    # TODO Add support for tarfile
    # with tarfile.open('/tmp/exec.tar.gz', 'w') as archive:
    #     archive.add('/tmp/temp.py')
    
    # container = client.containers.get("sleep")
    # container.put_archive("/", tarfile.open('/tmp/exec.tar.gz'))

    container_id = client.containers.get("sleep").id

    subprocess.run(["docker", "cp", "/tmp/temp.py", f"{container_id}:/temp.py"])

    task = execution_task_queue.enqueue(execute_task, container_name, command.user_command)
    task_id = task.get_id()
    resp = await get_execution_status(task_id)
    return resp
