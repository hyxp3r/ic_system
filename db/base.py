import re
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative, scoped_session, sessionmaker
from sqlalchemy_utils import generic_repr

from db.settings import DBSettings

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}
metadata = MetaData(naming_convention=convention)


def classname_to_tablename(name: str) -> str:
    result: List[str] = []

    last_index = 0
    for match in re.finditer(r'(?P<abbreviation>[A-Z]+(?![a-z]))|(?P<word>[A-Za-z][a-z]+)|(?P<digit>\d+)', name):
        if match.start() != last_index:
            raise ValueError(f'Could not translate class name "{name}" to table name')

        last_index = match.end()
        result.append(match.group().lower())

    return '_'.join(result)


@as_declarative(metadata=metadata)
@generic_repr
class BaseTable:
    @declared_attr  # type: ignore
    def __tablename__(cls) -> Optional[str]:  # noqa
        return classname_to_tablename(cls.__name__)  # type: ignore  #pylint: disable=E1101

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())


db_settings = DBSettings()

async_engine = db_settings.setup_engine_async()
sync_engine = db_settings.setup_engine_sync()

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
sync_session = scoped_session(sessionmaker(sync_engine))
