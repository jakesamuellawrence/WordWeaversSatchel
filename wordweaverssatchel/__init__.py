import flask

from . import translation

def create_app(test_config=None):
	# Application Factory. Creates an instance of the Flask class and sets things up
	app = flask.Flask(__name__)
	
	app.register_blueprint(translation.bp)
	
	@app.route('/')
	def hello():
		return "Home!"
	
	return app