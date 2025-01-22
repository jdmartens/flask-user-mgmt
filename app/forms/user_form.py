from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FileField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Profile Picture')
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    groups = SelectMultipleField('Groups', coerce=int)
