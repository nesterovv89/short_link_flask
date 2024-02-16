import random
import string
from re import match

from . import db
from .constants import AVAILABLE_SYMBOLS, MAX_SHORT_URL, SHORT_RANDOM_URL
from .error_handlers import InvalidAPIUsage
from .models import URLMap


class ShortLinkGenerate:
    def create_short_link(self, data):
        if not data:
            raise InvalidAPIUsage('Отсутствует тело запроса')
        if 'url' not in data:
            raise InvalidAPIUsage('"url" является обязательным полем!')
        custom_id = data.get('custom_id', None)
        if not custom_id or custom_id is None:
            data['custom_id'] = self._generate_short_id()
        if len(data['custom_id']) > MAX_SHORT_URL:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
        elif not match(AVAILABLE_SYMBOLS, data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        new_url = URLMap()
        new_url.from_dict(data)
        db.session.add(new_url)
        db.session.commit()
        return new_url.to_dict()

    def get_original_link(self, short_id):
        link = URLMap.query.filter_by(short=short_id).first()
        if link is not None:
            return link.original
        return None

    def _generate_short_id(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(SHORT_RANDOM_URL))
