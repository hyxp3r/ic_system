import pytest

from sqlalchemy import func, insert, select

from api.tasks.cron.students_update import get_students_with_key, get_students_tandem, update_api_keys, insert_students, update_students
from db import Students, sync_session
from api.schemas.studentDTO import StudentSchema, StudentSchemaAdd

@pytest.fixture
def add_student_with_api():
    stmt = insert(Students).values(fio = "Тест",
                                    personal_number = "233447",
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

@pytest.fixture
def students_with_no_api():
    stmt = insert(Students).values(fio = "Тест",
                                    personal_number = "190722",
                                    group = "ПИ901",
                                    program = "Прикладная",
                                    form = "Очная",
                                    api_key = "",
                                    email = "erma2001@mail.ru")
    with sync_session() as session:
        session.execute(stmt)
        sync_session.commit()
    yield
    with sync_session() as session:
        session.query(Students).delete()
        session.commit()

@pytest.fixture
def delete_students():
    yield
    with sync_session() as session:
        session.query(Students).delete()
        session.commit()

def test_students_with_api(add_student_with_api):
    results = get_students_with_key()
    for item in results:
        assert isinstance(item, StudentSchema)

def test_get_students_tandem():
    results = get_students_tandem()
    for item in results:
        assert isinstance(item, StudentSchemaAdd)
 
def test_update_api_keys(students_with_no_api):
    student_1 = StudentSchema(
        id = 1,
        fio = "Тест",
        personal_number = "190722",
        group = "ПИ901",
        program = "Прикладная",
        form = "Очная",
        api_key = "1245",
        email = "erma2001@mail.ru"
)
    students_api = [student_1]
    update_api_keys(students_api)
    stmt = select(Students).filter_by(personal_number="190722")
    cursor = sync_session.execute(stmt)
    res = cursor.one_or_none()
    student = res[0].to_read_model()
    assert student.api_key == student_1.api_key

def test_insert_students(delete_students):
    students_tandem_schema = get_students_tandem()
    len_students_tandem_schema = len(students_tandem_schema)
    insert_students(students_tandem_schema)
    stmt = select(func.count(Students.id))
    with sync_session() as session:
        count = session.execute(stmt)
        count = count.scalar_one()
    assert len_students_tandem_schema == count

def test_update_students(add_student_with_api):
    update_students()
    stmt = select(func.count(Students.id))
    with sync_session() as session:
        count = session.execute(stmt)
        count = count.scalar_one()
    assert count > 0
    stmt = select(Students).filter_by(personal_number="233447")
    cursor = sync_session.execute(stmt)
    res = cursor.one_or_none()
    student = res[0].to_read_model()
    assert student.api_key == "test"