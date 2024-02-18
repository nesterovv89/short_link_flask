from flask import jsonify, request

from . import app
from .error_handlers import ShortLinkServiceError
from .services import ShortLinkService


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not data:
        raise ShortLinkServiceError('Отсутствует тело запроса')
    if 'url' not in data:
        raise ShortLinkServiceError('"url" является обязательным полем!')
    short_link_service = ShortLinkService()
    try:
        new_url = short_link_service.create_short_link(data['url'], data.get('custom_id', None))
        return jsonify(new_url), 201
    except ShortLinkServiceError as e:
        return e.to_dict(), e.status_code


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    short_link_service = ShortLinkService()
    original_link = short_link_service.get_original_link(short_id)
    if original_link is not None:
        return jsonify({'url': original_link}), 200
    raise ShortLinkServiceError('Указанный id не найден', 404)
