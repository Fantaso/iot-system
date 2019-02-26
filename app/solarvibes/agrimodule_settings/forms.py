from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

# MANAGE SYSTEMS FORMS
class NewAgrimoduleForm(FlaskForm):
    name                = StringField('Agrimodule name', validators=[DataRequired(), Length(min=2, max=30, message='Give it a name for sanity MAX 30.')])
    identifier          = StringField('Agrimodule code', validators=[DataRequired(), Length(min=2, max=30, message='Your agrimodule identifier is in the back of your agrimodule.')])
    # lat                 = FloatField('latitude location', validators=[DataRequired(), NumberRange(min=-90, max=90, message='write the lat coordinates')])
    # lon                 = FloatField('longitude location', validators=[DataRequired(), NumberRange(min=-180, max=180, message='write the lon coordinates')])
    field_choices       = SelectField('Field to monitor:', validators=[Optional(strip_whitespace=True)], coerce = int)

# '/user/farm/field/agrimodule/add-sensor'
class AgrimoduleAddSensorForm(FlaskForm):
    agrimodule_choices  = SelectField(label='Agrimodule choices', validators=[DataRequired()], coerce = int)
    sensor_choices      = SelectField(label='Agrimodule choices', validators=[DataRequired()], choices=[('Agrisensor','Agrisensor'),('Agripump','Agripump')])
    identifier          = StringField('Sensor code', validators=[DataRequired(), Length(min=2, max=30, message='Your sensor system identifier is in the back of your device.')])

# '/user/farm/field/agrimodule/edit-agrimodule/<agrimodule_id>'
class PreEditAgrimoduleForm:
    def __init__(self, name, field_choices):
        self.name = name
        self.field_choices = field_choices

class EditAgrimoduleForm(FlaskForm):
    name                = StringField('Agrimodule name', validators=[DataRequired(), Length(min=2, max=30, message='Give it a name for sanity MAX 30.')])
    field_choices       = SelectField(label='Field to monitor:', validators=[Optional(strip_whitespace=True)], coerce = int)

# '/user/farm/field/agripump/change-pump/'
class PreEditAgripumpForm:
    def __init__(self, pump_choices):
        self.pump_choices = pump_choices

class EditAgripumpForm(FlaskForm):
    pump_choices        = SelectField(label='Pump choices', validators=[Optional(strip_whitespace=True)], coerce = int)
