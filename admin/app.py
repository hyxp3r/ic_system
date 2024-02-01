from typing import cast

from flask import Flask
from flask_admin import Admin, AdminIndexView

from db import sync_session
from db.models.finance import FinancialIndebtedness


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['FLASK_ADMIN_SWATCH'] = 'Cosmo'
    app.secret_key = 'kek'

    admin = Admin(app, name='IC_SYSTEM', index_view=AdminIndexView(name='📃', url='/'), template_mode='bootstrap4')

    from admin.views.finance import FinancialIndebtednessView

    admin.add_view(FinancialIndebtednessView(FinancialIndebtedness, sync_session, name='Фин. задолженность'))

    return cast(Flask, admin.app)


if __name__ == '__main__':

    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
