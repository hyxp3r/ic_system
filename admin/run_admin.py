from typing import cast

from flask import Flask
from flask_basicauth import BasicAuth
from flask_admin import Admin, AdminIndexView

from db import FinancialIndebtedness, Students, sync_session

from admin.config import AdminSettings
from admin.views.finance import FinancialIndebtednessView
from admin.views.students import StudentsView

def create_app() -> Flask:
    settings = AdminSettings()
    app = Flask(__name__)
    app.config['BASIC_AUTH_USERNAME'] = settings.login
    app.config['BASIC_AUTH_PASSWORD'] = settings.password
    app.config['BASIC_AUTH_FORCE'] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
    app.secret_key = settings.key

    admin = Admin(app, name='IC_SYSTEM', index_view=AdminIndexView(name='📃', url='/'), template_mode='bootstrap4')

    admin.add_view(FinancialIndebtednessView(FinancialIndebtedness, sync_session, name='Фин. задолженность'))
    admin.add_view(StudentsView(Students, sync_session, name='Студенты'))

    return cast(Flask, admin.app)

app = create_app()
basic_auth = BasicAuth(app)

