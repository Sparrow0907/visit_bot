from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings
from sqlalchemy import select
from models import Slot

DATABASE_URL = settings.database_url


engine = create_async_engine(DATABASE_URL, echo = True)
# Использует за пределами этого файла, чтобы обращаться к сессии
new_session = async_sessionmaker(engine, expire_on_commit=False)

                    # это будет new_session
async def get_slots(session: AsyncSession):
    result = await session.execute(
        select(Slot).where(Slot.is_booked == False)
    )
    return result.scalars().all()