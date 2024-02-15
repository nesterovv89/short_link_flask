from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, Length, Optional, Regexp

from .constants import AVAILABLE_SYMBOLS, MAX_SHORT_URL, MAX_URL_LENGHT


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[URL(message='Необходимо указать ссылку в URL формате'),
                    Length(max=MAX_URL_LENGHT)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Regexp(AVAILABLE_SYMBOLS), Length(max=MAX_SHORT_URL), Optional()]
    )
    submit = SubmitField('Создать')