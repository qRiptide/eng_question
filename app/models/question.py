from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import select, insert

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    question_id = Column(Integer, nullable=False, unique=True)
    question_text = Column(Text, nullable=False, unique=True)
    answer_text = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)

    @classmethod
    async def select_all_questions_text(cls, db_session: AsyncSession):
        query = select(cls.question_text)
        all_rows = await db_session.scalars(query)
        return all_rows.all()

    @classmethod
    async def insert_question(cls, db_session: AsyncSession, question: list) -> None:
        await db_session.execute(insert(cls), question)
