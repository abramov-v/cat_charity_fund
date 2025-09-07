from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """CRUD класс для проектов."""

    async def charity_get_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        charity = await session.execute(
            select(CharityProject).where(
                CharityProject.name == name
            )
        )
        return charity.scalars().first()


charity_crud = CRUDCharityProject(CharityProject)
