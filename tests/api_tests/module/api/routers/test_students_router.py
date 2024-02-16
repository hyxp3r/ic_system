import pytest
from sqlalchemy import insert
from httpx import AsyncClient

from api.redis.redis import Redis
from db import Students, sync_session

@pytest.fixture
def add_student_with_email():
    stmt = insert(Students).values(fio = "Тест",
                                    personal_number = "190722",
                                    group = "ПИ901",
                                    program = "Прикладная",
                                    form = "Очная",
                                    email = "erma2001@mail.ru")
    with sync_session() as session:
        session.execute(stmt)
        sync_session.commit()
    yield
    with sync_session() as session:
        session.query(Students).delete()
        session.commit()


@pytest.fixture
def add_student_with_no_email():
    stmt = insert(Students).values(fio = "Тест",
                                    personal_number = "190722",
                                    group = "ПИ901",
                                    program = "Прикладная",
                                    form = "Очная",)
    with sync_session() as session:

        session.execute(stmt)
        sync_session.commit()
    yield
    with sync_session() as session:
        session.query(Students).delete()
        session.commit()
        
@pytest.fixture
async def set_user_key():
        redis = Redis()
        personal_number = "190722"
        verification_code = "123456"
        async with redis:
            await redis.set(key=personal_number, value=verification_code, ex=300)

class TestStudentMakeCode:

    async def test_create_code_sucess(self, add_student_with_email, ac: AsyncClient):
        response = await ac.get("students/creating_codes",
                                    params={
                                        "personal_number": "190722" 
                                    })
        assert response.status_code == 200
        redis = Redis()
        async with redis:
            key = await redis.is_exist("190722")
            await redis.delete("190722")

        assert isinstance(key, int)


    async def test_create_code_404(self, add_student_with_email, ac: AsyncClient):
        response = await ac.get("students/creating_codes",
                                    params={
                                        "personal_number": "190721" 
                                    })
        assert response.status_code == 404

    async def test_create_code_422(self, add_student_with_no_email, ac: AsyncClient):
        response = await ac.get("students/creating_codes",
                                    params={
                                        "personal_number": "190722" 
                                    })
        assert response.status_code == 422


class TestStudentVerifyCode:

    async def test_verify_code_sucess(self, add_student_with_email, set_user_key,  ac: AsyncClient):
        response = await ac.get("students/verifying_codes",
                                    params={
                                        "personal_number": "190722" ,
                                        "verification_code": "123456"
                                    })
        assert response.status_code == 200
        response = response.json()
        assert "access_token" in response
        assert "token_type" in response


    async def test_create_code_404(self, add_student_with_email, ac: AsyncClient):
        response = await ac.get("students/verifying_codes",
                                    params={
                                        "personal_number": "1907222" ,
                                        "verification_code": "123456"
                                    })
        assert response.status_code == 404

    async def test_create_code_401(self, add_student_with_no_email, ac: AsyncClient):
        response = await ac.get("students/verifying_codes",
                                    params={
                                        "personal_number": "190722" ,
                                        "verification_code": "1234567"
                                    })
        assert response.status_code == 401