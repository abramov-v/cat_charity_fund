from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.abstract import AbstractCharityDonation


class Donation(AbstractCharityDonation):
    """Модель пожертвования от пользователя."""

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
