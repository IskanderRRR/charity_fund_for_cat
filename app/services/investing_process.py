from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing_process(new_object: CharityProject, session: AsyncSession):
    opened_charity_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == 0))
    opened_charity_projects = opened_charity_projects.scalars().all()

    not_invested_donations = await session.execute(
        select(Donation).where(Donation.invested_amount <
                               Donation.full_amount))
    not_invested_donations = not_invested_donations.scalars().all()

    for donation, project in zip(not_invested_donations,
                                 opened_charity_projects):
        not_spent_donation_balance = (donation.full_amount -
                                      donation.invested_amount)
        not_invested_project_balance = (project.full_amount -
                                        project.invested_amount)

        donation.invested_amount = min(donation.full_amount,
                                       donation.invested_amount +
                                       not_invested_project_balance)
        donation.fully_invested = (donation.invested_amount ==
                                   donation.full_amount)
        donation.close_date = (datetime.now() if
                               donation.fully_invested else None)

        project.invested_amount = min(project.full_amount,
                                      project.invested_amount +
                                      not_spent_donation_balance)
        project.fully_invested = project.invested_amount == project.full_amount
        project.close_date = datetime.now() if project.fully_invested else None

        session.add(donation)
        session.add(project)

    await session.commit()
    await session.refresh(new_object)
