import time

from fastapi import APIRouter, WebSocket

from backend.task_queue import execution_task_queue
from backend.tasks.execute_tasks import execute_task

router = APIRouter()


@router.websocket("/execute/{container_name}")
async def execute(websocket: WebSocket, container_name: str):
    """
    Opens a websocket connection with the terminal in te frontend
    and executes the command in the respective container and returns
    the result

    :param websocket: WebSocket object passed by FastAPI
    :param container: Name of the container

    """
    await websocket.accept()
    while True:
        command = await websocket.receive_text()
        task = execution_task_queue.enqueue(execute_task, container_name, command)
        task_id = task.get_id()
        resp = await get_execution_status(task_id)
        await websocket.send_text(resp)


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
