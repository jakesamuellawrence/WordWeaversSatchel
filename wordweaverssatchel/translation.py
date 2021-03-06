import flask
import werkzeug
import math

cache = []

bp = flask.Blueprint('translate', __name__, url_prefix='/translation')

@bp.route('/moth_to_eng', methods=['POST'])
def moth_to_eng():
	if flask.request.method == 'POST':
		mothertongue_in = flask.request.form['mothertongue_box']
	else:
		return "ERROR: Page was not submitted with POST"
	
	mothertongue_out = ""
	english_out = ""
	base_cost = 0
	multiplier = 0
	breakdown = ""
	
	print(cache)
	
	mothertongue_in = mothertongue_in.split()
	for i in mothertongue_in:
		translation = search_by_mothertongue(i)
		print(cache)
		if translation is None:
			return 'No results matched search'
		mothertongue_out = mothertongue_out + translation[0] + " "
		english_out = english_out + translation[1] + " "
		if translation[2] == 'true':
			multiplier = multiplier + float(translation[3])
		else:
			base_cost = base_cost + float(translation[3])
		breakdown = breakdown + translation[0].strip() + ', ' + translation[1].strip() + ', ' +  translation[2].strip() + ', ' +  translation[3].strip() + '<br/>'
		
	cost = base_cost * multiplier
	
	return flask.render_template('home.html', english_box_value=english_out, mothertongue_box_value=mothertongue_out, cost=math.ceil(cost), breakdown=breakdown)
	
@bp.route('/eng_to_moth', methods=['POST'])
def en_to_moth():
	if flask.request.method == 'POST':
		english_in = flask.request.form['english_box']
	else:
		return "ERROR: Page was not submitted with POST"
	
	mothertongue_out = ""
	english_out = ""
	base_cost = 0
	multiplier = 0
	
	english_in = english_in.split()
	for i in english_in:
		translation = search_by_english(i)
		if translation is None:
			return 'No results matched search'
		mothertongue_out = mothertongue_out + translation[0] + " "
		english_out = english_out + translation[1] + " "
		if translation[2] == 'true':
			multiplier = multiplier + float(translation[3])
		else:
			base_cost = base_cost + float(translation[3])
			
	cost = base_cost * multiplier
	
	return flask.render_template('home.html', mothertongue_box_value=mothertongue_out, english_box_value=english_out, cost=math.ceil(cost))

@bp.route('/new', methods=['POST'])
def new_vocabulary():
	if flask.request.method == 'POST':
		new_mothertongue = flask.request.form['new_mothertongue']
		new_english = flask.request.form['new_english']
		new_arbonym = flask.request.form['new_arbonym']
		new_cost = flask.request.form['new_cost']
	else:
		return "ERROR: Page was not submitted with POST"
		
	file = open("resources/mothertongue_dictionary.csv", "a")
	file.write('\n' 
			   + new_mothertongue + ','
			   + new_english + ','
			   + new_arbonym + ','
			   + new_cost)
	file.close()
	print('clearing cache')
	clear_cache()
		
	return flask.render_template('home.html')
	
def search_by_mothertongue(target):		
	# check if cache is empty, load if it is
	if cache == []:
		load_mothertongue_dictionary()
	
	# search for given term
	for i in cache:
		if i[0].lower().strip() == target.lower().strip():
			return i
	return None
	
def search_by_english(target):		
	# check if cache is empty, load if it is
	if cache == []:
		load_mothertongue_dictionary()
	
	# search for given term
	for i in cache:
		if i[1].lower().strip() == target.lower().strip():
			return i
	return None

def load_mothertongue_dictionary():
	global cache
	# read in data from csv file
	file = open("resources/mothertongue_dictionary.csv")
	for line in file:
		line = line.split(',')
		cache.append(line)
		
def clear_cache():
	global cache
	cache = []
	print('cache cleared!!!')