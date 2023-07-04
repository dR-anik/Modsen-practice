from datetime import datetime

from sqlmodel import Field, SQLModel


class Posts(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    text: str
    rubrics: str
    created_date: datetime
