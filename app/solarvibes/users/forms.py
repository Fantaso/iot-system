from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import Email, Length, NumberRange
from flask_uploads import IMAGES


# Constructor
class PreUserProfileForm:
    def __init__(self, username, name, last_name, address, zipcode, city, state, country, email, email_rec, birthday, image, mobile):
        self.username    = username
        self.name        = name
        self.last_name   = last_name
        self.address     = address
        self.zipcode     = zipcode
        self.city        = city
        self.state       = state
        self.country     = country
        self.email       = email
        self.email_rec   = email_rec
        self.birthday    = birthday
        self.image       = image
        self.mobile      = mobile

class UserProfileForm(FlaskForm):
    username    = StringField('Username',           validators=[Length(min=2, max=30, message='Your Username needs to be at least 2 characters long.')])
    name        = StringField('Name',               validators=[Length(min=2, max=30, message='Your name needs to be at least 2 characters long.')])
    last_name   = StringField('Last name',          validators=[Length(min=2, max=30, message='Your last name needs to be at least 2 characters long.')])
    address     = StringField('Address',            validators=[Length(min=2, max=30, message='Minimum: 2 characters.')])
    zipcode     = IntegerField('Zipcode',            validators=[NumberRange(min=1, max=99999, message='Number of your code')])
    city        = StringField('City',               validators=[Length(min=2, max=30, message='Minimum: 2 characters.')])
    state       = StringField('State',              validators=[Length(min=2, max=30, message='Minimum: 2 characters.')])
    country     = StringField('Country',            validators=[Length(min=2, max=30, message='Minimum: 2 characters.')])
    email       = StringField('Email',              validators=[Length(min=5, max=30, message=None), Email()])
    email_rec   = StringField('Recovery Email',     validators=[Length(min=5, max=30, message=None), Email()])
    birthday    = DateField('Birthday',             format='%d %B, %Y')
    image       = FileField(                        validators=[FileAllowed(IMAGES, 'Only images allowed.')])
    mobile      = StringField('Mobile',             validators=[Length(min=7, max=30, message=None)])
