# -*- coding:utf-8 -*-
from app.models import Alcohol
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import ValidationError
from wtforms.validators import Length, DataRequired, Regexp


class EditAlcoholForm(FlaskForm):
    isbn = StringField(u"ISBN",
                       validators=[DataRequired(message=u"You forgot to fill in this item!"),
                                   Regexp('[0-9]{13,13}', message=u"ISBN must be 13 digits")])
    title = StringField(u"Title",
                        validators=[DataRequired(message=u"You forgot to fill in this item!"), Length(1, 128, message=u"1 to 128 characters in length")])
    origin_title = StringField(u"Origin title", validators=[Length(0, 128, message=u"Up to 128 characters in length")])
    manufacturer = StringField(u"Manufacturer", validators=[Length(0, 128, message=u"Up to 64 characters in length")])
    distributor = StringField(u"Distributor", validators=[Length(0, 64, message=u"Up to 64 characters in length")])
    image = StringField(u"Image", validators=[Length(0, 128, message=u"Up to 128 characters in length")])
    tags = StringField(u"Tags", validators=[Length(0, 128, message=u"Up to 128 characters in length")])
    price = StringField(u"Price", validators=[Length(0, 64, message=u"Up to 32 characters in length")])
    numbers = IntegerField(u"Collection", validators=[DataRequired(message=u"You forgot to fill in this item!")])
    summary = PageDownField(u"Brief introduction")
    catalog = PageDownField(u"Table of contents")
    submit = SubmitField(u"Save Changes")


class AddAlcoholForm(EditAlcoholForm):
    def validate_isbn(self, filed):
        if Alcohol.query.filter_by(isbn=filed.data).count():
            raise ValidationError(u'The same ISBN already exists and cannot be entered, please check carefully whether the alcohol is already in stock.')


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField(u"Search for")


