from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .utils import ShortLinkGenerate


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    short_link_service = ShortLinkGenerate()
    new_url = short_link_service.create_short_link(data)
    return jsonify(new_url), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    short_link_service = ShortLinkGenerate()
    original_link = short_link_service.get_original_link(short_id)
    if original_link is not None:
        return jsonify({'url': original_link}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
