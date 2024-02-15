from re import match

from flask import jsonify, request

from . import app, db
from .constants import AVAILABLE_SYMBOLS, MAX_SHORT_URL
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id', None)
    if not custom_id or custom_id is None:
        data['custom_id'] = get_unique_short_id()
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
    return jsonify(new_url.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is not None:
        return jsonify({'url': link.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
