import pyodbc

from api.config import TandemSettings

settings = TandemSettings()


class Tandem:
    __server = settings.server
    __database = settings.database
    __uid = settings.uid
    __pwd = settings.pwd
    __connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER='
        + __server
        + ';DATABASE='
        + __database
        + ';UID='
        + __uid
        + ';PWD='
        + __pwd
    )

    def __enter__(self):
        self.__conn = pyodbc.connect(self.__connection_string)

    def __exit__(self, *args):
        self.__conn.close()

    def get_students(self) -> list[dict]:
        stmt = """  
        SELECT DISTINCT
        VPO.LASTNAME + ' ' + VPO.FIRSTNAME + ISNULL(' ' + VPO.MIDDLENAME, '') fio
        ,VPO.BOOKNUMBER personal_number 
        ,VPO.GROUPTITLE as 'group'
        ,VPO.SUBJECTCODE + ' ' + VPO.SUBJECTTITLE program
        ,VPO.DEVELOPFORMTITLE form
        ,VPO.EMAIL email
        FROM vpo2_view  VPO
        WHERE VPO.STATUSTITLE = 'активный'
        """
        results = []
        cursor = self.__conn.execute(stmt)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
