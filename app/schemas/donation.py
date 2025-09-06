from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    """TEST"""

    full_amount: PositiveInt
    comment: Optional[str] = None

    class Config:
        extra = 'forbid'


class DonationCreate(DonationBase):
    """TEST"""


class DonationUserOut(DonationBase):
    """TEST"""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAdminOut(DonationUserOut):
    """TEST"""

    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True



