import os

from dotenv import load_dotenv
from fastapi import status
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from database import *
from elastic import *
from services import add_unique_ids, get_data_from_csv, uncheck_first_boot_flag

__all__ = (
    'ActionRepository',
)


class ActionRepository:
    @classmethod
    async def startup(cls) -> None:
        load_dotenv(".env")
        is_first_boot = os.getenv("IS_FIRST_BOOT")

        if is_first_boot == "1":
            # Projecting database table
            SQLModel.metadata.create_all(engine)

            # Filling elastic index and database
            await ActionRepository.fill_database()

            # Updating .env file
            uncheck_first_boot_flag()

            print("Project initialization finished successfully!")

    @classmethod
    async def fill_database(cls) -> JSONResponse:
        # Getting data from .csv
        df = get_data_from_csv('Task/posts.csv')

        # Generate unique keys
        add_unique_ids(df)

        # Putting data into elastic
        await put_df_into_elastic(df)

        # Putting data into database
        await put_df_into_db(df)

        response = JSONResponse(
            content={
                "message": f"Database & Elastic index successfully filled with test data",
            },
            status_code=status.HTTP_201_CREATED)
        return response

    @staticmethod
    async def search_posts(query: str) -> list_of_posts:
        # Search for text in index and return their ids
        list_of_ids = await search_for_text_in_elastic(query=query)

        # Select posts from db with ORDER BY creation date , LIMIT = 20
        posts = await select_posts_by_ids_from_db(list_of_ids)

        return posts

    @staticmethod
    async def delete_by_id(post_id: str) -> JSONResponse:
        # Deletion from index
        await delete_post_by_id_from_elastic(post_id=post_id)

        # Deletion from database
        await delete_post_by_id_from_database(post_id=post_id)

        response = JSONResponse(
            content="Post was successfully deleted!",
            status_code=status.HTTP_200_OK
        )
        return response
