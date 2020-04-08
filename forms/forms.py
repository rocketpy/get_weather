from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


class SignUp(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20)])
    surname = StringField('surname', validators=[InputRequired(message='An surname is required !'),
                                                 Length(min=2, max=20)])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=5, max=255)])
    sex = StringField('sex', validators=[InputRequired(message='Field sex is required !'),
                                         Length(min=4, max=6, message='Not greater a 6 simbols')])
    birthday = StringField('birthday', validators=[InputRequired(message='Field birthday is required !'),
                                                   Length(min=6, max=10, message='Not greater a 6 simbols')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=5, max=255)])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])
    remember = BooleanField('remember me')


class AddPostForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20, message='It is a wrong length')])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=5, max=255, message='It is a wrong length')])
    message = StringField('message', validators=[InputRequired(message='Text field is required !'),
                                                 Length(min=5, max=1000, message='It is a wrong length')])
