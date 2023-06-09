import aiohttp
from fastapi import FastAPI
from app.db_session import AsyncSessionFactory
from app.data_models import QuestionValidate, Count
from app.models.question import Question

app = FastAPI(title='Question App', version='0.1:beta', debug=False)


async def get_questions(count: int = 1) -> dict:
    url = 'https://jservice.io/api/random?count='
    async with aiohttp.ClientSession() as session:
        async with session.get(url + str(count)) as resp:
            return await resp.json()


async def validate_question(question_to_db: QuestionValidate,
                            questions_in_db: list) -> QuestionValidate:
    while True:
        if question_to_db.question_text in questions_in_db:
            new = await get_questions()
            question_to_db = QuestionValidate(**new[0])
        else:
            return question_to_db


@app.post('/get_question')
async def get_question(body: Count):
    to_db = []
    questions = await get_questions(body.question_num)

    async with AsyncSessionFactory() as conn:
        questions_in_db = await Question.select_all_questions_text(conn)

        for q in questions:
            question = QuestionValidate(**q)
            unique_question = await validate_question(question, questions_in_db)
            to_db.append(unique_question.dict())

        await Question.insert_question(conn, to_db)
        await conn.commit()

    if questions_in_db:
        return {'question': questions_in_db[-1]}

    return {}
