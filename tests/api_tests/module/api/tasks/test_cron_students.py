import pytest

from sqlalchemy import insert

from api.tasks.cron.students_update import get_students_with_key
from db import Students, sync_session
from api.schemas.studentDTO import StudentSchema

@pytest.fixture
def add_student_with_api():
    stmt = insert(Students).values(fio = "Тест",
                                    personal_number = "190722",
                                    group = "ПИ901",
                                    program = "Прикладная",
                                    form = "Очная",
                                    api_key = "test",
                                    email = "erma2001@mail.ru")
    with sync_session() as session:
        session.execute(stmt)
        sync_session.commit()
    yield
    with sync_session() as session:
        session.query(Students).delete()
        session.commit()

def test_students_with_api(add_student_with_api):

    results = get_students_with_key()
    for item in results:
        assert isinstance(item, StudentSchema)
 