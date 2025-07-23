import asyncio

from pyzeebe import ZeebeWorker, ZeebeClient, create_insecure_channel

from app.services.bpmn.workers.notifier import notify_service
from app.services.bpmn.workers.lead_exists import service_process_lead_exists


channel = create_insecure_channel()


worker = ZeebeWorker(channel)
client = ZeebeClient(channel)


async def start_workers():
    notify_service(worker)
    service_process_lead_exists(worker)
    await worker.work()


async def stop_workers(task):
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
