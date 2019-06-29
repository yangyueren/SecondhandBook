
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, IntegerField, FloatField, SelectField, DecimalField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email


class LoginForm (FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    password = PasswordField('passsword', validators=[DataRequired()])
    # remember = BooleanField("remember", validators=[Optional()], default=False )
    submit = SubmitField(u'submit')


class RegisterForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(6, 16)])
    password1 = PasswordField('password', validators=[DataRequired(), Length(6, 16)])
    password2 = PasswordField('password', validators=[DataRequired(), Length(6, 16)])
    # remember = BooleanField("remember", validators=[Optional()], default=False )

    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    paypal = StringField('paypal', validators=[DataRequired()])
    submit = SubmitField(u'submit')


class ChangeUserInfo(FlaskForm):

    password1 = PasswordField('password', validators=[DataRequired(),Length(6, 16)])
    password2 = PasswordField('password', validators=[DataRequired(),Length(6, 16)])

    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    paypal = StringField('paypal', validators=[DataRequired()])
    submit = SubmitField(u'submit')


class BookForm(FlaskForm):
    isbn = StringField('isbn', validators=[DataRequired()])
    book_name = StringField('book name', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    publisher = StringField('publisher', validators=[DataRequired()])
    publish_date = StringField('publish date', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    book_type = StringField('book type', validators=[DataRequired()])
    picture = FileField('picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!'), FileRequired()])
    ini_price = FloatField('initial price', validators=[DataRequired()])
    sell_price = FloatField('selling price', validators=[DataRequired()])

    submit = SubmitField(u'submit')


class SeekBookForm(FlaskForm):
    isbn = StringField('isbn')
    book_name = StringField('book name', validators=[DataRequired()])
    author = StringField('author')
    publisher = StringField('publisher')
    publish_date = StringField('publish date')
    content = StringField('content', validators=[DataRequired()])
    book_type = StringField('book type', validators=[DataRequired()])
    picture = FileField('picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    ini_price = FloatField('initial price')
    sell_price = FloatField('selling price', validators=[DataRequired()])

    submit = SubmitField(u'submit')


class TestForm(FlaskForm):
    isbn = StringField('isbn')
    book_name = StringField('book name', validators=[DataRequired()])
    author = StringField('author')
    submit = SubmitField('submit')

