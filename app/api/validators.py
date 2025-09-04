from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models.charity_project import CharityProject

from app.models import User



async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_crud.get(charity_project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Такого проекта несуществует'
        )
    return charity_project


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_crud.charity_get_by_name(charity_project_name, session)
    if charity_project_id:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем существует.'
        )
    

#проверить все ниже


# app/api/validators.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import CharityProject


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await session.get(CharityProject, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден.",
        )
    return project


async def check_charity_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    query = select(CharityProject).where(CharityProject.name == project_name)
    result = await session.execute(query)
    project = result.scalars().first()
    if project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует.",
        )


async def check_project_not_fully_invested(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать или удалять.",
        )


async def check_full_amount_not_less_than_invested(
    new_amount: int,
    project: CharityProject,
) -> None:
    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя установить требуемую сумму меньше уже вложенной.",
        )
