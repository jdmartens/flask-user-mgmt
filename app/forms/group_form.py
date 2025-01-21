from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class GroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    permissions = TextAreaField('Permissions (JSON)')
