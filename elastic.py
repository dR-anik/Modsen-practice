import pandas as pd
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException

__all__ = (
    'put_df_into_elastic',
    'delete_post_by_id_from_elastic',
    'search_for_text_in_elastic'
)

es = AsyncElasticsearch(
    [{
        'scheme': "http",
        'host': 'localhost',
        'port': 9200
    }]
)

index_name = 'posts'


async def put_df_into_elastic(df: pd.DataFrame):
    """
    This function puts dataframe into elastic
    :param df: pd.DataFrame
    :return: None
    """
    async with es:
        for index, row in df.iterrows():
            document = {
                'post_id': row['id'],
                'text': row['text']
            }
            await es.index(index=index_name, body=document)


async def delete_post_by_id_from_elastic(post_id: str):
    """
    This function deletes post by their ids from elastic
    :param post_id: string
    :return: None
    """
    async with es:
        response = await es.delete_by_query(
            index=index_name,
            body={
                "query": {
                    "match": {
                        "post_id": post_id
                    }
                }
            }
        )
        if response['deleted'] == 0:
            raise HTTPException(
                status_code=404,
                detail='Post not found in elastic index.'
            )


async def search_for_text_in_elastic(query: str):
    """
    This function searches query into the text in every post and returns list of ids for found posts
    :param query: string
    :return: List[str]
    """
    async with es:
        response = await es.search(
            index=index_name,
            body={
                "query": {
                    "match": {
                        "text": query
                    }
                }
            }
        )
        hits = response['hits']['hits']
        post_ids = [hit['_source']['post_id'] for hit in hits]
        return post_ids
