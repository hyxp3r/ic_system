from flask_admin.contrib.sqla import ModelView


class StudentsView(ModelView):
    can_edit = True
    can_delete = False
    can_view_details = True

    column_default_sort = [("created_at", True), ("fio", False)]

    column_sortable_list = ["created_at"]
    column_searchable_list = ("fio", "personal_number")
    #column_filters = ("status",)

    form_columns = ["fio", "personal_number", "group", "program", "form", "email", "api_key"]



