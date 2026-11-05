from sqlalchemy import select
from database import Project, async_session
from database import User, async_session
from datetime import datetime, timedelta, timezone
from sqlalchemy import func, select

async def get_projects() -> list[Project]:
    async with async_session() as session:
        result = await session.execute(select(Project))
        return list(result.scalars().all())
    
async def add_project(title: str, description: str, url: str | None = None):
    async with async_session() as session:
        session.add(Project(title=title, description=description, url=url))
        await session.commit()
        
async def add_user(tg_id: int, username: str | None, full_name: str) -> bool:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if user is not None:
            return False

        session.add(User(tg_id=tg_id, username=username, full_name=full_name))
        await session.commit()
        return True
    
async def get_stats() -> dict:
    week_ago = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=7)
    async with async_session() as session:
        total = (await session.execute(select(func.count(User.id)))).scalar_one()
        week = (
            await session.execute(
                select(func.count(User.id)).where(User.created_at >= week_ago)
            )
        ).scalar_one()
        projects = (await session.execute(select(func.count(Project.id)))).scalar_one()
        last = (
            await session.execute(select(User).order_by(User.id.desc()).limit(5))
        ).scalars().all()
    return {"total": total, "week": week, "projects": projects, "last": list(last)}

async def delete_project(project_id: int) -> bool:
    async with async_session() as session:
        project = await session.get(Project, project_id)
        if project is None:
            return False
        await session.delete(project)
        await session.commit()
        return True

async def get_lang(tg_id: int) -> str:
    async with async_session() as session:
        result = await session.execute(select(User.lang).where(User.tg_id == tg_id))
        return result.scalar_one_or_none() or "en"


async def set_lang(tg_id: int, lang: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.lang = lang
            await session.commit()