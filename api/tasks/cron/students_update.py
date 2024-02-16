from sqlalchemy import select

from db import Students, sync_session





def get_students_with_key():
    stmt = select(Students).filter(Students.api_key.isnot(None))
    with sync_session() as session:
        res = session.execute(stmt)
        students_api =  [row[0].to_read_model() for row in res.all()]
    print(students_api)
    return students_api