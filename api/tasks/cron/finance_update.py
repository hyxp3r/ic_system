from datetime import datetime, timezone
import os
from pathlib import Path

from sqlalchemy import func, select

from api.config import FILE_PATH
from db import sync_session
from db.models.finance import FinancialIndebtedness

def get_mtime(file_path:Path) -> datetime:
    try:
        mtime = os.path.getmtime(file_path)
    except FileNotFoundError as e:
       # logger.error("File doesn't exist:", e)
        raise FileNotFoundError()

    mtime_readable = datetime.fromtimestamp(mtime, tz = timezone.utc)
    return mtime_readable


def get_count() -> int:
    stmt = select(func.count(FinancialIndebtedness.id)) 
    with sync_session() as session:
        count = session.execute(stmt)
    return count.scalar_one()

def get_date_db() -> datetime:
    stmt = select(FinancialIndebtedness).filter_by(status = True)
    with sync_session() as session:
        res = session.execute(stmt)
        file_date = res.all()[0][0].file_date()
    return file_date
