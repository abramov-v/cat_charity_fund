from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import check_charity_project_exists, check_charity_project_name_duplicate
from app.core.db import get_async_session
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)

from app.crud.charity_project import charity_crud
from app.core.user import current_user, current_superuser
from app.models import User


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    new_charity_project = await charity_crud.create(charity_project, session, user)
    return new_charity_project


@router.delete(
    '/charity_project/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    charity_project = await charity_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/charity_project/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    if obj_in.name:
        await check_charity_project_name_duplicate(obj_in.name, session)
    
    charity_project = await charity_crud.update(
        charity_project, session, obj_in
    )
    return charity_project
