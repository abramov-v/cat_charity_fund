from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db import get_async_session
from app.schemas.donation import DonationAdminOut, DonationCreate, DonationUserOut

from app.crud.donation import donation_crud
from app.core.user import current_superuser, current_user
from app.models import User


router = APIRouter()



@router.get(
    '/',
    response_model=list[DonationAdminOut],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationUserOut,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_donation(
    obj_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(obj_in, session, user)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserOut],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    user_donations = await donation_crud.get_user_donations(user, session)
    return user_donations
