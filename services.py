from uuid import uuid4

import pandas as pd

__all__ = (
    'get_data_from_csv',
    'add_unique_ids',
    'uncheck_first_boot_flag',
)


def get_data_from_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


def get_uuid() -> str:
    """Returns unique UUID (UUID4)"""
    return str(uuid4())


def add_unique_ids(df: pd.DataFrame) -> None:
    """Adding new column to df with unique IDs"""
    df['id'] = df.apply(lambda row: get_uuid(), axis=1)


def uncheck_first_boot_flag() -> None:
    with open(".env", "r") as f:
        lines = f.readlines()

    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("IS_FIRST_BOOT"):
                f.write("IS_FIRST_BOOT=0\n")
            else:
                f.write(line)