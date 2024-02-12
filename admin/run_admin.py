from typing import cast

from flask import Flask
from flask_admin import Admin, AdminIndexView

from db import sync_session
from db import FinancialIndebtedness, Students


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['FLASK_ADMIN_SWATCH'] = 'Cosmo'
    app.secret_key = 'kek'

    admin = Admin(app, name='IC_SYSTEM', index_view=AdminIndexView(name='📃', url='/'), template_mode='bootstrap4')

    from admin.views.finance import FinancialIndebtednessView
    from admin.views.students import StudentsView

    admin.add_view(FinancialIndebtednessView(FinancialIndebtedness, sync_session, name='Фин. задолженность'))
    admin.add_view(StudentsView(Students, sync_session, name='Студенты'))

    return cast(Flask, admin.app)


if __name__ == '__main__':

    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
