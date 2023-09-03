from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .abstract_model import AbstractModel


class Donation(AbstractModel, Base):
    """Модель пожертвования."""
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
