from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends

from app.security.security import is_admin
from app.services.role import RoleService

router = APIRouter(prefix="/role", dependencies=[Depends(is_admin)])


async def get_role_service() -> RoleService:
    return RoleService()


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]


@router.post("/")
async def assign_role_to_user(
    role_service: RoleServiceDep, keycloak_id: UUID, role_name: str
):
    return role_service.assign_role_to_user(keycloak_id, role_name)
