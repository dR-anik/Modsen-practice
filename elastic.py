from typing import List, Tuple

import pandas as pd
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException

__all__ = (
    'put_df_into_elastic',
    'get_index_count',
    'clear_elastic_index',
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


async def put_df_into_elastic(df: pd.DataFrame) -> None:
    async with es:
        for index, row in df.iterrows():
            document = {
                'post_id': row['id'],
                'text': row['text']
            }
            await es.index(index=index_name, body=document)


async def get_index_count(name: str = index_name) -> Tuple[str, int]:
    """Returns index_name & number of items in index"""
    response = await es.count(index=name)
    return name, response['count']


async def clear_elastic_index(name: str = index_name) -> str:
    await es.delete_by_query(index=name, body={"query": {"match_all": {}}})
    return name


async def delete_post_by_id_from_elastic(post_id: str) -> None:
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


async def search_for_text_in_elastic(query: str) -> List[str]:
    """Searches for text in posts and returns list of IDs for found posts"""
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