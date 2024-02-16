from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import ShortLinkGenerate


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    short_link_service = ShortLinkGenerate()

    if form.validate_on_submit():
        data = {
            'url': form.original_link.data,
            'custom_id': form.custom_id.data,
        }
        if URLMap.query.filter_by(short=data['custom_id']).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        new_url = short_link_service.create_short_link(data)
        if new_url:
            return (render_template('index.html', form=form, short=data['custom_id']), 200)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    short_link_service = ShortLinkGenerate()
    original_link = short_link_service.get_original_link(short)
    if original_link:
        return redirect(original_link)
    abort(404)
