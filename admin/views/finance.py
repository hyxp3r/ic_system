from flask_admin.contrib.sqla import ModelView


class FinancialIndebtednessView(ModelView):
    can_edit = False
    can_create = True
    can_delete = False
    can_view_details = True

    column_sortable_list = ['created_at']

    form_columns = ['fio', 'personal_number', 'contract_number', 'sum', 'status']

    column_labels = {'user.name': 'Full Name', 'timestamp': 'Created Date'}
