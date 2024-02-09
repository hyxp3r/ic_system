import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import func, insert, select, update

from api.config import FILE_PATH
from db import sync_session
from db.models.finance import FinancialIndebtedness


def get_mtime(file_path: Path) -> datetime:
    try:
        mtime = os.path.getmtime(file_path)
    except FileNotFoundError as e:
        # logger.error("File doesn't exist:", e)
        raise FileNotFoundError()

    mtime_readable = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return mtime_readable


def get_count() -> int:
    stmt = select(func.count(FinancialIndebtedness.id))
    with sync_session() as session:
        count = session.execute(stmt)
    return count.scalar_one()


def get_date_db() -> datetime:
    stmt = select(FinancialIndebtedness).filter_by(status=True)
    with sync_session() as session:
        res = session.execute(stmt)
        file_date = res.all()[0][0].file_date()
    return file_date


def make_dates_compare(file_time: datetime, db_time: datetime):
    if file_time == db_time:
        return True
    return False


def get_file_data(file_path: Path) -> list[dict]:
    df = pd.read_excel(
        file_path,
        usecols=[
            'Субконто1.Юридическое физическое лицо.Наименование',
            'Учащийся.Номер личного дела',
            'Субконто2.Номер договора',
            'Сумма Конечный остаток Дт',
        ],
    )
    df['Сумма Конечный остаток Дт'] = df['Сумма Конечный остаток Дт'].fillna(0)
    df = df[df['Сумма Конечный остаток Дт'] != 0]
    data = df.to_dict('records')
    return data


def update_insert_data(data: list[dict], file_time) -> str:
    stmt_upd = update(FinancialIndebtedness).where(FinancialIndebtedness.status == True).values(status=False)
    with sync_session() as session:
        with session.begin():
            session.execute(stmt_upd)
            for item in data:
                stmt_ins = insert(FinancialIndebtedness).values(
                    fio=item['Субконто1.Юридическое физическое лицо.Наименование'],
                    personal_number=item['Учащийся.Номер личного дела'],
                    contract_number=item['Субконто2.Номер договора'],
                    sum=item['Сумма Конечный остаток Дт'],
                    file_created_time=file_time,
                )
                session.execute(stmt_ins)
    return 'Данные успешно обновлены и добавлены'


def insert_data(data: list[dict], file_time)  -> str:
    with sync_session() as session:
        with session.begin():
            for item in data:
                stmt_ins = insert(FinancialIndebtedness).values(
                    fio=item['Субконто1.Юридическое физическое лицо.Наименование'],
                    personal_number=item['Учащийся.Номер личного дела'],
                    contract_number=item['Субконто2.Номер договора'],
                    sum=item['Сумма Конечный остаток Дт'],
                    file_created_time=file_time,
                )
                session.execute(stmt_ins)
    return 'Данные успешно добавлены'

def finance_update_task(file_path = FILE_PATH):
    file_time = get_mtime(file_path)
    count_data_table = get_count()
    data = get_file_data(file_path)
    if count_data_table > 0:
        db_time = get_date_db()
        compare_result = make_dates_compare(file_time, db_time)
        if compare_result:
            return "Обновление данных не требуется"
        result = update_insert_data(data, file_time)
        return result
    result = insert_data(data, file_time)
    return result
    