from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, UserDonation
from app.services.investing_process import investing_process

router = APIRouter()


@router.get(
    "/donation/",
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    description="Получает список всех пожертвований."
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.post(
    "/donation/",
    response_model=UserDonation,
    response_model_exclude_none=True,
    description="Сделать пожертвование."
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)
    await investing_process(new_donation, session)
    return new_donation


@router.get(
    "/donation/my/",
    response_model=List[UserDonation],
    response_model_exclude_none=True,
    description="Получить список моих пожертвований."
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_user_donations(session=session, user=user)
