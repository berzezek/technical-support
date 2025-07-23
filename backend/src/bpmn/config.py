# import asyncio

from pyzeebe import ZeebeWorker, ZeebeClient, create_insecure_channel

# from app.services.bpmn.workers.notifier import notify_service
# from app.services.bpmn.workers.lead_exists import service_process_lead_exists


channel = create_insecure_channel()


worker = ZeebeWorker(channel)
client = ZeebeClient(channel)
