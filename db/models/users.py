import sqlalchemy as sa

from api.schemas.studentDTO import StudentSchema
from db.base import BaseTable


class Students(BaseTable):
    """Таблица со студентами"""

    fio = sa.Column(sa.String(255), nullable=False, doc='ФИО студента')
    personal_number = sa.Column(sa.String(10), nullable=False, unique=True, doc='Личный номер студента', index=True)
    group = sa.Column(sa.String(10), nullable=False, doc='Группа')
    program = sa.Column(sa.String(100), nullable=False, doc='Направление')
    form = sa.Column(sa.String(50), nullable=False, doc='Форма')
    email = sa.Column(sa.String(255), nullable=True, doc='Почта')
    api_key = sa.Column(sa.String(255), nullable=True, doc='API ключ')


    def to_read_model(self) -> StudentSchema:
        return StudentSchema(
            id=self.id,
            fio=self.fio,
            personal_number=self.personal_number,
            group=self.group,
            program = self.program,
            form=self.form,
            email=self.email

        )
    

