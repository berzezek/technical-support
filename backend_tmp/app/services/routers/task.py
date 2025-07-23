from fastapi import APIRouter, Depends, status, Request
from app.services.auth import require_roles_any
from app.services.auth.auth_dep import get_current_user
from app.services.bpmn.user_tasks.assigiment import task_assignment, task_unassignment

router = APIRouter()


@router.post("/user-task-assignment", status_code=status.HTTP_204_NO_CONTENT)
@require_roles_any(["Operator"])
async def secure_data(request: Request, user_task: str, user: dict = Depends(get_current_user)):
    return await task_assignment(user_task, user)

@router.post("/user-task-unassignment", status_code=status.HTTP_204_NO_CONTENT)
@require_roles_any(["Administrator"])
async def user_task_unassignment(
    request: Request,
    user_task: str,
    current_user: dict = Depends(get_current_user),
):
    return await task_unassignment(user_task, current_user)