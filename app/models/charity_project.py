from sqlalchemy import Column, String, Text

from app.core.db import Base

from .abstract_model import AbstractModel


class CharityProject(AbstractModel, Base):
    """Модель проекта."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
