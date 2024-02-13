from datetime import datetime

from pydantic import BaseModel, field_validator


class StudentSchemaAdd(BaseModel):
    fio: str
    personal_number: str
    group: str
    program: str
    form: str
    email: str | None = None

    @field_validator('personal_number')
    def must_be_int(cls, v: str) -> str | ValueError:
        try:
            int(v)
        except ValueError:
            raise ValueError('mast contains only digits')
        return v


class StudentSchema(StudentSchemaAdd):
    id: int

    class Config:
        from_attributes = True
