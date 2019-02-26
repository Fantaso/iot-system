from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange


class PreAddPumpForm:
    def __init__(self, pump_name, pump_brand, pump_flow_rate, pump_head, pump_watts):
        self.pump_name       = pump_name
        self.pump_brand      = pump_brand
        self.pump_flow_rate  = pump_flow_rate
        self.pump_head       = pump_head
        self.pump_watts      = pump_watts

class AddPumpForm(FlaskForm):
    pump_name               = StringField('Pump name',                              validators=[DataRequired(), Length(min=2, max=30, message='Give it a name for sanity MAX 30.')])
    pump_brand              = StringField('Pump brand',                             validators=[DataRequired(), Length(min=2, max=30, message='Your pump supplier or brand name')])
    pump_flow_rate          = FloatField('Pump flow rate (liters per sec)',         validators=[DataRequired(), NumberRange(min=1, max=500, message="Your pump's water capacity or water turn over")])
    pump_head               = FloatField('Pump head (meters)',                      validators=[DataRequired(), NumberRange(min=1, max=500, message="Your pump's max head pressure or height power")])
    pump_watts              = FloatField('Pump power consumption (kilo Watts)',     validators=[DataRequired(), NumberRange(max=1000, message="Your pump's wattage consumption")])
