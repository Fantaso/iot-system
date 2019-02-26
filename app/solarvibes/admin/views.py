from flask import Blueprint, url_for, flash, redirect, render_template

from solarvibes.models import User, Role, roles_users
from solarvibes.models import Farm, Field, crops_field, Crop
from solarvibes.models import DailyFieldInput
from solarvibes.models import Agrimodule, Agripump, Agrisensor, Pump, Measurement
from solarvibes.models import AgrimoduleList, AgrisensorList, AgripumpList, WelcomeLog
from solarvibes import application, db

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# to deal with pictures db view
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join

admin_bp = Blueprint(
        'admin_bp',
        __name__,
)

admin = Admin(application, template_mode = 'bootstrap3')


class UserView(ModelView):
    column_exclude_list = ['password'] # remove a view column NOT EDIT COLUMN
    column_display_pk = True            # True forces view to display pk = primary_key = id
    can_create = True                   # False disables user to add to db view
    can_delete = True                   # False disables user to delete db view
    can_edit = True                     # False disables user to edit db view
    can_export = True                   # True enables to download csv file data from view
    create_modal = True                 # True enables modal view for adding new data to table
    form_excluded_columns = ('password')# remove field from EDIT VIEW
    inline_models = [Agrimodule, Pump, Farm]

    # column_formatters # specify how you want data to look in the view
    # column_default_sort # default sorting is pk
    # column_searchable
    # page_size = 20
    # after_model_delete
    # after_model_change
    # export_types = ['csv', 'xsl'] # i need to use another library

class PkView(ModelView):
    column_display_pk = True


admin.add_view(UserView(User, db.session))
admin.add_view(PkView(Role, db.session))
# admin.add_view(PkView(roles_users, db.session))
admin.add_view(PkView(Farm, db.session))
admin.add_view(PkView(Field, db.session))
# admin.add_view(PkView(crops_field, db.session))
admin.add_view(PkView(Crop, db.session))
admin.add_view(PkView(DailyFieldInput, db.session))
admin.add_view(PkView(Agrimodule, db.session))
admin.add_view(PkView(Agripump, db.session))
admin.add_view(PkView(Agrisensor, db.session))
admin.add_view(PkView(Pump, db.session))
admin.add_view(PkView(Measurement, db.session))
admin.add_view(PkView(AgrimoduleList, db.session))
admin.add_view(PkView(AgrisensorList, db.session))
admin.add_view(PkView(AgripumpList, db.session))
admin.add_view(PkView(WelcomeLog, db.session))

def get_path():
    return join(dirname(__file__)[:-5], 'static/images/crops')
admin.add_view(FileAdmin(get_path(), '/crops/', name='CropImage'))
