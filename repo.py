from sqlalchemy import select
from database import Project, async_session
from database import User, async_session

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