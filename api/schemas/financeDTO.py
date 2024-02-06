from datetime import datetime

from pydantic import BaseModel, field_validator


class FinanceSchemaAdd(BaseModel):
    fio: str
    personal_number: str
    contract_number: str
    sum: float
    status: bool = True
    file_created_time: datetime

    @field_validator('personal_number')
    def must_be_int(cls, v: str) -> str | ValueError:
        try:
            int(v)
        except ValueError:
            raise ValueError('mast contains only digits')
        return v


class FinanceSchema(FinanceSchemaAdd):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
