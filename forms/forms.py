from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


class SignUp(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20)])
    surname = StringField('surname', validators=[InputRequired(message='An surname is required !'),
                                                 Length(min=2, max=20)])
    sex = StringField('sex', validators=[Length(min=4, max=6, message='Not greater a 6 simbols')])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=10, max=50)])
    birthday = StringField('birthday', validators=[Length(min=6, max=10, message='Not greater a 6 simbols')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=10, max=50)])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])
    remember = BooleanField('remember me')


class AddPostForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20)])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=10, max=50)])
    message = StringField('message', validators=[InputRequired(message='Text field is required !'),
                                                 Length(min=5, max=1000)])
