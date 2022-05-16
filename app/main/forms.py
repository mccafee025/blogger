from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import Required,Email,EqualTo, Length
from flask_wtf.file import FileAllowed, FileField
from ..models import User, Comment
from flask_login import current_user
from flask.helpers import total_seconds

class UpdateProfile(FlaskForm):
    username = StringField('Username', validators = [Required(), Length(min = 1, max = 12)])
    email = StringField('Email', validators = [Required(), Email()])
    picture = FileField('Upload', validators = [FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email is already tak
