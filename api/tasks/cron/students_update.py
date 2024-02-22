from sqlalchemy import insert, select, update

from api.schemas.studentDTO import StudentSchema, StudentSchemaAdd
from api.utils.tandem import Tandem
from db import Students, sync_session

def get_students_with_key() -> list[StudentSchema]:
    stmt = select(Students).filter(Students.api_key.isnot(None))
    with sync_session() as session:
        res = session.execute(stmt)
        students_api =  [row[0].to_read_model() for row in res.all()]
    return students_api

def get_students_tandem() -> list[StudentSchemaAdd]:
    tandem_session = Tandem()
    with tandem_session:
        students_tandem = tandem_session.get_students()
    students_tandem_schemas = []
    for student in students_tandem:
        student_schema = StudentSchemaAdd(
            fio=student["fio"],
            personal_number=student["personal_number"],
            group=student["group"],
            program=student["program"],
            form = student["form"],
            email = student["email"],
        )
        students_tandem_schemas.append(student_schema)
    return students_tandem_schemas

def update_api_keys(sudents_api:list[StudentSchema]):
    if len(sudents_api) != 0:
        for student in sudents_api:
            stmt = update(Students).filter_by(personal_number=student.personal_number).values(api_key=student.api_key)
            with sync_session() as session:
                session.execute(stmt)
                session.commit()

def insert_students(students_tandem_schemas:list[StudentSchemaAdd]):
        with sync_session() as session:
                for student in students_tandem_schemas:
                    stmt = insert(Students).values(**student.model_dump())
                    session.execute(stmt)
                session.commit()

def update_students_table():
    students_tandem_schemas = get_students_tandem()
    students_api = get_students_with_key()
    with sync_session() as session:
        session.query(Students).delete()
        session.commit()
    insert_students(students_tandem_schemas)
    if len(students_api) > 0:
        update_api_keys(students_api)