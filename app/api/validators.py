from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectUpdate


async def check_project_exists(charity_project_id: int, session: AsyncSession):
    """Проверка существования проекта с данным id."""
    charity_project = await charity_project_crud.get(
        charity_project_id, session)
    if charity_project is None:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return charity_project


async def check_project_name_duplicate(
        project_name: str, session: AsyncSession):
    """Проверка существования проектов с данным именем."""
    charity_project = await session.execute(select(CharityProject).where(
        CharityProject.name == project_name))
    charity_project = charity_project.scalars().first()
    if charity_project is not None:
        raise HTTPException(
            status_code=400, detail="Проект с таким именем уже существует!")


async def check_project_was_invested(charity_project: CharityProject):
    """Проверка, были ли в проект инвестированы средства."""
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!")


async def check_project_was_closed(charity_project: CharityProject):
    """Проверка, закрыт ли проект."""
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!")


async def check_is_possible_to_change_amount(
    charity_project: CharityProject, obj_in: CharityProjectUpdate
):
    """Проверка на корректность изменения суммы сбора."""
    update_data = obj_in.dict(exclude_unset=True)
    if "full_amount" in update_data:
        if (update_data["full_amount"] < charity_project.invested_amount or
                update_data["full_amount"] is None):
            raise HTTPException(
                status_code=400,
                detail="Нельзя установить требуемую сумму меньше вложенной")
