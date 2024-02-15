from flask import abort, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        elif URLMap.query.filter_by(short=custom_id).first():
            form.custom_id.errors = ['Предложенный вариант короткой ссылки уже существует.']
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(url_map)
        db.session.commit()
        return (render_template('index.html', form=form, short=custom_id), 200)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    original_link = URLMap.query.filter_by(short=short).first()
    if original_link:
        return redirect(original_link.original)
    abort(404)