import asyncio

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



db_url: str = f'postgresql+asyncpg://{POSTEGRES_USER}:{POSTEGRES_PASSWORD}@{POSTEGRES_HOST}:{POSTEGRES_PORT}/{POSTEGRES_DB}'
async_engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=True)


class Base(DeclarativeBase):
    pass


class StarWars(Base):
    __tablename__ = 'starwars'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    birth_year: Mapped[str] = mapped_column()
    eye_color: Mapped[str] = mapped_column()  # заполняет сам пользователь при регистрации
    films: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    hair_color: Mapped[str] = mapped_column()
    height: Mapped[str] = mapped_column()
    homeworld: Mapped[str] = mapped_column()
    mass: Mapped[int] = mapped_column()
    name: Mapped[int] = mapped_column(unique=True)
    skin_color: Mapped[int] = mapped_column()
    species: Mapped[int] = mapped_column()
    starships: Mapped[int] = mapped_column()
    vehicles: Mapped[int] = mapped_column()

# async def lala():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# asyncio.run(lala())
