import flask

bp = flask.Blueprint('translate', __name__, url_prefix='/translation')

@bp.route('/moth_to_eng', methods=['POST'])
def moth_to_eng():
	if flask.request.method == 'POST':
		mother_tongue_value = flask.request.form['mothertongue_box']
	return flask.render_template('home.html', english_box_value=mother_tongue_value)
	
@bp.route('/eng_to_moth')
def en_to_moth():
	return 'ENG TO MOTH!!!!'