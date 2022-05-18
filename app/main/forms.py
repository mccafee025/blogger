from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, ValidationError, PasswordField
from wtforms.validators import Required,Email,EqualTo, Length
from flask_wtf.file import FileAllowed, FileField
from ..models import User
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
                raise ValidationError('Email is already taken.')
class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators = [Required()])
    confirm_password = PasswordField('Confirm Password', validators = [Required(), EqualTo('Password')])
    submit = SubmitField('Reset Password')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Please register for an account')
class BlogForm(FlaskForm):
    title = StringField('Title', validators = [Required()])
    body = TextAreaField('Your blog here ', validators = [Required()])
    submit = SubmitField('Post')
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment on Post', validators = [Required()])
    submit = SubmitField('Post')
