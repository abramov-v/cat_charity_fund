from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models.charity_project import CharityProject


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка, что проект с данным ID существует."""

    charity_project = await charity_crud.get(charity_project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проекта с таким именем не существует.'
        )
    return charity_project


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка, что имя проекта уникально."""

    charity_project = await charity_crud.charity_get_by_name(
        charity_project_name, session
    )
    if charity_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует.'
        )


async def check_project_not_fully_invested(project: CharityProject) -> None:
    """Запрет на редактирование/удаление закрытых проектов."""

    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать или удалять.",
        )


async def check_full_amount_not_less_than_invested(
    new_amount: int,
    project: CharityProject,
) -> None:
    """Запрет на уменьшение требуемой суммы ниже уже вложенной."""

    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя установить требуемую сумму меньше уже вложенной.",
        )


async def check_project_has_no_investments_for_delete(
    project: CharityProject,
) -> None:
    """Запрет на удаление проекта, если в него уже внесены средства."""

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект уже были внесены средства — удаление запрещено.',
        )
