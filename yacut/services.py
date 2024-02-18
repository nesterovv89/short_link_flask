import random
import string
from re import match

from . import db
from .constants import AVAILABLE_SYMBOLS, MAX_SHORT_URL, SHORT_RANDOM_URL
from .error_handlers import ShortLinkServiceError
from .models import URLMap


class ShortLinkService:
    def create_short_link(self, original_link, custom_id=None):
        if not original_link:
            raise ShortLinkServiceError('Отсутствует оригинальная ссылка')

        if custom_id and not match(AVAILABLE_SYMBOLS, custom_id):
            raise ShortLinkServiceError('Указано недопустимое имя для короткой ссылки')

        if custom_id and len(custom_id) > MAX_SHORT_URL:
            raise ShortLinkServiceError('Указано недопустимое имя для короткой ссылки')

        if custom_id and URLMap.query.filter_by(short=custom_id).first():
            raise ShortLinkServiceError('Предложенный вариант короткой ссылки уже существует.')

        if not custom_id:
            custom_id = self._generate_short_id()

        new_url = URLMap(original=original_link, short=custom_id)
        db.session.add(new_url)
        db.session.commit()
        return new_url.to_dict()

    def get_link_by_short_id(self, short_id):
        link = URLMap.query.filter_by(short=short_id).first()
        return link

    def get_original_link(self, short_id):
        link = self.get_link_by_short_id(short_id)
        if link is not None:
            return link.original
        return None

    def _generate_short_id(self):
        return (
            ''.join(random.choice(string.ascii_letters + string.digits)
                    for _ in range(SHORT_RANDOM_URL))
        )
