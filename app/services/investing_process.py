from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing_process(new_object: CharityProject, session: AsyncSession):
    opened_charity_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == 0))
    opened_charity_projects = opened_charity_projects.scalars().all()
    print(opened_charity_projects)
    not_invested_donations = await session.execute(
        select(Donation).where(Donation.invested_amount < Donation.full_amount))
    not_invested_donations = not_invested_donations.scalars().all()
    print(not_invested_donations)
    if opened_charity_projects and not_invested_donations:
        donation_idx = 0
        project_idx = 0
        while ((donation_idx < len(not_invested_donations)) and
               (project_idx < len(opened_charity_projects))):
            donation, project = not_invested_donations[donation_idx], opened_charity_projects[project_idx]
            not_spent_donation_balance = donation.full_amount - donation.invested_amount
            not_invested_project_balance = project.full_amount - project.invested_amount
            if not_spent_donation_balance > not_invested_project_balance:
                donation.invested_amount += not_invested_project_balance
                session.add(donation)
                project.invested_amount = project.full_amount
                project.fully_invested = True
                project.close_date = datetime.now()
                session.add(project)
                project_idx += 1
            elif not_spent_donation_balance < not_invested_project_balance:
                donation.invested_amount = donation.full_amount
                donation.fully_invested = True
                donation.close_date = datetime.now()
                session.add(donation)
                project.invested_amount += not_spent_donation_balance
                session.add(project)
                donation_idx += 1
            else:
                donation.invested_amount = donation.full_amount
                donation.fully_invested = True
                donation.close_date = datetime.now()
                session.add(donation)
                project.invested_amount = project.full_amount
                project.fully_invested = True
                project.close_date = datetime.now()
                session.add(project)
                donation_idx += 1
                project_idx += 1
        await session.commit()
        await session.refresh(new_object)
