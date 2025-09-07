from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def is_closed(obj) -> bool:
    return obj.invested_amount >= obj.full_amount


def close_obj(obj) -> None:
    if not obj.fully_invested and is_closed(obj):
        obj.fully_invested = True
        obj.close_date = utcnow()


def free_amount(obj) -> int:
    return max(0, obj.full_amount - obj.invested_amount)


def _apply_transfer(donation: Donation, project: CharityProject) -> int:
    if donation.fully_invested or project.fully_invested:
        return 0
    take = min(free_amount(donation), free_amount(project))
    if take <= 0:
        return 0
    project.invested_amount += take
    donation.invested_amount += take
    close_obj(project)
    close_obj(donation)
    return take


async def invest_new_project(
        project: CharityProject,
        session: AsyncSession
) -> None:
    if project.fully_invested:
        await session.refresh(project)
        return

    result = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date.asc(), Donation.id.asc())
    )
    donations = list(result.scalars().all())

    for donation in donations:
        if is_closed(project):
            break
        _apply_transfer(donation, project)

    await session.commit()
    await session.refresh(project)


async def invest_new_donation(
        donation: Donation,
        session: AsyncSession
) -> None:
    if donation.fully_invested:
        await session.refresh(donation)
        return

    result = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(CharityProject.create_date.asc(), CharityProject.id.asc())
    )
    projects = list(result.scalars().all())

    for project in projects:
        if is_closed(donation):
            break
        _apply_transfer(donation, project)

    await session.commit()
    await session.refresh(donation)
