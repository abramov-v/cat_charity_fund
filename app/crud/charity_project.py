from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.services.investing import apply_transfer, is_closed


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

    async def invest_new_project(
        self,
        project: CharityProject,
        session: AsyncSession
    ) -> None:
        if project.fully_invested:
            return

        result = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(Donation.create_date.asc(), Donation.id.asc())
        )
        donations = result.scalars().all()

        for donation in donations:
            if is_closed(project):
                break
            apply_transfer(donation, project)

        await session.commit()
        await session.refresh(project)


charity_crud = CRUDCharityProject(CharityProject)
