from flask_admin.contrib.sqla import ModelView


class FinancialIndebtednessView(ModelView):
    can_edit = True
    can_delete = False
    can_view_details = True

    column_default_sort = [('created_at', True), ('fio', False)]

    column_sortable_list = ['created_at']
    column_searchable_list = ('fio', 'personal_number')
    column_filters = ('status',)

    form_columns = ['fio', 'personal_number', 'contract_number', 'sum', 'status']

    column_labels = {
        'fio': 'ФИО',
        'personal_number': 'Личный номер',
        'contract_number': 'Номер договора',
        'sum': 'Сумма задолженности',
        'status': 'Актуальность',
        'file_created_time': 'Дата создания файла',
        'created_at': 'Дата добавления записи',
    }
