from datetime import datetime

from pydantic import BaseModel, Field, validator


class Count(BaseModel):
    question_num: int = Field(ge=1)


class QuestionValidate(BaseModel):
    question_id: int = Field(alias='id')
    question_text: str = Field(alias='question')
    answer_text: str = Field(alias='answer')
    created_at: datetime

    @validator('created_at')
    def remove_tz(cls, time):
        return time.replace(tzinfo=None)
