from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLForm
from .services import ShortLinkService
from .error_handlers import ShortLinkServiceError


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    short_link_service = ShortLinkService()

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        try:
            new_url = short_link_service.create_short_link(original_link, custom_id)
            return render_template('index.html', form=form, short=new_url['short_link'])
        except ShortLinkServiceError as e:
            flash(e.message)
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    short_link_service = ShortLinkService()
    original_link = short_link_service.get_original_link(short)
    if original_link:
        return redirect(original_link)
    abort(404)
