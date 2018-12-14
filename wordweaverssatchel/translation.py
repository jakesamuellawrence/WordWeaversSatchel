import flask
import werkzeug

cache = []

bp = flask.Blueprint('translate', __name__, url_prefix='/translation')

@bp.route('/moth_to_eng', methods=['POST'])
def moth_to_eng():
	if flask.request.method == 'POST':
		mothertongue_in = flask.request.form['mothertongue_box']
	else:
		return "ERROR: Page was not submitted with POST"
	
	translation = search_by_mothertongue(mothertongue_in)
	if translation is None:
		return 'No results matched search'
	mothertongue_out = translation[0]
	english_out = translation[1]
	
	return flask.render_template('home.html', english_box_value=english_out, mothertongue_box_value=mothertongue_out)
	
@bp.route('/eng_to_moth', methods=['POST'])
def en_to_moth():
	if flask.request.method == 'POST':
		english_in = flask.request.form['english_box']
	else:
		return "ERROR: Page was not submitted with POST"
	
	translation = search_by_english(english_in)
	if translation is None:
		return 'No results matched search'
	mothertongue_out = translation[0]
	english_out = translation[1]
	
	return flask.render_template('home.html', mothertongue_box_value=mothertongue_out, english_box_value=english_out)
	
def search_by_mothertongue(target):		
	# check if cache is empty, load if it is
	if cache == []:
		load_mothertongue_dictionary()
	
	# search for given term
	for i in cache:
		if i[0].lower() == target.lower():
			return i
	return None
	
def search_by_english(target):		
	# check if cache is empty, load if it is
	if cache == []:
		load_mothertongue_dictionary()
	
	# search for given term
	for i in cache:
		if i[1].lower() == target.lower():
			return i
	return None

def load_mothertongue_dictionary():
	# read in data from csv file
	file = flask.current_app.open_resource("mothertongue_dictionary.csv")
	for line in file:
		line = line.decode().split(',')
		cache.append(line)