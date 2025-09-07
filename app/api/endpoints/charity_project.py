from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_name_duplicate,
                                check_full_amount_not_less_than_invested,
                                check_project_has_no_investments_for_delete,
                                check_project_not_fully_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import invest_new_project

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
):
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_crud.create(charity_project, session)
    await invest_new_project(new_charity_project, session)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_charity_project_exists(project_id, session)
    await check_project_not_fully_invested(project)
    await check_project_has_no_investments_for_delete(project)
    return await charity_crud.remove(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_charity_project_exists(project_id, session)
    await check_project_not_fully_invested(project)

    if obj_in.name:
        await check_charity_project_name_duplicate(
            obj_in.name, session
        )

    if obj_in.full_amount is not None:
        await check_full_amount_not_less_than_invested(
            obj_in.full_amount, project
        )

    updated = await charity_crud.update(project, obj_in, session)
    return updated
