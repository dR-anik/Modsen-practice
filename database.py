from typing import List

import pandas as pd
from dotenv import dotenv_values
from fastapi import HTTPException
from sqlalchemy import desc
from sqlmodel import Session, create_engine

from models import Posts

__all__ = (
    'engine',
    'put_df_into_db',
    'delete_post_by_id_from_database',
    'select_posts_by_ids_from_db',
)

# Env variables
config = dotenv_values(".env")
username = config["POSTGRES_USER"]
password = config["POSTGRES_PASSWORD"]
db = config["POSTGRES_DB"]


postgresql_url = f"postgresql://{username}:{password}@localhost/{db}"
engine = create_engine(postgresql_url, echo=True)


async def put_df_into_db(df: pd.DataFrame):
    """
    This function puts posts from dataframe into the database
    :param df: pd.DataFrame
    :return: None
    """
    with Session(engine) as session:
        for _, row in df.iterrows():
            post = Posts(
                id=row['id'],
                text=row['text'],
                rubrics=row['rubrics'],
                created_date=row['created_date']
            )
            session.add(post)
        session.commit()


async def delete_post_by_id_from_database(post_id: str):
    """
    This function deletes post from database
    :param post_id: string
    :return: None
    """
    with Session(engine) as session:
        post = session.query(Posts).filter(Posts.id == post_id).first()
        if post:
            session.delete(post)
            session.commit()
        else:
            raise HTTPException(
                status_code=404,
                detail='Post not found in database.'
            )


async def select_posts_by_ids_from_db(list_of_ids: List[str]):
    """
    This function selects posts by their ids from database
    :param list_of_ids: List[string]
    :return: List[Post]
    """
    with Session(engine) as session:
        posts = (
            session.query(Posts)
            .filter(Posts.id.in_(list_of_ids))
            .order_by(desc(Posts.created_date))
            .limit(20)
            .all()
        )
        return posts
