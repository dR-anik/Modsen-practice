from uuid import uuid4

import pandas as pd

__all__ = (
    'get_data_from_csv',
    'add_unique_ids',
    'uncheck_first_boot_flag',
)


def get_data_from_csv(filename: str):
    """
    This function takes data from csv and returns dataframe
    :param filename: string
    :return: pd.Dataframe
    """
    return pd.read_csv(filename)


def get_uuid():
    """
    This function generates and returns random UUID4
    :return: string
    """
    return str(uuid4())


def add_unique_ids(df: pd.DataFrame):
    """
    This function add column to dataframe with unique id for each post
    :param df: pd.DataFrame
    :return: None
    """
    df['id'] = df.apply(lambda row: get_uuid(), axis=1)


def uncheck_first_boot_flag():
    """
    This function changes the value of IS_FIRST_BOOT env-variable from 1 to 0
    :return: None
    """
    with open(".env", "r") as f:
        lines = f.readlines()

    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("IS_FIRST_BOOT"):
                f.write("IS_FIRST_BOOT=0\n")
            else:
                f.write(line)
