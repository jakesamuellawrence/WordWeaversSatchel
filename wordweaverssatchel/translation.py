import flask

bp = flask.Blueprint('spectrum', __name__)

@bp.route('/translate')
def translate():
	return 'Translate'